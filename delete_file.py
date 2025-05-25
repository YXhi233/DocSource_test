import os, sys

def delete_file(tex_file):
    fileToDelete = os.path.join("Documents", os.path.dirname(tex_file).replace('_', ' '))
    fileToDelete = os.path.join(fileToDelete, os.path.basename(tex_file).replace('.tex', '.pdf'))
    if("Verbali" not in fileToDelete):
        fileToDelete = fileToDelete.replace('_',' ')
    try:
        if os.path.exists(fileToDelete):
            os.remove(fileToDelete)
            print(f"Deleted PDF file: {fileToDelete}")
        else:
            print(f"{fileToDelete} does not exist, skipping.")

        dir = os.path.dirname(fileToDelete)
        if not os.listdir(dir):
            os.rmdir(dir)
            print(f"Directory eliminata: {dir}")
        dir = os.path.dirname(fileToDelete)
        if not os.listdir(dir):
            os.rmdir(dir)
            print(f"Directory eliminata: {dir}")

    except FileNotFoundError:
        print(f"{fileToDelete} does not exist.")
    except Exception as e:
        print(f"Error deleting {fileToDelete}: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python delete_file.py <path_to_tex_file")
    else:
        delete_file(sys.argv[1])