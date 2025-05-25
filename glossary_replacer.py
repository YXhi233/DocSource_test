import os
import re
import glob

def extract_glossary_terms(glossary_file):
    """Estrae i termini dal glossario."""
    terms = []
    with open(glossary_file, 'r', encoding='utf-8') as file:
        content = file.read()

        pattern = r'\\textbf{([^}]+)}'
        matches = re.findall(pattern, content)
        for match in matches:

            term = match.strip()
            if term:
                terms.append(term)
    return terms

def replace_terms_in_file(file_path, terms):
    """Sostituisce i termini nel file con il formato richiesto."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    sorted_terms = sorted(terms, key=len, reverse=True)
    
    for term in sorted_terms:
        pattern = r'(?<!\\textit{)(?<!\\text)(?<!\w)' + re.escape(term) + r'(?!\w)(?!}\\textsubscript)'
        replacement = r'\\textit{' + term + r'}\\textsubscript{\\textit{G}}'
        content = re.sub(pattern, replacement, content)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    return True

def process_tex_files(directory, glossary_file):
    """Processa tutti i file .tex nella directory e nelle sottodirectory."""

    glossary_terms = extract_glossary_terms(glossary_file)
    print(f"Trovati {len(glossary_terms)} termini nel glossario.")
    
    tex_files = glob.glob(os.path.join(directory, '**', '*.tex'), recursive=True)
    
    tex_files = [f for f in tex_files if os.path.abspath(f) != os.path.abspath(glossary_file)]
    
    print(f"Trovati {len(tex_files)} file .tex da processare.")
    
    for file_path in tex_files:
        print(f"Elaborazione del file: {file_path}")
        replace_terms_in_file(file_path, glossary_terms)
    
    print("Elaborazione completata.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    glossary_file = os.path.join(base_dir, 'Documenti_Interni', 'Glossario_v1.0.0.tex')
    docs_dir = os.path.join(base_dir, 'Documenti_Interni')
    
    process_tex_files(docs_dir, glossary_file)