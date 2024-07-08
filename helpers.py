import requests
from bs4 import BeautifulSoup
import re
import os
import time
from tqdm import tqdm

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


# Descarga el contenido del URL
# OK
def download(href):

    url, nombre = getType(href)

    print("Descargando " + nombre + " ...")

    directory = "./Updates/"

    if not os.path.exists(directory):
        os.makedirs(directory)

    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024
    with tqdm(total=total_size, unit="iB", unit_scale=True) as progress_bar:
        with open(directory + nombre, "wb") as file:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    file.write(chunk)
                    progress_bar.update(len(chunk))

    print(nombre + " descargado!!!")


def upydate(online_url=[], count=0):

    if not online_url:
        return

    try:
        actual, mime_type = getType(online_url[0])
        print(mime_type)

        if ".rar" in mime_type or ".exe" in mime_type or ".cvd" in mime_type:
            download(online_url[0])
        else:
            # print("HTML!!")
            html = getHtml(actual)
            tag_objects = getHref(html, actual)
            upydate(tag_objects)
    except requests.exceptions.RequestException as e:
        # Manejar cualquier excepción de solicitud
        print("Error al verificar la URL " + actual)

    # Llamar recursivamente a la función con el resto de las URLs
    upydate(online_url[1:], count + 1)
