import os, shutil, sys, pathlib, json

pythonnDir = os.path.join(pathlib.Path(sys.executable).parent, "Lib", "site-packages")

def add_init_files(folder):
    for root, dirs, files in os.walk(folder):
        init_file = os.path.join(root, "__init__.py")
        if not os.path.exists(init_file):
            open(init_file, "w", encoding="utf-8").close()

def copy_python_files(src_dir, dst_dir):
    for root, dirs, files in os.walk(src_dir):
        relative_path = os.path.relpath(root, src_dir)
        target_root = os.path.join(dst_dir, relative_path)
        os.makedirs(target_root, exist_ok=True)

        for file in files:
            if file.endswith(".py"):
                shutil.copy(os.path.join(root, file), os.path.join(target_root, file))

def copy_library(directory):
    
    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        print(f"Library directory doesn't exist: {directory}")
        sys.exit(1)

    setup_path = os.path.join(directory, "setup.json")
    if not os.path.isfile(setup_path):
        print(f"setup.json not found in {directory}")
        sys.exit(1)

    with open(setup_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    pythonDir = data.get("python", pythonnDir)
    name = data.get("name", "unnamed_pkg")
    entryPoint = os.path.join(directory, data.get("entry", ""))

    if not os.path.isfile(entryPoint):
        print("Entry point file not found")
        sys.exit(1)

    pkg_path = os.path.join(pythonDir, name)
    os.makedirs(pkg_path, exist_ok=True)

    shutil.copy(entryPoint, os.path.join(pkg_path, "__entry__.py"))

    copy_python_files(directory, pkg_path)

    add_init_files(pkg_path)

    print(f"Library '{name}' copied to site-packages successfully.")

def main(argv):
    if len(argv) < 2:
        print("Usage: python copy_lib.py <library_folder>")
        return
    library = argv[1]
    copy_library(os.path.join(os.getcwd(), library))

if __name__ == "__main__":
    main(sys.argv)
