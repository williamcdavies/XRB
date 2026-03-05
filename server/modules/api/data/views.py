import csv
import math
import os
import shutil
from pathlib import Path

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group as AuthGroup
from django.http import FileResponse

from .permissions import check_path_access, check_write_access

User = get_user_model()

BASE_DATA_DIR = Path(os.environ.get('DATA_DIR', '/data'))

def is_path_safe(file_path: str) -> bool:
    try:
        resolved = Path(file_path).resolve()
        return resolved.is_relative_to(BASE_DATA_DIR.resolve())
    except (ValueError, OSError):
        return False


def validate_and_convert_value(value: str, column_name: str) -> dict:
    result = {
        'value': None,
        'original': value,
        'is_valid': True,
        'warning': None,
    }

    if value is None or value.strip() == '':
        result['value'] = None
        result['warning'] = 'empty_value'
        return result

    value = value.strip()

    if value.upper() == 'NULL':
        result['value'] = None
        result['warning'] = 'null_value'
        return result

    if value.lower() in ('inf', '+inf'):
        result['value'] = None
        result['is_valid'] = False
        result['warning'] = 'positive_infinity'
        return result

    if value.lower() == '-inf':
        result['value'] = None
        result['is_valid'] = False
        result['warning'] = 'negative_infinity'
        return result

    if value.lower() == 'nan':
        result['value'] = None
        result['is_valid'] = False
        result['warning'] = 'not_a_number'
        return result

    try:
        if '.' not in value and 'e' not in value.lower():
            result['value'] = int(value)
        else:
            float_val = float(value)
            if math.isinf(float_val):
                result['value'] = None
                result['is_valid'] = False
                result['warning'] = 'infinity_after_conversion'
                return result
            if math.isnan(float_val):
                result['value'] = None
                result['is_valid'] = False
                result['warning'] = 'nan_after_conversion'
                return result
            result['value'] = float_val
    except ValueError:
        result['value'] = value

    return result


def read_validate_csv(file_path: str) -> dict:
    data = []
    columns = []
    warnings = []
    row_count = 0

    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)

        try:
            columns = [c.strip() for c in next(reader)]
        except StopIteration:
            return {'success': False, 'error': 'Empty CSV file', 'data': [], 'columns': []}

        for row_idx, row in enumerate(reader, start=2):
            row_count += 1

            if len(row) != len(columns):
                warnings.append({
                    'row': row_idx,
                    'type': 'column_count_mismatch',
                    'message': f'Row {row_idx} has {len(row)} columns, expected {len(columns)}',
                })
                if len(row) < len(columns):
                    row.extend([''] * (len(columns) - len(row)))
                else:
                    row = row[:len(columns)]

            row_data = {}
            for col_name, value in zip(columns, row):
                validated = validate_and_convert_value(value, col_name)
                row_data[col_name] = validated['value']

                if validated['warning'] and validated['warning'] not in ('empty_value', 'null_value'):
                    warnings.append({
                        'row': row_idx,
                        'column': col_name,
                        'type': validated['warning'],
                        'original_value': validated['original'],
                        'converted_value': validated['value'],
                    })

            data.append(row_data)

    result = {
        'data': data,
        'columns': columns,
        'metadata': {
            'row_count': row_count,
            'column_count': len(columns),
            'warnings': warnings,
            'warning_count': len(warnings),
            'file_path': file_path,
        },
    }
    return result


# -----------------------------------------------------
# API Endpoints
# -----------------------------------------------------

@api_view(['GET'])
@permission_classes([AllowAny])
def download_file(request):
    """
    allow any user to download a file as long as they can access it

    query parameters:
    -----------------
    path : str (required)
    """
    relative_path = request.query_params.get('path')

    if not relative_path:
        return Response(
            {'error': 'Missing required parameter: path'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = request.user if request.user.is_authenticated else None
    allowed, reason = check_path_access(user, relative_path)
    if not allowed:
        return Response(
            {'error': f'Access denied: {reason}'},
            status=status.HTTP_403_FORBIDDEN,
        )

    file_path = BASE_DATA_DIR / relative_path
    if not is_path_safe(str(file_path)):
        return Response(
            {'error': 'Access denied: path outside allowed directories'},
            status=status.HTTP_403_FORBIDDEN,
        )

    if not file_path.exists():
        return Response(
            {'error': f'File not found: {relative_path}'},
            status=status.HTTP_404_NOT_FOUND,
        )

    if not file_path.is_file():
        return Response(
            {'error': 'Not a file'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        return FileResponse(
            open(file_path, 'rb'),
            as_attachment=True,
            filename=file_path.name,
        )
    except PermissionError:
        return Response(
            {'error': 'Permission denied when reading file'},
            status=status.HTTP_403_FORBIDDEN,
        )
    except Exception as e:
        return Response(
            {'error': f'Error reading file: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(['POST'])
def upload_file(request):
    """
    user must be authenticated with bearer token to upload file
    
    form data:
    ---------
    file : file (required)
    path : str (required)
        Target directory relative to /data, e.g. users/jake,
        groups/astro-lab, or public.
    """

    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    target_dir = request.data.get('path', '').strip('/')
    if not target_dir:
        return Response(
            {'error': 'Missing required parameter: path (target directory)'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    allowed, reason = check_write_access(request.user, target_dir)
    if not allowed:
        return Response(
            {'error': f'Upload denied: {reason}'},
            status=status.HTTP_403_FORBIDDEN,
        )

    uploaded_file = request.FILES['file']

    try:
        upload_dir = BASE_DATA_DIR / target_dir
        upload_dir.mkdir(parents=True, exist_ok=True)

        safe_name = uploaded_file.name.replace(' ', '_').replace('/', '_').replace('\\', '_')
        file_path = upload_dir / safe_name

        with open(file_path, 'wb+') as dest:
            for chunk in uploaded_file.chunks():
                dest.write(chunk)

        relative = str(file_path.relative_to(BASE_DATA_DIR))

        return Response({
            'path': relative,
            'name': file_path.name,
            'size': file_path.stat().st_size,
            'type': file_path.suffix.lower().lstrip('.'),
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {'error': f'Error uploading file: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(['POST'])
def create_directory(request):
    """
    Authenticated user creates a new directory under a path they can write to.

    body (JSON or form):
    --------------------
    path : str (required)
        Parent directory relative to /data, e.g. public, users/jake, groups/astro-lab.
    name : str (required)
        New directory name (single segment; no slashes).
    """
    parent = (request.data.get('path') or '').strip().rstrip('/')
    name = (request.data.get('name') or '').strip()

    if not parent:
        return Response(
            {'error': 'Missing required parameter: path (parent directory)'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if not name:
        return Response(
            {'error': 'Missing required parameter: name (directory name)'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if '/' in name or '\\' in name:
        return Response(
            {'error': 'Directory name must not contain slashes'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    target_path = f'{parent}/{name}' if parent else name

    allowed, reason = check_write_access(request.user, target_path)
    if not allowed:
        return Response(
            {'error': f'Create directory denied: {reason}'},
            status=status.HTTP_403_FORBIDDEN,
        )

    full_path = BASE_DATA_DIR / target_path
    if not is_path_safe(str(full_path)):
        return Response(
            {'error': 'Access denied: path outside allowed directories'},
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        full_path.mkdir(parents=True, exist_ok=False)
        return Response(
            {'path': target_path, 'name': name},
            status=status.HTTP_201_CREATED,
        )
    except FileExistsError:
        return Response(
            {'error': f'Directory already exists: {target_path}'},
            status=status.HTTP_409_CONFLICT,
        )
    except Exception as e:
        return Response(
            {'error': f'Error creating directory: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(['DELETE'])
def delete_file(request):
    """
    Authenticated user deletes a file they have write access to.

    query parameters:
    -----------------
    path : str (required)
        File path relative to /data.
    """
    relative_path = request.query_params.get('path', '').strip('/')

    if not relative_path:
        return Response(
            {'error': 'Missing required parameter: path'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    allowed, reason = check_write_access(request.user, relative_path)
    if not allowed:
        return Response(
            {'error': f'Delete denied: {reason}'},
            status=status.HTTP_403_FORBIDDEN,
        )

    file_path = BASE_DATA_DIR / relative_path
    if not is_path_safe(str(file_path)):
        return Response(
            {'error': 'Access denied: path outside allowed directories'},
            status=status.HTTP_403_FORBIDDEN,
        )

    if not file_path.exists():
        return Response(
            {'error': f'Not found: {relative_path}'},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        if file_path.is_file():
            file_path.unlink()
        elif file_path.is_dir():
            shutil.rmtree(file_path)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except PermissionError:
        return Response(
            {'error': 'Permission denied'},
            status=status.HTTP_403_FORBIDDEN,
        )
    except Exception as e:
        return Response(
            {'error': f'Error deleting: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def browse_files(request):
    """
    any user can browse files, but authenticated directories are still protected

    query parameters
    ----------------
    path : str (default '')
        Directory relative to /data.
        if none provided, then return all possible paths 
    """
    base_path = request.query_params.get('path', '').strip('/')

    user = request.user if request.user.is_authenticated else None
    if base_path:
        allowed, reason = check_path_access(user, base_path)
        if not allowed:
            return Response({'error': f'Access denied: {reason}'}, status=status.HTTP_403_FORBIDDEN)

    if not base_path:
        items = [{'name': 'public', 'path': 'public', 'type': 'directory'}]
        if user and user.is_authenticated:
            items.append({
                'name': user.email,
                'path': f'users/{user.email}',
                'type': 'directory',
            })
            for group in user.groups.all().order_by('name'):
                items.append({
                    'name': group.name,
                    'path': f'groups/{group.name}',
                    'type': 'directory',
                })
        return Response({'path': '', 'items': items, 'count': len(items)})

    full_path = BASE_DATA_DIR / base_path

    if not is_path_safe(str(full_path)):
        return Response({'error': 'Access denied: path outside allowed directories'}, status=status.HTTP_403_FORBIDDEN)

    if base_path == 'users' and user and user.is_authenticated:
        user_dir = full_path / user.email
        user_items = [{'name': user.email, 'path': f'users/{user.email}', 'type': 'directory'}] if user_dir.is_dir() else []
        return Response({'path': base_path, 'items': user_items, 'count': len(user_items)})

    if not full_path.exists():
        return Response({'error': 'Directory not found'}, status=status.HTTP_404_NOT_FOUND)

    if not full_path.is_dir():
        return Response({'error': 'Path is not a directory'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        items = []
        for item in sorted(full_path.iterdir()):
            rel = str(item.relative_to(BASE_DATA_DIR))
            entry = {'name': item.name, 'path': rel, 'type': 'directory' if item.is_dir() else 'file'}
            if item.is_file():
                entry['size'] = item.stat().st_size
                entry['extension'] = item.suffix.lower()
            items.append(entry)

        return Response({'path': base_path, 'items': items, 'count': len(items)})

    except Exception as e:
        return Response({'error': f'Error browsing directory: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
