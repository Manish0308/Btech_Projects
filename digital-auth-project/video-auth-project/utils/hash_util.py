import hashlib

def generate_hash(file_path, block_size=65536):
    """
    Generates SHA-256 hash of a given video file.

    Args:
        file_path (str): Path to the video file.
        block_size (int): Size of chunks read at a time.

    Returns:
        str: Hexadecimal SHA-256 hash string.
    """
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(block_size):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        return f"Error generating hash: {e}"
