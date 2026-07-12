"""
file_handler.py

This module validates uploaded files.
Only Python (.py) and Java (.java) files are allowed.
"""

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    "py",
    "java"
}


def allowed_file(filename):
    """
    Check whether the uploaded file has an allowed extension.

    Parameters:
        filename (str): Name of uploaded file

    Returns:
        bool:
            True  -> Allowed
            False -> Not Allowed
    """

    # File must contain a dot
    if "." not in filename:
        return False

    # Extract extension
    extension = filename.rsplit(".", 1)[1].lower()

    # Check extension
    return extension in ALLOWED_EXTENSIONS