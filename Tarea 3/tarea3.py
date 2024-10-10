import dns.resolver
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def verificar_subdominio(subdominio):
    try:
        respuestas = dns.resolver.resolve(subdominio, 'A')
        if respuestas:
            return subdominio
    except dns.resolver.NXDOMAIN:
        return None
    except dns.resolver.NoAnswer:
        return None
    except dns.resolver.Timeout:
        return None
    except Exception as e:
        print(f"Error al verificar {subdominio}: {e}")
        return None

def obtener_subdominios(dominio, wordlist):
    subdominios_encontrados = []
    subdominios = []

    try:
        with open(wordlist, 'r') as f:
            subdominios = f.read().splitlines()
    except FileNotFoundError:
        print(f"El archivo {wordlist} no se encontró.")
        return subdominios_encontrados

    with ThreadPoolExecutor(max_workers=50) as executor: 
        futures = {executor.submit(verificar_subdominio, f"{sub}.{dominio}"): sub for sub in subdominios}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Verificando subdominios"):
            resultado = future.result()
            if resultado:
                subdominios_encontrados.append(resultado)

    return subdominios_encontrados

if __name__ == '__main__':
    dominio = input("Introduce un dominio: ").strip()
    subdominios = obtener_subdominios(dominio, 'subdomains.txt')
    
    if subdominios:
        print("Subdominios encontrados:")
        for sub in subdominios:
            print(sub)
    else:
        print("No se encontraron subdominios.")
