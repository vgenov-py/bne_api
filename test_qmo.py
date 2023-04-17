import unittest
from db import QMO

class test_QMO(unittest.TestCase):

    def setUp(self) -> None:
         self.n_1 = QMO("per", {"id": "XX1000003", "limit": 1})

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

    def test_dollar_parser(self):
        self.assertEqual(self.n_1.dollar_parser("|aNombre"), "Nombre")
        self.assertEqual(self.n_1.dollar_parser("|aNombre|bApellido"), "Nombre, Apellido")
        self.assertEqual(self.n_1.dollar_parser("|a|Nombre"), ", ombre")

    def test_other_identifiers(self):
        self.assertEqual(self.n_1.other_identifiers("|aURL|2Nombre"), "Nombre: URL /**/ ")
        
    def test_related_palce(self):
        self.assertEqual(self.n_1.related_place("|wg|aEspaña /**/ |wh|aBarcelona (Provincia) /**/ |wh|aGerona (Provincia) /**/ |wh|aLérida (Provincia) /**/ |wh|aTarragona (Provincia) /**/ |aComarques Centrals (Cataluña)"), "España /**/ Barcelona (Provincia) /**/ Gerona (Provincia) /**/ Lérida (Provincia) /**/ Tarragona (Provincia) /**/ Comarques Centrals (Cataluña) /**/ ")

if __name__ == '__main__':
    unittest.main()