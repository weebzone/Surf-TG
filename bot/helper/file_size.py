SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


def get_readable_file_size(size_in_bytes: int | str):
    if isinstance(size_in_bytes, str):
        size_in_bytes = int(size_in_bytes)
    if not size_in_bytes:
        return '0B'
    index = 0
    while size_in_bytes >= 1024 and index < len(SIZE_UNITS) - 1:
        size_in_bytes /= 1024
        index += 1
    return f'{size_in_bytes:.2f}{SIZE_UNITS[index]}' if index > 0 else f'{size_in_bytes:.2f}B'
