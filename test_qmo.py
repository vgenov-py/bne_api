import unittest
from db import QMO

qmo_funcs = QMO("")

class test_QMO(unittest.TestCase):

    def setUp(self) -> None:
         self.n_1 = QMO("geo", {"id": "XX1000003", "limit": 1})
         self.per = QMO("per", {"id": "XX1000003", "limit": 1})

    def n_test(self):
        n_t = 0
        for func in dir(self):
            if func.startswith("test_"):
                n_t += 1
        n_f = 0
        for func in dir(self.n_1):
            if not func.startswith("__"):
                n_f += 1
        return n_t - n_f
    
    def tearDown(self) -> None:
         pass

    '''
    GEO:
    '''

    def test_dollar_parser(self):
        self.assertEqual(self.n_1.dollar_parser("|aNombre"), "Nombre")
        self.assertEqual(self.n_1.dollar_parser("|aNombre|bApellido"), "Nombre, Apellido")
        self.assertEqual(self.n_1.dollar_parser("|a|Nombre"), ", ombre")

    def test_other_identifiers(self):
        self.assertEqual(self.n_1.other_identifiers("|aURL|2Nombre"), "Nombre: URL /**/ ")
        
    def test_related_palce(self):
       self.assertEqual(self.n_1.related_place("|wg|aEspaña /**/ |wh|aBarcelona (Provincia) /**/ |wh|aGerona (Provincia) /**/ |wh|aLérida (Provincia) /**/ |wh|aTarragona (Provincia) /**/ |aComarques Centrals (Cataluña)"), "España /**/ Barcelona (Provincia) /**/ Gerona (Provincia) /**/ Lérida (Provincia) /**/ Tarragona (Provincia) /**/ Comarques Centrals (Cataluña) /**/ ")

    def test_sources(self):
        self.assertEqual(self.n_1.sources("|aLCSH|b[Colònia Güell S.A. (Santa Coloma de Cervelló, Spain)] /**/ |aGeoNames|b(Còlonia Güell) /**/ |aWWW Còlonia Güell, 21-10-2014|b(Còlonia Güell, Santa Coloma de Cervelló. La Colonia Güell se inició en el año 1.890 a iniciativa del empresario Eusebi Güell en su finca Can Soler de la Torre, situada en el término municipal de Santa Coloma de Cervelló, actual Comarca del Baix Llobregat)|uhttp://www.gaudicoloniaguell.org/"), "LCSH: [Colònia Güell S.A. (Santa Coloma de Cervelló, Spain)] /**/ GeoNames: (Còlonia Güell) /**/ ")

    def test_gen_url(self):
        self.assertEqual(self.n_1.gen_url("|aXX102734"), "http://catalogo.bne.es/uhtbin/cgisirsi/0/x/0/05?searchdata1=102734")
    
    def test_f_lat_lng(self):
        self.assertEqual(self.n_1.f_lat_lng("|dE0020143|eE0020143|fN0412156|gN0412156|2geonames"), "2.0143, 41.2156")
    
    '''
    PER:
    '''
    def test_per_person_name(self):
        self.assertEqual(self.per.per_person_name("|aTolstói, Lev|d1828-1910"), "Tolstói, Lev, (1828-1910)")
        self.assertEqual(self.per.per_person_name("|aCasanueva del Mazo, Bernardo|d1920-1993"), "Casanueva del Mazo, Bernardo, (1920-1993)")

    def test_per_other_attributes(self):
        self.assertEqual(self.per.per_other_attributes(None),None)
        self.assertEqual(self.per.per_other_attributes("|cNombre artístico"),"Nombre artístico")
        self.assertEqual(self.per.per_other_attributes("|cSanto /**/ |dObispo de Lyon"),"Santo /**/ Obispo de Lyon")

    def test_per_other_sources(self):
        return
        self.assertEqual(self.per.per_other_attributes(None),None)
        self.assertEqual(self.per.per_other_attributes(""),"")

    def test_per_gen_url(self):
        self.assertEqual(self.per.per_gen_url("|aXX133007"), "http://catalogo.bne.es/uhtbin/cgisirsi/0/x/0/05?searchdata1=%5ea133007")
        self.assertEqual(self.per.per_gen_url(None), None)


if __name__ == '__main__':
    qmo_funcs = tuple(filter(lambda func: not func.startswith("__"),dir(qmo_funcs)))
    test_funcs = tuple(filter(lambda func: func.startswith("test"),dir(test_QMO)))
    print(f"{round(len(test_funcs) / len(qmo_funcs),4) * 100}% tested")
    unittest.main()