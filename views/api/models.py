query_create_geo = f'''
    CREATE TABLE geo (
        id TEXT PRIMARY KEY,
        t_001 TEXT,
        t_024 TEXT,
        t_034 TEXT,
        t_080 TEXT,
        t_151 TEXT,
        t_451 TEXT,
        t_510 TEXT,
        t_550 TEXT,
        t_551 TEXT,
        t_667 TEXT,
        t_670 TEXT,
        t_781 TEXT,
        id_BNE TEXT,
        otros_identificadores TEXT,
        coordenadas_lat_lng TEXT,
        CDU TEXT,
        nombre_de_lugar TEXT,
        otros_nombres_de_lugar TEXT,
        entidad_relacionada TEXT,
        materia_relacionada TEXT,
        lugar_relacionado TEXT,
        nota_general TEXT,
        fuentes_de_informacion TEXT,
        lugar_jerarquico TEXT,
        obras_relacionadas_en_el_catalogo_BNE TEXT
    );
'''

query_create_per = f'''
    CREATE TABLE per (
    id TEXT PRIMRAY KEY,
    t_001 TEXT,
    t_003 TEXT,
    t_005 TEXT,
    t_008 TEXT,
    t_024 TEXT,
    t_046 TEXT,
    t_100 TEXT,
    t_368 TEXT,
    t_370 TEXT,
    t_372 TEXT,
    t_373 TEXT,
    t_374 TEXT,
    t_375 TEXT,
    t_377 TEXT,
    t_400 TEXT,
    t_500 TEXT,
    t_670 TEXT,
    geo_id TEXT
    );
'''

query_create_mon = f'''
    CREATE TABLE mon (
    id TEXT PRIMARY KEY,
    t_001 TEXT,
    t_035 TEXT,
    t_040 TEXT,
    t_100 TEXT,
    t_130 TEXT,
    t_245 TEXT,
    t_260 TEXT,
    t_300 TEXT,
    t_500 TEXT,
    t_899 TEXT,
    t_927 TEXT,
    t_980 TEXT,
    t_994 TEXT
    );
'''