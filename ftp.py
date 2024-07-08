import base
import helpers
import requests
from bs4 import BeautifulSoup
import re
import os
import time
from tqdm import tqdm


class FTP(base.Base):
    def __init__(self, url):
        super().__init__(url)
        if self.verify():
            self.status = bool(1)
            print(self.url + " => Online ")
            direct_links = self.upydate([self.url])

    def upydate(self, online_url=[]):
        if not online_url:
            return

        try:
            actual, mime_type = self.getType(online_url[0])
            print(mime_type)

            if ".rar" in mime_type or ".exe" in mime_type or ".cvd" in mime_type:
                return {mime_type: actual}
            else:
                # print("HTML!!")
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
                temp = "http://ftp.uo.edu.cu" + link
                link = temp
            links[i]["href"] = link
            href.append(links[i])
        print(href)
        return href
