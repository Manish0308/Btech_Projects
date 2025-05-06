import hashlib

def generate_file_hash(file_path):
    """
    Generate SHA-256 hash of a file.
    """
    hash_func = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def compare_hashes(path1, path2):
    """
    Compare the hashes of two files.
    Returns a dictionary with hash values and whether they are identical.
    """
    hash1 = generate_file_hash(path1)
    hash2 = generate_file_hash(path2)
    return {
        "file1_hash": hash1,
        "file2_hash": hash2,
        "is_identical": hash1 == hash2
    }

def compute_hash(file_path):
    """
    Compute and return the hash for a given file path.
    This function provides the same result as `generate_file_hash`
    but can be used in different contexts where only the hash is needed.
    """
    return generate_file_hash(file_path)
