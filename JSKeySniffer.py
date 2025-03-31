import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pyfiglet
from termcolor import colored

PATTERNS = {
    "Google API Key": r'AIza[0-9A-Za-z\-_]{35}',
    "AWS Access Key": r'AKIA[0-9A-Z]{16}',
    "AWS Secret Key": r'(?i)aws[_-]?secret[_-]?access[_-]?key\s*[:=]\s*["\']?([A-Za-z0-9+/=]{40})["\']?',
    "JWT Token": r'eyJ[a-zA-Z0-9]{10,}\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+',
    "Access Token": r'(?i)access[_-]?token\s*[:=]\s*["\']?([\w\-]{10,})["\']?',
    "Secret Key": r'(?i)secret[_-]?key\s*[:=]\s*["\']?([\w\-]{10,})["\']?',
    "Internal URL": r'https?://(dev|staging|internal|localhost|192\\.168|10\\.)[\w\.\-/:]+'
}

def fetch_js_files(url):
    """Obtiene la lista de archivos .js desde el HTML del sitio."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        scripts = [urljoin(url, script["src"]) for script in soup.find_all("script", src=True) if script["src"].endswith(".js")]
        return scripts
    except requests.RequestException as e:
        print(colored(f"[ERROR] No se pudo acceder a {url}: {e}", "red"))
        return []

def analyze_js(content):
    """Analiza el contenido de un archivo .js en busca de información sensible."""
    found_data = {}
    for label, pattern in PATTERNS.items():
        matches = re.findall(pattern, content)
        if matches:
            found_data[label] = set(matches)  # Eliminar duplicados
    return found_data if found_data else None

def scan_url(target_url):
    js_files = fetch_js_files(target_url)

    if not js_files:
        print(colored("[INFO] No se encontraron archivos JavaScript.", "yellow"))
        return

    print(colored(f"\n[INFO] Analizando {len(js_files)} archivos JS...", "blue"))
    all_results = {}

    for js_file in js_files:
        print(colored(f"\n🔍 Escaneando: {js_file}", "magenta"))
        try:
            response = requests.get(js_file, timeout=10)
            response.raise_for_status()
            results = analyze_js(response.text)
        except requests.RequestException:
            results = None

        if results:
            for category, values in results.items():
                all_results.setdefault(category, set()).update(values)
                print(colored(f"  📌 {category}:", "green"))
                for value in values:
                    print(colored(f"    ➞ {value}", "yellow"))
        else:
            print(colored("  ❌ No se encontró información sensible.", "red"))

    print(colored("\n💛 Resumen de datos sensibles encontrados:", "cyan"))
    print(colored("--------------------------------------------------", "cyan"))
    for category, values in all_results.items():
        print(colored(f"  📌 {category}:", "green"))
        for value in values:
            print(colored(f"    ➞ {value}", "yellow"))
    print(colored("--------------------------------------------------\n", "cyan"))

def scan_file():
    file_path = input(colored("Ingrese la ruta del archivo .js: ", "cyan")).strip()
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            results = analyze_js(content)
            if results:
                print(colored("\n💛 Datos sensibles encontrados:", "cyan"))
                print(colored("--------------------------------------------------", "cyan"))
                for category, values in results.items():
                    print(colored(f"  📌 {category}:", "green"))
                    for value in values:
                        print(colored(f"    ➞ {value}", "yellow"))
                print(colored("--------------------------------------------------\n", "cyan"))
            else:
                print(colored("  ❌ No se encontró información sensible.", "red"))
    except FileNotFoundError:
        print(colored("[ERROR] No se pudo encontrar el archivo.", "red"))
    except Exception as e:
        print(colored(f"[ERROR] Ocurrió un problema: {e}", "red"))

def scan_from_list():
    file_path = input(colored("Ingrese la ruta del archivo de targets (.txt): ", "cyan")).strip()
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            targets = file.read().splitlines()
            for target in targets:
                print(colored(f"\n🌐 Escaneando {target}...", "blue"))
                scan_url(target)
    except FileNotFoundError:
        print(colored("[ERROR] No se pudo encontrar el archivo de targets.", "red"))
    except Exception as e:
        print(colored(f"[ERROR] Ocurrió un problema: {e}", "red"))

def main():
    print(colored(pyfiglet.figlet_format("JSKeySniffer"), "blue"))
    print(colored("Created by Stealthy\n", "cyan"))
    print(colored("Seleccione un modo de escaneo:", "blue"))
    print(colored("1. Escanear por URL", "green"))
    print(colored("2. Escanear un archivo .js local", "green"))
    print(colored("3. Escanear desde un listado de URLs en un .txt", "green"))
    choice = input(colored("Ingrese la opción (1/2/3): ", "cyan")).strip()
    if choice == "1":
        target_url = input(colored("Ingrese la URL objetivo: ", "cyan")).strip()
        scan_url(target_url)
    elif choice == "2":
        scan_file()
    elif choice == "3":
        scan_from_list()
    else:
        print(colored("[ERROR] Opción no válida.", "red"))

if __name__ == "__main__":
    main()
