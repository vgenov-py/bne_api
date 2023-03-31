import unittest
import requests as req

LIMIT = 1
url = "http://127.0.0.1:3000/api"

def get_res(url):
    # print(req.get(url).json()["data"])
    return req.get(url).json()["data"]

class Test_routes(unittest.TestCase):

    def test_geo(self):
        url =f"http://127.0.0.1:3000/api/geo?limit={LIMIT}"
        self.assertListEqual(get_res(url), [{'id': 'XX102734', 't_001': '|aXX102734', 't_024': '|ahttp://id.loc.gov/authorities/names/n96077394|2lcnaf /**/ |ahttp://viaf.org/viaf/315538112|2viaf', 't_034': '|dE0020143|eE0020143|fN0412156|gN0412156|2geonames', 't_080': '|a(460.235-21 Santa Coloma de Cervelló)|22015', 't_151': '|aCòlonia Güell (Santa Coloma de Cervelló)', 't_451': None, 't_510': None, 't_550': '|aBarrios|zSanta Coloma de Cervelló', 't_551': None, 't_667': None, 't_670': '|aLCSH|b[Colònia Güell S.A. (Santa Coloma de Cervelló, Spain)] /**/ |aGeoNames|b(Còlonia Güell) /**/ |aWWW Còlonia Güell, 21-10-2014|b(Còlonia Güell, Santa Coloma de Cervelló. La Colonia Güell se inició en el año 1.890 a iniciativa del empresario Eusebi Güell en su finca Can Soler de la Torre, situada en el término municipal de Santa Coloma de Cervelló, actual Comarca del Baix Llobregat)|uhttp://www.gaudicoloniaguell.org/', 't_781': None, 'id_BNE': 'XX102734', 'otros_identificadores': 'lcnaf: http://id.loc.gov/authorities/names/n96077394 /**/ viaf: http://viaf.org/viaf/315538112 /**/ ', 'coordenadas_lat_lng': '2.0143, 41.2156', 'CDU': '(460.235-21 Santa Coloma de Cervelló), 2015', 'nombre_de_lugar': 'Còlonia Güell (Santa Coloma de Cervelló)', 'otros_nombres_de_lugar': None, 'entidad_relacionada': None, 'materia_relacionada': 'Barrios, Santa Coloma de Cervelló', 'lugar_relacionado': None, 'nota_general': None, 'fuentes_de_informacion': 'LCSH: [Colònia Güell S.A. (Santa Coloma de Cervelló, Spain)] /**/ GeoNames: (Còlonia Güell) /**/ ', 'lugar_jerarquico': None, 'obras_relacionadas_en_el_catalogo_BNE': 'http://catalogo.bne.es/uhtbin/cgisirsi/0/x/0/05?searchdata1=102734'}])
        self.assertListEqual(get_res(f"{url}&fields=id"), [{'id': 'XX102734'}])
        self.assertListEqual(get_res(f"{url}&id=XX102734&fields=id,lugar_jerarquico"), [{'id': 'XX102734', "lugar_jerarquico":None}])


if __name__ == '__main__':
    unittest.main()