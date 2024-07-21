import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import os


class Base:
    def __init__(self, url):
        self.url = url
        self.exceptions = [
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
            "Description",
            "Name",
            "mailto"
        ]

    def add_exception(self, exception):
        self.exceptions.append(exception)

    def get(self, var):
        if hasattr(self, var):
            return getattr(self, var)
        else:
            return 0

    def set(self, var, value):
        if hasattr(self, var):
            setattr(self, var, value)
        else:
            print("La propiedad " + var + " no existe en la clase Persona.")

    def verify(self):
        url = self.url
        try:
            link = url
            print("Conectando con: ")
            print(link)
            response = requests.get(link, timeout=5)
            response.raise_for_status()
            print("Status: ")
            print(response.status_code)
            if 200 == response.status_code:
                print()
                return True
            else:
                print(
                    """
            
            Conexion rechazada
            
            Es posible que el sitio este en clases,
            checar VPN  
                        
            """
                )
                return False
        except requests.exceptions.RequestException as e:
            print(
                "\n No se pudo establecer la conexion con: "
                + link
                + """

        Posiblemente este el servidor apagado

"""
            )
            print()
            return False

    # Pending
    def sliceUrl(self, url):
        regex = r"/([^/]+)(?:/)?$"  # Expresión regular para capturar el último segmento de una URL
        match = re.search(regex, url)

        if match:
            return match.group(1)
        else:
            return ""

    def getType(self, url):
        tipo = type(url)
        if tipo == str:
            return [url, self.sliceUrl(url)]
        else:
            return [url.get("href"), url.text]

    def getHtml(self, online):
        url, name = self.getType(online)
        request = requests.get(url)
        html = request.text
        soup_data = BeautifulSoup(html, "html.parser")
        return soup_data

    def download(self, href):

        url, nombre = self.getType(href)

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

    def upydate(self, online_url=[]):
        if not online_url:
            return
        print(online_url[0])
        try:
            actual, mime_type = self.getType(online_url[0])
            if (
                ".zip" in mime_type
                or ".rar" in mime_type
                or ".exe" in mime_type
                or ".cvd" in mime_type
            ):
                print(actual)
                self.direct_links.update({mime_type: lambda: self.download(actual)})
            elif actual in self.exceptions:
                return
            else:
                html = self.getHtml(actual)
                tag_objects = self.getHref(html,actual)
                self.upydate(tag_objects)
        except requests.exceptions.RequestException as e:
            # Manejar cualquier excepción de solicitud
            print("Error al verificar la URL " + actual)

        # Llamar recursivamente a la función con el resto de las URLs
        self.upydate(online_url[1:])

