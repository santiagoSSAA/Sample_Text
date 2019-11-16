import ConfigParser

mapa=ConfigParser.ConfigParser()
mapa.read('mapa.map')
print mapa.sections()
print mapa.items('info')
print mapa.get('info','mapa')
mp=''
for s in mapa.sections():
    print s
    if s=='info':
        mp=mapa.get(s,'mapa')
    else:
        print mapa.get(s,'tipo'), mapa.get(s,'fila'),mapa.get(s,'col')
print mp, type(mp)
