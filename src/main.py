from copystatic import delete_dir, copy_files_recursive
from markdown_to_html_node import generate_page, generate_page_recursive

dir_path_static = "./static"
dir_path_public = "./public"

def main():
    print("Deleting public directory...")
    delete_dir(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive("./static", "./public")

    print("Generating page...")
    generate_page_recursive("./content", "./template.html", dir_path_public)

if __name__ == "__main__":
    main()
