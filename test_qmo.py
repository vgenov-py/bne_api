import unittest
from db import QMO

qmo_funcs = QMO("")

class test_QMO(unittest.TestCase):

    def setUp(self) -> None:
         self.n_1 = QMO("geo", {"id": "XX1000003", "limit": 1})
         self.per = QMO("per", {"id": "XX1000003", "limit": 1})
         self.joining_query = QMO("mon", {"id": "21", "per": "id:3"})
         self.joining_query_2 = QMO("mon", {"t_008": "21", "per": "id:3"})

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
    
    def test_country_of_publication(self):
        self.assertEqual(self.per.country_of_publication(None),None)
        self.assertEqual(self.per.country_of_publication("|a930610s1852    sp           |||| ||spa"), "España")
        self.assertEqual(self.per.country_of_publication("|a951102s1832    sp     | |||| 000 0 lat"), "España")
        self.assertEqual(self.per.country_of_publication("|a951102s1832    abc     | |||| 000 0 lat"), "Alberta")

    def test_main_language(self):
        self.assertEqual(self.per.main_language(None),None)
        self.assertEqual(self.per.main_language("|a930610s1852    sp           |||| ||spa"), "español")
        self.assertEqual(self.per.main_language("|a930610s1852    sp           |||| ||ach"), "acoli")
    
    def test_other_languages(self):
        self.assertEqual(self.per.other_languages(None), None)
        self.assertEqual(self.per.other_languages("|abul|brus|bfre"), "ruso, francés")
        self.assertEqual(self.per.other_languages("|abul|brus|bfre|baaa"), "ruso, francés, aaa")
        self.assertEqual(self.per.other_languages("|abul|brus|bfre|baaa|deng"), "ruso, francés, aaa, inglés")
    
    def test_original_language(self):
        self.assertEqual(self.per.original_language(None), None)
        self.assertEqual(self.per.original_language("|abul|brus|bfre|baaa|deng|heng"), "inglés")

    def test_publication_date(self):
        self.assertEqual(self.per.publication_date(None),None)
        self.assertEqual(self.per.publication_date("|a880309s1987    bu                  bul"),"1987")

    def test_decade(self):
        self.assertEqual(self.per.decade(None),None)
        self.assertEqual(self.per.decade("|a880309s1987    bu                  bul"),"80")
        self.assertEqual(self.per.decade("|a880309s1727    bu                  bul"),"20")
        self.assertEqual(self.per.decade("|a880309s17uu    bu                  bul"),None)
        self.assertEqual(self.per.decade("|a990501s19uu    sp                  spa"),None)
        
    def test_century(self):
        self.assertEqual(self.per.century(None),None)
        self.assertEqual(self.per.century("|a880309s1987    bu                  bul"),"XX")
        self.assertEqual(self.per.century("|a880309s198u    bu                  bul"),"XX")
        self.assertEqual(self.per.century("|a880309s19ux    bu                  bul"),"XX")
        self.assertEqual(self.per.century("|a880309s0100    bu                  bul"),"II")
        self.assertEqual(self.per.century("|a880309s1530    bu                  bul"),"XVI")

    def test_legal_deposit(self):
        self.assertEqual(self.per.legal_deposit(None), None)
        self.assertEqual(self.per.legal_deposit("|aCR 1714-1986|bOficina Depósito Legal Ciudad Real"), "CR 1714-1986")
        self.assertEqual(self.per.legal_deposit("|aCR 1714-1986|bOficina Depósito Legal Ciudad Real|aCRotronúmero"), "CR 1714-1986 /**/ CRotronúmero")

    def test_isbn(self):
        self.maxDiff = None
        self.assertEqual(self.per.isbn("|a978-84-345-1144-6|qobra completa"), "978-84-345-1144-6 (obra completa)")    
        self.assertEqual(self.per.isbn("|a978-84-345-1144-6|qobra completa /**/ |a988-84-345-1144-6|qobra incompleta"), "978-84-345-1144-6 (obra completa)  /**/ 988-84-345-1144-6 (obra incompleta)")    
    
    def test_mon_title(self):
        self.assertEqual(self.per.mon_title(None),None)
        self.assertEqual(self.per.mon_title("|aMérope|h[Texto impreso] :|btragedia en cinco actos de Alfieri|ctraducción de Juan Eugenio Harcenbusch"), "Mérope: tragedia en cinco actos de Alfieri.")
        self.assertEqual(self.per.mon_title("|aMérope|h[Texto impreso] :|btragedia en cinco actos de Alfieri|ctraducción de Juan Eugenio Harcenbusch|nDollarN|pDollarP"), "Mérope: tragedia en cinco actos de Alfieri. DollarN, DollarP")

    def test_mon_other_titles(self):
        self.assertEqual(self.per.mon_other_titles("|iII|aAA|bBB|nNN|pPP", None), "II: AA: BB. NN, PP")
        self.assertEqual(self.per.mon_other_titles("|iII|aAA|bBB|nNN|pPP", "|aAAA"), "II: AA: BB. NN, PP /**/ AAA")
    
    def test_edition(self):
        self.assertEqual(self.per.mon_edition("|aAA|bBB"), "AA, BB")
        self.assertEqual(self.per.mon_edition("|aAA"), "AA")

    def test_mon_publication_place(self):
        self.assertEqual(self.per.mon_publication_place("|aAA", None), "AA")
        self.assertEqual(self.per.mon_publication_place(None, "|aAA"), "AA")

    def test_mon_serie(self):
        self.assertEqual(self.per.mon_serie("|aAA|vVV", None), "AAVV")
        self.assertEqual(self.per.mon_serie(None, "|aAA|vVV"), "AAVV")
        self.assertEqual(self.per.mon_serie("|aXX|vYY","|aAA|vVV"), "XXYY /**/ AAVV")
    
    def test_mon_notes(self):
        self.assertEqual(self.per.mon_notes({"500":"|aAA", "594": "|a594", "563": None}), "AA /**/ 594")
        self.assertEqual(self.per.mon_notes({}), None)
    
    def test_mon_subject(self):
        self.assertEqual(self.per.mon_subject({"600": "|a[S.l.]|b[s.n.]|cimp. 1832|eVich|fpor Ignacio Valls, imp.|2XX|1|3|4|5|6|7|8|9|10"}, ("600", "610", "611", "630", "650", "651", "653")), "[S.l.] - [s.n.] - imp. 1832 - Vich - por Ignacio Valls, imp. - 0")
        self.assertEqual(self.per.mon_subject({"600": "|a[S.l.]|b[s.n.]|cimp. 1832|eVich|fpor Ignacio Valls, imp.|2XX|1|3|4|5|6|7|8|9|10", "610":"|2A"}, ("600", "610", "611", "630", "650", "651", "653")), "[S.l.] - [s.n.] - imp. 1832 - Vich - por Ignacio Valls, imp. - 0")
    
    def test_mon_authors(self):
        self.assertEqual(self.per.mon_authors(None, "700"), None)
        self.assertEqual(self.per.mon_authors("|aCervantes Saavedra, Miguel de|d1547-1616|0XX1718747", None), "Cervantes Saavedra, Miguel de, (1547-1616)")
        self.assertEqual(self.per.mon_authors("|aCervantes Saavedra, Miguel de|d1547-1616|0XX1718747", "|aJarvis, Charles|d1675?-1739|0http://datos.bne.es/resource/XX979939|eXX"), "Cervantes Saavedra, Miguel de, (1547-1616) /**/ Jarvis, Charles, (1675?-1739)(XX)")

    '''
    PURGUE:
    '''

    # def test_purgue(self):
    #     # self.assertEqual(self.n_1.purgue, {'success': True, 'limit': 1, 'fields': None, 'args': {'id': 'XX1000003'}})
    #     self.assertEqual(self.joining_query.purgue, {'success': True, 'limit': "1000", 'fields': None, 'args': {'id': '21'}, "dataset_2":{"per":"a:3"}})
    
    '''
    JOINING:
    '''

    def test_joining(self):
        to_where = self.joining_query.joining({"per":"a:hola"})
        to_where = list(to_where.values())[0]
        self.assertEqual(self.joining_query.joining({"per":"a:3"}), {"per":{"a":"3"}})
        self.assertEqual(self.joining_query.joining({"per":"a:3,b:2"}), {"per":{"a":"3", "b": "2"}})

    '''
    WHERE:
    '''

    # def test_where(self):
    #     args = {"id":"XX100900"}
    #     where_id = '''WHERE ( per_fts match \'id:NEAR("XX100900")\'  )'''
    #     self.assertEqual(self.per.where(args), where_id)
    #     args = {"id": "XX", "t_100": "Fernández"}
    #     self.assertEqual(self.per.where(args), '''WHERE ( per_fts match 'id:NEAR("XX")'   AND  per_fts match 't_100:NEAR("Fernández")\'  )''')
    #     args = {"t_375": "masculino||femenino"}
    #     self.assertEqual(self.per.where(args), '''WHERE (per.t_375 LIKE '|%masculino%' OR per.t_375 LIKE '|%femenino%')''')
    #     args = {"t_375": "masculino||femenino", "t_670": "Out of"}
    #     self.assertEqual(self.per.where(args), '''WHERE (per.t_375 LIKE '|%masculino%' OR per.t_375 LIKE '|%femenino%' AND per.t_670 LIKE '|%out of%')''')
    #     args = {"t_375": "masculino||femenino", "t_670": "Out of||AA"}
    #     self.assertEqual(self.per.where(args), '''WHERE (per.t_375 LIKE '|%masculino%' OR per.t_375 LIKE '|%femenino%' AND per.t_670 LIKE '|%out of%' OR per.t_670 LIKE '|%aa%')''')
    
    
    '''
    WHERE_FTS:
    '''
    def test_where_fts(self):
        args = {"id": "XX100900"}
        self.assertEqual(self.per.where_fts(args),"WHERE per_fts MATCH 'id: XX100900*' ")
        args = {"id": "XX100900", "t_100": "Genovese"}
        self.assertEqual(self.per.where_fts(args),"WHERE per_fts MATCH 'id: XX100900*'  AND 't_100: Genovese*' ")
        args = {"t_100": "Genovese||Berjano"}
        self.assertEqual(self.per.where_fts(args),"WHERE per_fts MATCH 't_100: Genovese* OR Berjano*' ")
        args = {"t_100": "Genovese||Berjano||Gorzinski", "id": "XX1010"}
        self.assertEqual(self.per.where_fts(args),"WHERE per_fts MATCH 't_100: Genovese* OR Berjano* OR Gorzinski*'  AND 'id: XX1010*' ")
        args = {"id": "!XX100900"}
        self.assertEqual(self.per.where_fts(args),"WHERE per_fts MATCH 't_001: a * NOT id: XX100900*' ")
        
    
    # '''
    # QUERY:
    # '''

    # def test_query(self):
    #     result = '''SELECT mon.id, mon.t_001, mon.t_008, mon.t_020, mon.t_035, mon.t_040, mon.t_100, mon.t_130, mon.t_245, mon.t_260, mon.t_300, mon.t_500, mon.t_700, mon.t_899, mon.t_927, mon.t_980, mon.t_994, mon.per_id FROM mon WHERE mon.t_008 LIKE 21 LIMIT 1000;'''
    #     self.assertEqual(self.joining_query_2.query()["query"],result)

if __name__ == '__main__':
    qmo_funcs = tuple(filter(lambda func: not func.startswith("__"),dir(qmo_funcs)))
    test_funcs = tuple(filter(lambda func: func.startswith("test"),dir(test_QMO)))
    print(f"{round(len(test_funcs) / len(qmo_funcs),4) * 100}% tested")
    unittest.main()