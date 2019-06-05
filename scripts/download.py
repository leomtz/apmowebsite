# Utilities to scrap info from previous APMO pages

import urllib.request

for j in range(2005,2019):
    filedata = urllib.request.urlopen('http://www.ommenlinea.org/wp-content/apmo/apmo%s_res.pdf' % j)  
    datatowrite = filedata.read()

    with open('apmo%s_res.pdf' % j, 'wb') as f:  
        f.write(datatowrite)