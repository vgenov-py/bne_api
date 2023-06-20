import unittest
from qargs import Qargs
from sqlite3 import Cursor

class test_Qargs(unittest.TestCase):

    def setUp(self) -> None:
        self.empty = Qargs("per",{})
        self.table = Qargs("per",{"table":"per"})
        self.table_limit = Qargs("per",{"table":"per", "limit":1000})
        self.table_fields = Qargs("per",{"table": "per", "fields":"id,t_001,t_003"})
        self.table_filters = Qargs("per",{"table": "per", "filters": {"id": "XX123000", "t_001":"XX123000"}})
    
    def tearDown(self) -> None:
        pass

    '''
    Connection:
    '''
    def test_db(self):
        self.assertEqual(type(self.empty.cur), Cursor)

    '''
    clean_args()
    '''
    def test_clean_args(self):
        pass
        # self.assertEqual(self.empty.clean_args({"table":"per"}),"")
    '''
    Table:
    '''
    def test_table(self):
        self.assertEqual(self.table.table, "per")
        with self.assertRaises(Exception):
            self.empty.table
    '''
    Limit:
    '''
    def test_limit(self):
        self.assertEqual(self.table_limit.limit, 1000)
        with self.assertRaises(Exception):
            self.table.limit
    '''
    Available fields:
    '''
    def test_available_fields(self):
        self.assertEqual(self.table.available_fields, ('per.id', 'per.t_001', 'per.t_024', 'per.t_046', 'per.t_100', 'per.t_368', 'per.t_370', 'per.t_372', 'per.t_373', 'per.t_374', 'per.t_375', 'per.t_377', 'per.t_400', 'per.t_500', 'per.t_510', 'per.t_670', 'per.otros_identificadores', 'per.fecha_nacimiento', 'per.fecha_muerte', 'per.nombre_de_persona', 'per.otros_atributos_persona', 'per.lugar_nacimiento', 'per.lugar_muerte', 'per.pais_relacionado', 'per.otros_lugares_relacionados', 'per.lugar_residencia', 'per.campo_actividad', 'per.grupo_o_entidad_relacionada', 'per.ocupacion', 'per.genero', 'per.lengua', 'per.otros_nombres', 'per.persona_relacionada', 'per.fuentes_de_informacion', 'per.obras_relacionadas_en_el_catalogo_BNE'))
    '''
    Fields:
    '''
    def test_fields(self):
        self.assertEqual(type(self.table_fields.fields), str)
        self.assertEqual(self.table.fields, None)
        self.assertEqual(self.table_fields.fields, "id,t_001,t_003")
    '''
    Filters:
    '''
    def test_filters(self):
        self.assertEqual(type(self.table_filters.filters), dict)
        self.assertEqual(self.table_filters.filters, {"id": "XX123000", "t_001":"XX123000"})
    '''
    SELECT:
    '''
    def test_select(self):
        self.assertEqual(type(self.table_fields.select), str)
        self.assertEqual(self.table_fields.select, "SELECT id,t_001,t_003 FROM per")
        select_statement = '''SELECT per.id, per.t_001, per.t_024, per.t_046, per.t_100, per.t_368, per.t_370, per.t_372, per.t_373, per.t_374, per.t_375, per.t_377, per.t_400, per.t_500, per.t_510, per.t_670, per.otros_identificadores, per.fecha_nacimiento, per.fecha_muerte, per.nombre_de_persona, per.otros_atributos_persona, per.lugar_nacimiento, per.lugar_muerte, per.pais_relacionado, per.otros_lugares_relacionados, per.lugar_residencia, per.campo_actividad, per.grupo_o_entidad_relacionada, per.ocupacion, per.genero, per.lengua, per.otros_nombres, per.persona_relacionada, per.fuentes_de_informacion, per.obras_relacionadas_en_el_catalogo_BNE FROM per'''
        self.assertEqual(self.table.select, select_statement)
    '''
    WHERE:
    '''
    def test_where(self):
        self.assertEqual(self.table_filters.where, "WHERE per.id LIKE '%XX123000%' AND per.t_001 LIKE '%XX123000%'")
    '''
    QUERY:
    '''
    def test_query(self):    
        self.assertEqual(self.table_filters.query, "SELECT per.id, per.t_001, per.t_024, per.t_046, per.t_100, per.t_368, per.t_370, per.t_372, per.t_373, per.t_374, per.t_375, per.t_377, per.t_400, per.t_500, per.t_510, per.t_670, per.otros_identificadores, per.fecha_nacimiento, per.fecha_muerte, per.nombre_de_persona, per.otros_atributos_persona, per.lugar_nacimiento, per.lugar_muerte, per.pais_relacionado, per.otros_lugares_relacionados, per.lugar_residencia, per.campo_actividad, per.grupo_o_entidad_relacionada, per.ocupacion, per.genero, per.lengua, per.otros_nombres, per.persona_relacionada, per.fuentes_de_informacion, per.obras_relacionadas_en_el_catalogo_BNE FROM per WHERE per.id LIKE '%XX123000%' AND per.t_001 LIKE '%XX123000%' LIMIT 1000;")

if __name__ == '__main__':
    unittest.main()