import csv
import math
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

BASE_DATA_DIR = Path('/data')

def is_path_safe(file_path: str) -> bool:
    # check if path is relative to base directory
    try:
        resolved = Path(file_path).resolve()
        return resolved.is_relative_to(BASE_DATA_DIR.resolve())
    except (ValueError, OSError):
        return False


# used to detect and validate erroneous csv values
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
        # check if decimal or scientific notation
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
def get_file(request):
    """
    any user can attempt to get file data

    query parameters:
    -----------------
    path : str (required)
        Relative path under /data.  The first directory component determines
        access control:
            public/
            users/<username>/
            groups/<group>/
    """
    relative_path = request.query_params.get('path')

    # check if path has been provided
    if not relative_path:
        return Response(
            {'error': 'Missing required parameter: path'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # check if authenticated for requested path
    user = request.user if request.user.is_authenticated else None
    allowed, reason = check_path_access(user, relative_path)
    if not allowed:
        return Response(
            {'error': f'Access denied: {reason}'},
            status=status.HTTP_403_FORBIDDEN,
        )

    # append provided path to base data directory
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

    if file_path.suffix.lower() not in ['.csv', '.xlsx']:
        return Response(
            {'error': 'Unsupported file format. Only .csv, .xlsx is supported.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # TODO add xlsx conversion
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            csv_content = f.read()
        return Response(csv_content, content_type='text/csv')
    except FileNotFoundError:
        return Response({'error': f'File not found: {relative_path}'}, status=status.HTTP_404_NOT_FOUND)
    except PermissionError:
        return Response({'error': 'Permission denied when reading file'}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        return Response({'error': f'Error processing file: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

    # check if form data is provided
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    target_dir = request.data.get('path', '').strip('/')
    if not target_dir:
        return Response(
            {'error': 'Missing required parameter: path (target directory)'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # check permissions
    allowed, reason = check_write_access(request.user, target_dir)
    if not allowed:
        return Response(
            {'error': f'Upload denied: {reason}'},
            status=status.HTTP_403_FORBIDDEN,
        )

    uploaded_file = request.FILES['file']

    try:
        # append target directory to base data directory
        upload_dir = BASE_DATA_DIR / target_dir
        upload_dir.mkdir(parents=True, exist_ok=True)

        # sanitize filename and add to upload directory
        safe_name = uploaded_file.name.replace(' ', '_').replace('/', '_').replace('\\', '_')
        file_path = upload_dir / safe_name

        # write file in chunks
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

    # check permissions
    user = request.user if request.user.is_authenticated else None
    if base_path:
        allowed, reason = check_path_access(user, base_path)
        if not allowed:
            return Response({'error': f'Access denied: {reason}'}, status=status.HTTP_403_FORBIDDEN)

    # when no path provided, return all possible top-level paths the user can access
    if not base_path:
        items = [{'name': 'public', 'path': 'public', 'type': 'directory'}]
        if user and user.is_authenticated:
            items.append({
                'name': user.username,
                'path': f'users/{user.username}',
                'type': 'directory',
            })
        return Response({'path': '', 'items': items, 'count': len(items)})

    full_path = BASE_DATA_DIR / base_path

    if not is_path_safe(str(full_path)):
        return Response({'error': 'Access denied: path outside allowed directories'}, status=status.HTTP_403_FORBIDDEN)

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