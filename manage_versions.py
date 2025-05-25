import os, sys, re

def get_version(fileName):
    with open(fileName, 'r') as file:
        data = file.read()
        match = re.findall(r'{}(.*?){}'.format("label{Git_Action_Version}", "&"), data, re.DOTALL)
        file.close
        return match[0] if match else ''
    
def manage_version(file):
    version = get_version(file)
    version=version.replace('\n', '').replace('\r','').strip()
    if not version:
        raise ValueError("No version found.")
    base, ext = os.path.splitext(file) 
    version_pattern = re.compile(r'_v\d+\.\d+\.\d+$')
    if version_pattern.search(base) and version_pattern.search(base)[0] == f"_v{version}":
        return None
    base = version_pattern.sub('', base)
    newFile = f"{base}_v{version}{ext}"
    os.rename(file, newFile)

    return newFile
    
def main():
    if ".tex" not in sys.argv[1]:
        print("Usage: python delete_file.py <path_to_tex_file")
    else:
        tex_file = sys.argv[1]
        oldPdf = os.path.join('Documents', tex_file.replace('.tex', '.pdf'))
        if("Verbali" not in oldPdf):
            oldPdf = oldPdf.replace('_', ' ')
        newFile = manage_version(tex_file)

        if newFile and os.path.exists(oldPdf):
            try:
                os.remove(oldPdf)
            except FileNotFoundError:
                print(f"{oldPdf} does not exist.")
            except Exception as e:
                print(f"Error deleting {oldPdf}: {e}")
        if newFile: 
            print(newFile)
        else:
            print("No update needed")

if __name__=="__main__":
    main()