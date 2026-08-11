import os

ALLOWED_EXTENSIONS = {"py", "java"}


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def get_extension(filename):

    return os.path.splitext(filename)[1].lower()