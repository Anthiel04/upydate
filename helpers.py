import requests
from bs4 import BeautifulSoup

exceptions = ['https://ayuda.uclv.edu.cu']

# Si el servidor responde con 200 se trabaja con ese enlace

def getUrl(url = []):
    for i in range(len(url)):
        try:
            if(200 == requests.get(url[i]).status_code):
                online_url = url[i]
        except:
            print("No se pudo establecer la conexion con: " + url[i])
            continue
        else:
            return online_url
        finally:
            print("Conectando con: " + url[i])
    print("""
          
          No se pudo establecer conexion con ningun servidor
          
          
          Tip:
            Mudate
          
          """)
    exit()
        

# Obtiene el HTML de la URL

def getHtml(online):
    request = requests.get(online)
    html = request.text
    soup_data = BeautifulSoup(html, 'html.parser')
    return soup_data

# Obtiene el url de las <a> y se deshace de los no validos

def getHref(html,actual_url):

    href = []
    links = html.find_all("a")

    for i in range(len(links)):

        link = links[i].get("href")

        # Si el enlace se encuentra en la lista de excepciones se ignora
        if(link in exceptions):
            continue
        
        # Si el enlace no contiene barras ignorarlo
        elif(link.count('/') == 0):
            continue
        
        # Si el enlace contiene al menos una barra completar enlace con la base
        elif(link.count('/') < 2):
            temp = actual_url + link
            href.append(temp)

        # Si el enlace contiene mas de 2 barras guardarlo
        else:
            href.append(link)

    return href


def typeChecker(url, contentType):
    arr = getHref(getHtml(url), url)
    files = []
    for i in range(len(arr)):
        temp = requests.get(arr[i])
        if(contentType == temp.headers.get("Content-Type")):
            files.append(arr[i])   
        else:
            continue     
    return files

def download(href):
    for i in range(len(href)):
        
        if "application/x-rar-compressed" in requests.get(href[i]).headers.get("Content-Type"):
            
            print("La respuesta de " + href[i] + "contiene un archivo RAR")
            
            print("Descargando...")

            with open("./Updates/" + href[i][-5:] + "update.rar", "wb") as file:
                file.write(requests.get(href[i].content))

            print("Descargado!!!")
            
        else:
            
            print(href[i] + """
    La respuesta no contiene un archivo RAR""")
            explored = typeChecker(href[i], "application/x-rar-compressed")
            if(range(0) != explored):
                download(explored)
                # download(getHref(getHtml(href[i]), href[i]))
            
    return 0