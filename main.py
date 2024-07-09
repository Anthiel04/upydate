from uclv import UCLV
from ftp import FTP
from uij import UIJ
import simplemenu

# import os
# import config

# config.load()

# Enlaces de las actualizaciones
default = 0
menu(default)

villa_clara = UCLV("https://antivirus.uclv.cu/")
provincia = FTP("http://ftp.uo.edu.cu/Antivirus/")
uci_o_cujae_nise = UIJ("http://antivirus.uij.edu.cu/")

URLs = [
    villa_clara,
    provincia,
    uci_o_cujae_nise,
]


print(villa_clara.direct_links)
