from fastapi import APIRouter
import requests

router = APIRouter(
    prefix="/map",
    tags=["Mapa"]
)

@router.get("/wfs")
def get_wfs_data():
    # Exemplo de chamada a um WFS (ajustar conforme seu GeoServer)
    url = "http://<SEU_GEOSERVER>/geoserver/ows"
    params = {
        "service": "WFS",
        "version": "1.0.0",
        "request": "GetFeature",
        "typeName": "NOME_DO_LAYER",
        "outputFormat": "application/json",
        "srsName": "EPSG:4326"
    }

    response = requests.get(url, params=params)
    return response.json()
