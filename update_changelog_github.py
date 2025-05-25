import os
import re
import sys
import glob
from datetime import datetime

github_to_real_name = {
    "Dakkarm": "A. Mio",
    "AneMarie98": "A.M. Margarit",
    "YXhi233": "Y. Huang"
}

def parse_version(version_str):
    """Converte una stringa versione in una tupla di interi."""
    return tuple(map(int, version_str.split('.')))

def increment_version(current_version, detail):
    """Incrementa la versione basandosi sul dettaglio del commit."""
    major, minor, patch = parse_version(current_version)
    
    if "Approvazione" in detail:
        return f"{major + 1}.0.0"
    elif "Redazione" in detail:
        return f"{major}.{minor + 1}.0"
    elif "Fix" in detail:
        return f"{major}.{minor}.{patch + 1}"
    else:
        return f"{major}.{minor}.{patch}"

def get_current_version_from_file(file_path):
    """Estrae la versione corrente dal file LaTeX."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    pattern = r'\\label\{Git_Action_Version\}\s*\n\s*(\d+\.\d+\.\d+)'
    match = re.search(pattern, content)
    
    if match:
        return match.group(1)
    else:
        version_pattern = r'(\d+\.\d+\.\d+)\s*&'
        match = re.search(version_pattern, content)
        if match:
            return match.group(1)
        else:
            return "0.0.0"

def format_date():
    """Restituisce la data corrente nel formato europeo (DD/MM/YYYY)."""
    return datetime.now().strftime("%d/%m/%Y")

def get_real_name(github_username):
    """Converte un nome utente GitHub nel nome reale corrispondente."""
    return github_to_real_name.get(github_username, github_username)

def find_norme_di_progetto_file(base_dir):
    """Trova il file Norme_di_progetto.tex o Norme_di_progetto_vX.Y.Z.tex."""
    base_file = os.path.join(base_dir, 'Documenti_Interni', 'Norme_di_progetto.tex')
    if os.path.exists(base_file):
        return base_file
    
    pattern = os.path.join(base_dir, 'Documenti_Interni', 'Norme_di_progetto_v*.tex')
    matching_files = glob.glob(pattern)
    
    if matching_files:
        matching_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return matching_files[0]
    
    return None

def update_changelog(file_path, commit_message, author, verificatore):
    """Aggiorna il registro delle modifiche nel file LaTeX."""
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    current_version = get_current_version_from_file(file_path)
    print(f"Versione corrente trovata: {current_version}")
    
    new_version = increment_version(current_version, commit_message)
    print(f"Nuova versione: {new_version}")
    
    real_author = get_real_name(author)
    real_verificatore = get_real_name(verificatore)
    
    new_date = format_date()
    new_row = f"    {new_version} & {new_date} & {real_author} & {real_verificatore} & {commit_message} \\\\\\ "
    
    label_pattern = r'(\\label\{Git_Action_Version\}\s*\n)'
    
    if re.search(label_pattern, content):
        new_content = re.sub(
            label_pattern,
            '\\1' + new_row + '\n    ',
            content
        )
    else:
        print("Errore: Non è stato possibile trovare il punto di inserimento nel file.")
        return False
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)
    
    print(f"Registro delle modifiche aggiornato con successo!")
    print(f"Versione: {new_version}")
    print(f"Data: {new_date}")
    print(f"Autore: {real_author}")
    print(f"Verificatore: {real_verificatore}")
    print(f"Dettaglio: {commit_message}")
    
    return True

def main():
    """Funzione principale per GitHub Actions."""

    commit_message = os.environ.get('GITHUB_COMMIT_MESSAGE', '')
    author_name = os.environ.get('GITHUB_ACTOR', '')
    verificatore = os.environ.get('GITHUB_VERIFICATORE', author_name)
    
    print(f"Commit message: {commit_message}")
    print(f"Author: {author_name}")
    print(f"Verificatore: {verificatore}")
    
    script_dir = os.environ.get('GITHUB_WORKSPACE', os.path.dirname(os.path.abspath(__file__)))
    file_path = find_norme_di_progetto_file(script_dir)
    
    if not file_path:
        print(f"Errore: Non è stato possibile trovare il file Norme_di_progetto.tex o Norme_di_progetto_vX.Y.Z.tex.")
        sys.exit(1)
    
    print(f"File trovato: {file_path}")
    
    keywords = ['Approvazione', 'Redazione', 'Fix']
    if any(keyword in commit_message for keyword in keywords):
        success = update_changelog(file_path, commit_message, author_name, verificatore)
        
        if success:
            print("\nOperazione completata con successo!")
        else:
            print("\nErrore durante l'aggiornamento del changelog.")
            sys.exit(1)
    else:
        print(f"Commit message '{commit_message}' non contiene parole chiave per l'aggiornamento del changelog.")
        print("Parole chiave supportate: Approvazione, Redazione, Fix")

if __name__ == "__main__":
    main()