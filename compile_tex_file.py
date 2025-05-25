import os, sys, subprocess

def compile_tex(tex_file):
    output_dir = os.path.join("Documents", os.path.dirname(tex_file))
    output_dir = output_dir.replace("_", " ")

    print(f"output: {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    command = [
        'latexmk', '-pdf', '-output-directory=' + output_dir, tex_file
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print(f"Error compiling file {tex_file}")
    
    clean_command = [
        'latexmk', '-c', '-output-directory=' + output_dir, tex_file
    ]
    try:
        subprocess.run(clean_command, check=True)
        
    except subprocess.CalledProcessError:
        print(f"Error clean file {tex_file}")

    oldPdf = os.path.join(output_dir, os.path.basename(tex_file).replace('.tex','.pdf'))
    if("Verbali" not in output_dir):
        newPDF = oldPdf.replace('_',' ')
        os.rename(oldPdf, newPDF)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python compile_tex_file.py <path_to_tex_file>")
    else:
        if not os.path.isfile(sys.argv[1]):
            print(f"File {sys.argv[1]} does not exist.")
        else:
            print(" - Compiling LaTeX file:", sys.argv[1])
            compile_tex(sys.argv[1])