from copystatic import delete_dir, copy_files_recursive

dir_path_static = "./static"
dir_path_public = "./public"

def main():
    print("Deleting public directory...")
    delete_dir(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive("./static", "./public")

if __name__ == "__main__":
    main()
