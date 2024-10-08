import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def verificar_subdominio(subdominio):
    try:
        resultado = subprocess.run(['dig', '+short', subdominio], capture_output=True, text=True)
        if resultado.stdout.strip():  
            return subdominio
        return None
    except Exception as e:
        print(f"Error al verificar {subdominio}: {e}")
        return None

def obtener_subdominios(dominio, wordlist):
    subdominios_encontrados = []
    subdominios = []

    with open(wordlist, 'r') as f:
        subdominios = f.read().splitlines()

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(verificar_subdominio, f"{sub}.{dominio}"): sub for sub in subdominios}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Verificando subdominios"):
            resultado = future.result()
            if resultado:
                subdominios_encontrados.append(resultado)

    return subdominios_encontrados

if __name__ == '__main__':
    dominio = input("Introduce un dominio (ejemplo: google.com): ")
    subdominios = obtener_subdominios(dominio, 'subdomains.txt')
    
    if subdominios:
        print("Subdominios encontrados:")
        for sub in subdominios:
            print(sub)
    else:
        print("No se encontraron subdominios.")

