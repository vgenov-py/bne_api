import unittest
from db import QMO

qmo_funcs = QMO("")

class test_QMO(unittest.TestCase):

    def setUp(self) -> None:
         self.n_1 = QMO("geo", {"id": "XX1000003", "limit": 1})
         self.per = QMO("per", {"id": "XX1000003", "limit": 1})
         self.joining_query = QMO("mon", {"id": "21", "per": "a:3"})
         self.joining_query_2 = QMO("mon", {"t_008": "21", "per": "a:3"})

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

    def test_(self):
        self.assertEqual(self.per.group_or_entity({}), None)
        self.assertEqual(self.per.group_or_entity({"373":"|aAteneo de Madrid|2abne","510":"|aEspaña|bPresidente (1936-1939: Azaña) /**/ |wr|iEntidad corporativa fundada:|aIzquierda Republicana (España. 1934-1959) /**/ |wr|iEntidad corporativa fundada:|aAcción Republicana"}), "Ateneo de Madrid /**/ España, Presidente (1936-1939: Azaña) /**/ , r, Entidad corporativa fundada:, Izquierda Republicana (España. 1934-1959) /**/ , r, Entidad corporativa fundada:, Acción Republicana")
    
    '''
    MON:
    '''

    def test_get_single_dollar(self):
        self.assertEqual(self.per.mon_per_id("|aRipoll y Vilamajó, Jaime|0XX919455"), "XX919455")
        self.assertEqual(self.per.mon_per_id("|aAntón, Francisco|qAntón Alted"), None)
        self.assertEqual(self.per.mon_per_id(None), None)
        self.assertEqual(self.per.mon_per_id(""), None)

    '''
    PURGUE:
    '''

    def test_purgue(self):
        # self.assertEqual(self.n_1.purgue, {'success': True, 'limit': 1, 'fields': None, 'args': {'id': 'XX1000003'}})
        self.assertEqual(self.joining_query.purgue, {'success': True, 'limit': "1000", 'fields': None, 'args': {'id': '21'}, "dataset_2":{"per":"a:3"}})
    
    '''
    JOINING:
    '''

    def test_joining(self):
        to_where = self.joining_query.joining({"per":"a:hola"})
        to_where = list(to_where.values())[0]
        self.assertEqual(self.joining_query.joining({"per":"a:3"}), {"per":{"a":"3"}})

    '''
    WHERE:
    '''

    def test_where(self):
        args = {"id":"XX100900"}
        where_id = '''WHERE  per_fts match \'id:NEAR("XX100900")\'  '''
        self.assertEqual(self.per.where(args), where_id)
        args = {"id": "XX", "t_100": "Fernández"}
        self.assertEqual(self.per.where(args), '''WHERE  per_fts match 'id:NEAR("XX")'   AND  per_fts match 't_100:NEAR("Fernández")\'  ''')
        args = {"id": "XX", "t_375": "mas culino","t_300": "!some value"}

    '''
    QUERY:
    '''

    def test_query(self):
        result = '''SELECT mon.id, mon.t_001, mon.t_008, mon.t_020, mon.t_035, mon.t_040, mon.t_100, mon.t_130, mon.t_245, mon.t_260, mon.t_300, mon.t_500, mon.t_700, mon.t_899, mon.t_927, mon.t_980, mon.t_994, mon.per_id FROM mon WHERE mon.t_008 LIKE 21 LIMIT 1000;'''
        self.assertEqual(self.joining_query_2.query()["query"],result)
if __name__ == '__main__':
    qmo_funcs = tuple(filter(lambda func: not func.startswith("__"),dir(qmo_funcs)))
    test_funcs = tuple(filter(lambda func: func.startswith("test"),dir(test_QMO)))
    print(f"{round(len(test_funcs) / len(qmo_funcs),4) * 100}% tested")
    unittest.main()