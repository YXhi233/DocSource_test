import os
import sys
import subprocess


def check_chktex(tex_file):
    print("Checking with ChkTeX...")
    if not os.path.exists(tex_file):
        print(f"File {tex_file} not found.")
        sys.exit(1)
    command = ["chktex", "-q", "-n1","-n8","-n12","-n13","-n18","-n24","-n26","-n36","-n44", tex_file]
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("ChkTeX found issues.")
        
    print("No ChkTeX issues found.")

def check_aspell(tex_file):
    print("Checking spelling with aspell...")
    personal_dict = "dictionary.pws"
    command = ["aspell", "list","--lang=it","--mode=tex","--encoding=utf-8","--dont-ignore-accents",f"--personal={personal_dict}"] 
    if not os.path.exists(personal_dict):
        print(f"Personal dictionary {personal_dict} not found. Proceeding without it.")
    with open(tex_file, "r", encoding="utf-8") as f:
        print("Reading file...")
        text = f.read()
        print("Checking spelling...")
        result = subprocess.run(command, input=text, capture_output=True, text=True)
    if result.stdout.strip():
        print("Possible spelling mistakes found:")
        print(result.stdout)
        
    print("No spelling mistakes found.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python controllo_ortografia.py <path_to_tex_file>")
        sys.exit(1)
    tex_file = sys.argv[1]
    print(f"============Checking file: {tex_file}==================")
    check_chktex(tex_file)
    check_aspell(tex_file)