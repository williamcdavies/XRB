import csv
import os
import math
from pathlib import Path

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings


# Define allowed base directories for file access (security measure)
# In Docker, data is mounted at /data; locally, it's at shared/data relative to project root
ALLOWED_BASE_DIRS = [
    Path('/data'),
]


def is_path_safe(file_path: str) -> bool:
    """
    Check if the given file path is within allowed directories.
    Prevents directory traversal attacks.
    """
    try:
        resolved_path = Path(file_path).resolve()
        return any(
            resolved_path.is_relative_to(base_dir.resolve())
            for base_dir in ALLOWED_BASE_DIRS
        )
    except (ValueError, OSError):
        return False


def validate_and_convert_value(value: str, column_name: str) -> dict:
    """
    Validate and convert a string value to an appropriate type.
    Returns a dict with 'value', 'original', 'is_valid', and 'warning' keys.
    """
    result = {
        'value': None,
        'original': value,
        'is_valid': True,
        'warning': None
    }
    
    # Handle empty or whitespace-only values
    if value is None or value.strip() == '':
        result['value'] = None
        result['warning'] = 'empty_value'
        return result
    
    value = value.strip()
    
    # Handle NULL string values
    if value.upper() == 'NULL':
        result['value'] = None
        result['warning'] = 'null_value'
        return result
    
    # Handle infinity values
    if value.lower() == 'inf' or value.lower() == '+inf':
        result['value'] = None
        result['is_valid'] = False
        result['warning'] = 'positive_infinity'
        return result
    
    if value.lower() == '-inf':
        result['value'] = None
        result['is_valid'] = False
        result['warning'] = 'negative_infinity'
        return result
    
    # Handle NaN values
    if value.lower() == 'nan':
        result['value'] = None
        result['is_valid'] = False
        result['warning'] = 'not_a_number'
        return result
    
    # Handle comparison operators in values (e.g., ">6", "<7.3")
    comparison_match = None
    if value.startswith('>') or value.startswith('<'):
        comparison_match = value[0]
        numeric_part = value[1:].strip()
    else:
        numeric_part = value
    
    # Try to convert to number
    try:
        # Try integer first
        if '.' not in numeric_part and 'e' not in numeric_part.lower():
            result['value'] = int(numeric_part)
        else:
            # Try float (handles scientific notation)
            float_val = float(numeric_part)
            
            # Check for infinity after conversion
            if math.isinf(float_val):
                result['value'] = None
                result['is_valid'] = False
                result['warning'] = 'infinity_after_conversion'
                return result
            
            # Check for NaN after conversion
            if math.isnan(float_val):
                result['value'] = None
                result['is_valid'] = False
                result['warning'] = 'nan_after_conversion'
                return result
            
            result['value'] = float_val
        
        # Add comparison operator warning if present
        if comparison_match:
            result['warning'] = f'comparison_operator_{comparison_match}'
            result['original_with_operator'] = value
            
    except ValueError:
        # Keep as string if not a number
        result['value'] = value
    
    return result


def csv_to_json(file_path: str, include_metadata: bool = True) -> dict:
    """
    Convert a CSV file to JSON format.
    First row is treated as column headers.
    Includes data validation and cleaning.
    """
    data = []
    columns = []
    warnings = []
    row_count = 0
    
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        # Use csv.reader to properly handle quoted fields
        reader = csv.reader(csvfile)
        
        # First row contains column headers
        try:
            columns = next(reader)
            columns = [col.strip() for col in columns]
        except StopIteration:
            return {
                'success': False,
                'error': 'Empty CSV file',
                'data': [],
                'columns': [],
            }
        
        # Process data rows
        for row_idx, row in enumerate(reader, start=2):  # Start at 2 (1-indexed, after header)
            row_count += 1
            
            # Check for row length mismatch
            if len(row) != len(columns):
                warnings.append({
                    'row': row_idx,
                    'type': 'column_count_mismatch',
                    'message': f'Row {row_idx} has {len(row)} columns, expected {len(columns)}'
                })
                # Pad or truncate row to match columns
                if len(row) < len(columns):
                    row.extend([''] * (len(columns) - len(row)))
                else:
                    row = row[:len(columns)]
            
            row_data = {}
            for col_idx, (col_name, value) in enumerate(zip(columns, row)):
                validated = validate_and_convert_value(value, col_name)
                row_data[col_name] = validated['value']
                
                # Track warnings for problematic values
                if validated['warning'] and validated['warning'] not in ['empty_value', 'null_value']:
                    warnings.append({
                        'row': row_idx,
                        'column': col_name,
                        'type': validated['warning'],
                        'original_value': validated['original'],
                        'converted_value': validated['value']
                    })
            
            data.append(row_data)
    
    result = {
        'success': True,
        'data': data,
        'columns': columns,
    }
    
    if include_metadata:
        result['metadata'] = {
            'row_count': row_count,
            'column_count': len(columns),
            'warnings': warnings,
            'warning_count': len(warnings),
            'file_path': file_path,
        }
    
    return result


def get_column_stats(data: list, columns: list) -> dict:
    """
    Calculate basic statistics for numeric columns.
    """
    stats = {}
    
    for col in columns:
        values = [row.get(col) for row in data if row.get(col) is not None]
        numeric_values = [v for v in values if isinstance(v, (int, float))]
        
        col_stats = {
            'total_count': len(data),
            'non_null_count': len(values),
            'null_count': len(data) - len(values),
            'is_numeric': len(numeric_values) == len(values) and len(values) > 0,
        }
        
        if col_stats['is_numeric'] and numeric_values:
            col_stats['min'] = min(numeric_values)
            col_stats['max'] = max(numeric_values)
            col_stats['mean'] = sum(numeric_values) / len(numeric_values)
        
        stats[col] = col_stats
    
    return stats


@api_view(['GET'])
@permission_classes([AllowAny])
def get_file_data(request):
    """
    Retrieve file data and return as JSON.
    
    Query parameters:
        - path: Relative path to file within allowed directories (e.g., "clean_data/lrlx_data_BH_CLEAN.csv")
        - include_stats: Include column statistics (default: false)
        - include_metadata: Include file metadata and warnings (default: true)
    """
    relative_path = request.query_params.get('path')
    include_stats = request.query_params.get('include_stats', 'false').lower() == 'true'
    include_metadata = request.query_params.get('include_metadata', 'true').lower() == 'true'
    
    if not relative_path:
        return Response(
            {'error': 'Missing required parameter: path'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Build full file path from relative path
    # Look in allowed directories for the file
    file_path = None
    for base_dir in ALLOWED_BASE_DIRS:
        potential_path = base_dir / relative_path
        if potential_path.exists():
            file_path = potential_path
            break
    
    if file_path is None:
        return Response(
            {'error': f'File not found: {relative_path}'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Validate file path is safe
    if not is_path_safe(str(file_path)):
        return Response(
            {'error': 'Access denied: Path is outside allowed directories'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Check file extension and process accordingly
    file_extension = file_path.suffix.lower()
    
    try:
        if file_extension == '.csv':
            result = csv_to_json(str(file_path), include_metadata=include_metadata)
            
            if not result['success']:
                return Response(
                    {'error': result.get('error', 'Failed to parse CSV file')},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Add column statistics if requested
            if include_stats:
                result['column_stats'] = get_column_stats(result['data'], result['columns'])
            
            return Response(result)
        
        elif file_extension == '.json':
            import json
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Try to extract columns if it's a list of dicts
            columns = []
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                columns = list(data[0].keys())
            
            result = {
                'success': True,
                'data': data,
                'columns': columns,
            }
            
            if include_metadata:
                result['metadata'] = {
                    'row_count': len(data) if isinstance(data, list) else 1,
                    'column_count': len(columns),
                    'file_path': str(file_path),
                }
            
            return Response(result)
        
        else:
            return Response(
                {'error': f'Unsupported file format: {file_extension}. Supported formats: .csv, .json'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    except FileNotFoundError:
        return Response(
            {'error': f'File not found: {relative_path}'},
            status=status.HTTP_404_NOT_FOUND
        )
    except PermissionError:
        return Response(
            {'error': 'Permission denied when reading file'},
            status=status.HTTP_403_FORBIDDEN
        )
    except Exception as e:
        return Response(
            {'error': f'Error processing file: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
