import requests
from bs4 import BeautifulSoup
import re
import os
import time
from tqdm import tqdm
import rarfile
import shutil

exceptions = [
    "https://ayuda.uclv.edu.cu",
    "Parent Directory",
    "http://browsehappy.com",
    "https://larsjung.de/h5ai/",
    "?C=N;O=D",
    "?C=M;O=A",
    "?C=S;O=A",
    "/..",
    "..",
    "",
    "avira",
    "clamav",
    "avast",
    "segurmatica",
    "update_all/",
    "update_all_v10_to_v17/",
    "Nod32_v10_to_v17.rar"
]

filetypes = [".rar", ".exe", ".cvd"]


# Reintenta cada 10 min 6 veces
def connect(URLs):
    for i in range(6):
        online_url = getUrl(URLs)
        if online_url != "":
            return online_url
        time.sleep(600)


# Pending
def sliceUrl(url):
    regex = r"/([^/]+)(?:/)?$"  # Expresión regular para capturar el último segmento de una URL
    match = re.search(regex, url)

    if match:
        return match.group(1)
    else:
        return ""


# Determina si es una tag o una url
def getType(url):
    tipo = type(url)
    if tipo == str:
        return [url, sliceUrl(url)]
    else:
        return [url.get("href"), url.text]


# Si el servidor responde con 200 se trabaja con ese enlace
# OK
def getUrl(url):
    for i in range(len(url)):
        try:
            link = url[i]
            print("Conectando con: " + link)
            print()

            response = requests.get(link, timeout=5)
            response.raise_for_status()

            # print(response.status_code)
            # print()

            if 200 == response.status_code:
                print(link + " esta online")
                print()
                return link
            else:
                print(
                    """
                
                Conexion rechazada
                
                Es posible que el sitio este en clases,
                checar VPN  
                            
                """
                )
        except requests.exceptions.RequestException as e:
            print(
                "No se pudo establecer la conexion con: "
                + link
                + """

        Posiblemente este el servidor apagado

"""
            )
            print()
            continue

    print(
        """
    No se pudo establecer conexion con ningun servidor       
        Tip:
            Mudate

"""
    )
    exit()


# Obtiene el HTML de la URL
# OK
def getHtml(online):
    url, name = getType(online)
    request = requests.get(url)
    html = request.text
    soup_data = BeautifulSoup(html, "html.parser")
    return soup_data


# Obtiene el url de las <a> y se deshace de los no validos
# Optimizar, ajustar y la madre de los tomates
def getHref(html, actual_url):

    href = []
    links = html.find_all("a")

    for i in range(len(links)):
        link = links[i].get("href")

        # Si el enlace se encuentra en la lista de excepciones se ignora
        # Si el enlace no contiene barras ignorarlo
        if link in exceptions or links[i].text in exceptions or links[i] in href:
            continue

            # Si el enlace no contiene http completar con la base
        elif "http" not in link:
            if link[0] == "/":
                link = link[1:]
            temp = actual_url + link
            link = temp
        links[i]["href"] = link
        href.append(links[i])
    print(href)
    return href

# Función para limpiar la carpeta de destino
def clear_directory(directory):
    if os.path.exists(directory):
        # Eliminar todo el contenido de la carpeta
        shutil.rmtree(directory)
    # Crear la carpeta de nuevo
    os.makedirs(directory)

# Limpiar la carpeta de destino
# Funcion para descomprimir
def unrar(rar):

    # Ruta donde descomprimir
    extract_path = "./Updates/Files"
    print("Se va a extraer en: " + extract_path)
    clear_directory(extract_path)
    # Abrir el archivo .rar
    with rarfile.RarFile(rar) as rf:
        # Descomprimir todo el contenido
        rf.extractall(path=extract_path)
    


# Descarga el contenido del URL
# OK
def download(href):
    # Desestructurando el enlace en nombre de archivo y url
    url, archivo = getType(href)
    print("Descargando " + archivo + " ...")
    # Directorio de descargas, si no existe se crea
    directory = "./Updates/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    resume_header = {}
    # Comprobando que el archivo a descargar existe para reanudar la descarga
    file_path = os.path.join(directory, "Nod32")
    block_size = 1024
    if os.path.exists(file_path):
        resume_header["Range"] = f"bytes={os.path.getsize(file_path)}-"
        print("Reanudando...")
        response = requests.get(url, headers=resume_header, stream=True)
        total_size = int(response.headers.get("content-length", 0)) + os.path.getsize(
            file_path
        )
        with tqdm(
            total=total_size,
            initial=os.path.getsize(file_path),
            unit="iB",
            unit_scale=True,
        ) as progress_bar:
            mode = (
                "ab" if os.path.exists(directory + "Nod32") else "wb"
            )  # Append o Write
            with open(file_path, "ab") as file:
                for chunk in response.iter_content(chunk_size=block_size):
                    file.write(chunk)
                    progress_bar.update(len(chunk))
        print(archivo + " descargado!!!")
        unrar(file_path)
        return

    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    with tqdm(total=total_size, unit="iB", unit_scale=True) as progress_bar:
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=block_size):
                file.write(chunk)
                progress_bar.update(len(chunk))
    print(archivo + " descargado!!!")
    unrar(file_path)
    return


def upydate(online_url=[]):

    if not online_url:
        return

    try:
        actual, mime_type = getType(online_url[0])
        print(mime_type)
        found = False
        for exception in exceptions:
            if exception == online_url[0]:
                found = True
                break
        if ".rar" in mime_type or "zip" in mime_type:
            download(online_url[0])
            return 0
        else:
            # print("HTML!!")
            html = getHtml(actual)
            tag_objects = getHref(html, actual)
            upydate(tag_objects)
    except requests.exceptions.RequestException as e:
        # Manejar cualquier excepción de solicitud
        print("Error al verificar la URL " + actual)

    # Llamar recursivamente a la función con el resto de las URLs
    upydate(online_url[1:])
