import helpers
import time

# import os
# import config

# config.load()

# Enlaces de las actualizaciones
URLs = [
    "https://antivirus.uclv.cu/nod32/",
    "http://ftp.uo.edu.cu/Antivirus/",
]

online_url = helpers.connect(URLs)

helpers.upydate([online_url])
