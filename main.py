import helpers

# Enlaces de las actualizaciones

URLs = [
 "https://antivirus.uclv.cu/",
 "http://ftp.uo.edu.cu/Antivirus/",
 "http://antivirus.uij.edu.cu/"
]

online_url = helpers.getUrl(URLs)

helpers.upydate(["https://antivirus.uclv.cu/clamav/"])
print("Completado!")
helpers.getCol()

