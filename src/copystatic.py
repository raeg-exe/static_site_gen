import os
import shutil


def delete_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def copy_files_recursive(src_dir_path, dst_dir_path):
    if not os.path.exists(dst_dir_path):
        os.mkdir(dst_dir_path)

    for name in os.listdir(src_dir_path):
        src_path = os.path.join(src_dir_path, name)
        dst_path = os.path.join(dst_dir_path, name)

        print(f" * {src_path} -> {dst_path}")

        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            copy_files_recursive(src_path, dst_path)