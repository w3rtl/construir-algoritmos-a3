import os
import requests
from dotenv import load_dotenv
from folium import Map, Marker, Icon

load_dotenv(".env")

s = requests.Session()
res = s.post(f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={os.getenv('SPTRANS_TOKEN')}")
print(res.text)

# linha 209P - Term. Pinheiros / Cachoeirinha
paradas = s.get("http://api.olhovivo.sptrans.com.br/v2.1/Parada/BuscarParadasPorLinha?codigoLinha=2216").json()
pos = s.get("http://api.olhovivo.sptrans.com.br/v2.1/Posicao/Linha?codigoLinha=2216").json()

# tiles do Esri (os do OpenStreetMap bloqueiam quando o html é aberto direto do arquivo)
m = Map(location=[paradas[0]["py"], paradas[0]["px"]], zoom_start=14, tiles="Esri.WorldStreetMap")

# paradas em azul
for i in paradas:
    Marker(location=[i["py"], i["px"]], popup=i["np"], icon=Icon(color="blue")).add_to(m)

# ônibus em vermelho
for i in pos["vs"]:
    Marker(location=[i["py"], i["px"]], popup=i["p"], icon=Icon(color="red")).add_to(m)

m.save("mapa.html")
