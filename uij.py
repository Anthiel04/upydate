import base

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

    # Obtiene el url de las <a> y se deshace de los no validos
    def getHref(self, html, actual):

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
