import requests
from bs4 import BeautifulSoup
import re


exceptions = ['https://ayuda.uclv.edu.cu',"Parent Directory",'','=', "?C=N;O=D", "?C=M;O=A","?C=S;O=A"]
filetypes = ['.rar', '.exe',".cvd"]
collection = []

# Obtiene los links de descarga
# OK
def getCol():
    for i in range(len(collection)):
        print(i)

# Si el servidor responde con 200 se trabaja con ese enlace 
# OK
def getUrl(url = []):
    for i in range(len(url)):
        try:
            link = url[i]
            print("Conectando con: " + link)
            print()
            
            if 200 == requests.get(link).status_code:
                print(link + " esta online")
                print()
                return link
            elif 200 != requests.get(link).status_code:
                print("""
                      
                      
                      Conexion rechazada
                      
                      Verifique VPN
                      
                      
                      """)
        except:
            print("No se pudo establecer la conexion con: " + link)
            continue
        else:
            return link
        
    print("""
          
          No se pudo establecer conexion con ningun servidor
          
          
          Tip:
            Mudate
          
          """)
    exit()
        
# Obtiene el HTML de la URL
# OK
def getHtml(online):
    if type(online) == str:
        request = requests.get(online)    
    else: 
        request = requests.get(online.get('href'))
    html = request.text
    soup_data = BeautifulSoup(html, 'html.parser')
    return soup_data

# Obtiene el url de las <a> y se deshace de los no validos
# Optimizar, ajustar y la madre de los tomates
def getHref(html,actual_url):

    href = []
    links = html.find_all("a")

    for i in range(len(links)):

        link = links[i]

        try:
        # Verificar si la URL contiene alguna de las excepciones
            for excepcion in exceptions:
                if re.search(excepcion, link.get('href')):
                    continue                
        except:
            depinga = 0
            
        # Si el enlace se encuentra en la lista de excepciones se ignora
        # Si el enlace no contiene barras ignorarlo
        if(link.get("href") in exceptions or link in href or link.text in exceptions ):
            continue
        
        # Si el enlace contiene al menos una barra completar enlace con la base
        elif(link.get("href").count('/') < 2):
            temp = actual_url + link.get('href')
            link['href'] = temp
            href.append(link)

        # Si el enlace contiene mas de 2 barras guardarlo
        else:
            href.append(link)
    print(href)
    return href

# Descarga el contenido del URL
# OK
def download(href):
    
    url, nombre = href.get("href"), href.text
    
    collection.append(url)
                    
    print("Descargando...")

    with open("./Updates/" + nombre, "wb") as file:
        response = requests.get(url)
        file.write(response.content)

    print("Descargado!!!")
       
def upydate(online_url = [], count = 0):
    
    if not online_url:
        return
    
    try:

        if count <= 0:
            mime_type = 'HTML'
            actual = online_url[0]
        
        else:
            mime_type = online_url[0].text
            actual = online_url[0].get('href')
        
        print(mime_type)

        if "HTML" in mime_type:
            # print("HTML!!")
            html = getHtml(actual)
            tag_objects = getHref(html,actual)
            upydate(tag_objects)
        elif "rar" in mime_type or "exe" in mime_type or 'cvd' in mime_type:
            download(online_url[0])
            
        """ else:
            print("La URL: " + actual + " contiene otro tipo de contenido: " + mime_type)
 """
    except requests.exceptions.RequestException as e:
        # Manejar cualquier excepción de solicitud
        print("Error al verificar la URL" + actual)

    # Llamar recursivamente a la función con el resto de las URLs
    upydate(online_url[1:], count + 1)