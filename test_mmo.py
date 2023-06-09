import unittest
from mmo import MMO


class test_QMO(unittest.TestCase):

    def setUp(self) -> None:
        self.n_1 = MMO("per")
        self.per = MMO("per")
        self.ent = MMO("ent")

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
        self.assertEqual(self.per.main_language("|a 930610s1852    sp           |||| ||spa"), "español")
        self.assertEqual(self.per.main_language("|a 930610s1852    sp           |||| ||ach"), "acoli")
    
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
        self.assertEqual(self.per.publication_date("|a 880309s1987    bu                  bul"),"1987")

    def test_decade(self):
        self.assertEqual(self.per.decade(None),None)
        self.assertEqual(self.per.decade("|a 880309s1987    bu                  bul"),"80")
        self.assertEqual(self.per.decade("|a 880309s1727    bu                  bul"),"20")
        self.assertEqual(self.per.decade("|a 880309s17uu    bu                  bul"),None)
        self.assertEqual(self.per.decade("|a 990501s19uu    sp                  spa"),None)
        
    def test_century(self):
        self.assertEqual(self.per.century(None),None)
        self.assertEqual(self.per.century("|a 880309s1987    bu                  bul"),"XX")
        self.assertEqual(self.per.century("|a 880309s198u    bu                  bul"),"XX")
        self.assertEqual(self.per.century("|a 880309s19ux    bu                  bul"),"XX")
        self.assertEqual(self.per.century("|a 880309s0100    bu                  bul"),"II")
        self.assertEqual(self.per.century("|a 880309s1530    bu                  bul"),"XVI")

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
    ENT:
    '''
    def test_ent_other_identifiers(self):
        self.assertEqual(self.ent.ent_other_identifiers(None),None)
        self.assertEqual(self.ent.ent_other_identifiers("|2 X|a B"), " X:  B")
    
    def test_ent_establishment_date(self):
        self.assertEqual(self.ent.ent_establishment_date(None), None)
        self.assertEqual(self.ent.ent_establishment_date("|q Algún valor|s Algún otro valor S"), "Algún valor")
        self.assertEqual(self.ent.ent_establishment_date("|s Algún otro valor S"), "Algún otro valor S")

    def test_finish_date(self):
        self.assertEqual(self.ent.ent_finish_date(None), None)
        self.assertEqual(self.ent.ent_finish_date("|r R|tTTT"), "R")
        self.assertEqual(self.ent.ent_finish_date("R|t TTT"), "TTT")

    def test_entity_name(self):
        self.assertEqual(self.ent.ent_entity_name(None), None)
        self.assertEqual(self.ent.ent_entity_name("|a XX"), "XX")
        self.assertEqual(self.ent.ent_entity_name("|a XX|b BB"), "XX,  BB,  BB...")
        self.assertEqual(self.ent.ent_entity_name("|a XX|b BB|eEE"), "XX,  BB,  BB...EE")
    
    def test_ent_relationship_note(self):
        self.assertEqual(self.ent.ent_relationship_note(None), None)
        self.assertEqual(self.ent.ent_relationship_note("|a XX"), "XX")
        self.assertEqual(self.ent.ent_relationship_note("|a XX|b 1|b 2 2|b hola como"), "XX 1, 2 2, hola como")

if __name__ == '__main__':
    unittest.main()
