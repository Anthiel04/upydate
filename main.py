from uclv import UCLV
from ftp import FTP
from uij import UIJ
from cultura import Cultura

# Enlaces de las actualizaciones

villa_clara = UCLV("https://antivirus.uclv.cu/")
""" provincia = FTP("http://ftp.uo.edu.cu/Antivirus/")
uci_o_cujae_nise = UIJ("http://antivirus.uij.edu.cu/") """
""" cultura = Cultura("http://ftp.baibrama.cult.cu/Antivirus/Actualizaciones/") """

""" URLs = [
    villa_clara,
    provincia,
    uci_o_cujae_nise,
    cultura
] """

print(villa_clara.direct_links)
villa_clara.direct_links["aviupd.exe"]()