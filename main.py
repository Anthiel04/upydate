from uclv import UCLV
from ftp import FTP
from uij import UIJ
import helpers

# import os
# import config

# config.load()

# Enlaces de las actualizaciones


villa_clara = UCLV("https://antivirus.uclv.cu/")
provincia = FTP("http://ftp.uo.edu.cu/Antivirus/")
uci_o_cujae_nise = UIJ("http://antivirus.uij.edu.cu/")

URLs = [
    villa_clara,
    provincia,
    uci_o_cujae_nise,
]

for objeto in URLs:
    objeto.verify()

print(provincia.get("direct_links"))
print(uci_o_cujae_nise.direct_links)
print(villa_clara["direct_links"])
