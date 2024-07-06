import helpers
import time

# import os
# import config

# config.load()

# Enlaces de las actualizaciones
URLs = [
    "https://antivirus.uclv.cu/",
    "http://ftp.uo.edu.cu/Antivirus/",
    "http://antivirus.uij.edu.cu/",
]

online_url = helpers.connect(URLs)

helpers.upydate([online_url])
print("Completado!")
