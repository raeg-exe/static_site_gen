from copystatic import delete_dir, copy_files_recursive
from markdown_to_html_node import generate_page_recursive
import sys

dir_path_static = "./static"
dir_path_public = "./docs"

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    print("Deleting public directory...")
    delete_dir(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive("./static", dir_path_public)

    print("Generating page...")
    generate_page_recursive("./content", "./template.html", dir_path_public, basepath)

if __name__ == "__main__":
    main()
