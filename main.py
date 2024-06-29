import helpers

# Enlaces de las actualizaciones

URLs = [
 "https://antivirus.uclv.cu/",
 "http://ftp.uo.edu.cu/Antivirus/",
 "http://antivirus.uij.edu.cu/"
]

online_url = helpers.getUrl(URLs)

data = helpers.getHtml(online_url)

href = helpers.getHref(data,online_url)

print(href)

helpers.download(href)


