import os
from layer1.models import ArtifactDescriptor, FileEntry
from layer1.detect import detect_file_type
from layer1.hashutil import sha256_file
from layer1.walk import walk_directory
from layer1.normalize import (
    artifact_id_from_path,
    create_artifact_dir,
    normalize_single_file,
    normalize_directory,
    normalize_zip
)

def ingest(path: str) -> ArtifactDescriptor:
    artifact_id = artifact_id_from_path(path)
    artifact_dir = create_artifact_dir(artifact_id)

    original_name = os.path.basename(path)
    files = []
    file_types = set()
    container = False
    disk_image = False

    if os.path.isfile(path):
        ftype = detect_file_type(path)

        if ftype == "zip":
            source_type = "archive"
            container = True
            normalize_zip(path, artifact_dir)
        elif ftype == "disk_image":
            source_type = "disk_image"
            disk_image = True
            normalize_single_file(path, artifact_dir)
        else:
            source_type = "single_file"
            normalize_single_file(path, artifact_dir)

    elif os.path.isdir(path):
        source_type = "directory"
        container = True
        normalize_directory(path, artifact_dir)

    else:
        raise ValueError("Unsupported input")

    for full, rel in walk_directory(artifact_dir):
        ftype = detect_file_type(full)
        file_types.add(ftype)

        files.append(
            FileEntry(
                path=rel,
                size=os.path.getsize(full),
                hash=sha256_file(full)
            )
        )

    return ArtifactDescriptor(
        artifact_id=artifact_id,
        source_type=source_type,
        original_name=original_name,
        normalized_path=artifact_dir,
        files=files,
        file_types=sorted(file_types),
        container=container,
        disk_image=disk_image
    )
