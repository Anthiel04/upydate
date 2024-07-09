import base
import requests
from bs4 import BeautifulSoup


# Check!!!!!!!!!!!!
class UIJ(base.Base):
    def __init__(self, url):
        super().__init__(url)
        self.filetypes = [".rar", ".exe", ".cvd"]
        self.status = self.verify()
        if self.status == True:
            print(self.url + " => Online ")
            self.direct_links = {}
            self.upydate([self.url])
        else:
            self.direct_links = "Offline"

    def upydate(self, online_url=[]):
        if not online_url:
            return

        try:
            actual, mime_type = self.getType(online_url[0])
            if (
                ".zip" in mime_type
                or ".rar" in mime_type
                or ".exe" in mime_type
                or ".cvd" in mime_type
            ):
                self.direct_links.update({mime_type: lambda: self.download(actual)})
                return 0
            else:
                html = self.getHtml(actual)
                tag_objects = self.getHref(html)
                self.upydate(tag_objects)
        except requests.exceptions.RequestException as e:
            # Manejar cualquier excepción de solicitud
            print("Error al verificar la URL " + actual)

        # Llamar recursivamente a la función con el resto de las URLs
        self.upydate(online_url[1:])

    # Obtiene el url de las <a> y se deshace de los no validos
    def getHref(self, html):

        href = []
        links = html.find_all("a")

        for i in range(len(links)):
            link = links[i].get("href")

            # Si el enlace se encuentra en la lista de excepciones se ignora
            # Si el enlace no contiene barras ignorarlo
            if (
                link in self.exceptions
                or links[i].text in self.exceptions
                or links[i] in href
            ):
                continue

            # Si el enlace no contiene http completar con la base
            elif "http" not in link:
                if link[0] == "/":
                    link = link[1:]
                temp = self.url + link
                link = temp
            links[i]["href"] = link
            href.append(links[i])
        return href
