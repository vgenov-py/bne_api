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


query_create_per_human = f'''
    CREATE TABLE per (
    id TEXT PRIMARY KEY,
    t_001 TEXT,
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
    t_510 TEXT,
    t_670 TEXT,
    otros_identificadores TEXT,
    fecha_nacimiento TEXT,
    fecha_muerte TEXT,
    nombre_de_persona TEXT,
    otros_atributos_persona TEXT,
    lugar_nacimiento TEXT,
    lugar_muerte TEXT,
    pais_relacionado TEXT,
    otros_lugares_relacionados TEXT,
    lugar_residencia TEXT,
    campo_actividad TEXT,
    grupo_o_entidad_relacionada TEXT,
    ocupacion TEXT,
    genero TEXT,
    lengua TEXT,
    otros_nombres TEXT,
    persona_relacionada TEXT,
    fuentes_de_informacion TEXT,
    obras_relacionadas_en_el_catalogo_BNE TEXT
    );
'''

per_fts = '''
    CREATE VIRTUAL TABLE per_fts USING FTS5(
        id,
        t_100,
        t_372,
        t_374,
        t_400,
        nombre_de_persona,
        campo_actividad,
        ocupacion,
        otros_nombres,
        tokenize="unicode61 separators '|a'");

insert into per_fts (id,t_100,t_372,t_374,t_400,nombre_de_persona,campo_actividad,ocupacion,otros_nombres) select id,t_100,t_372,t_374,t_400,nombre_de_persona,campo_actividad,ocupacion,otros_nombres from per;
'''

new_mon = f'''
    CREATE TABLE mon (
    id TEXT PRIMARY KEY,
    t_001 TEXT,
    t_008 TEXT,
    t_017 TEXT,
    t_020 TEXT,
    t_024 TEXT,
    t_035 TEXT,
    t_040 TEXT,
    t_041 TEXT,
    t_080 TEXT,
    t_100 TEXT,
    t_110 TEXT,
    t_130 TEXT,
    t_245 TEXT,
    t_246 TEXT,
    t_260 TEXT,
    t_264 TEXT,
    t_300 TEXT,
    t_440 TEXT,
    t_490 TEXT,
    t_500 TEXT,
    t_504 TEXT,
    t_505 TEXT,
    t_546 TEXT,
    t_561 TEXT,
    t_586 TEXT,
    t_594 TEXT,
    t_600 TEXT,
    t_610 TEXT,
    t_611 TEXT,
    t_630 TEXT,
    t_650 TEXT,
    t_651 TEXT,
    t_653 TEXT,
    t_655 TEXT,
    t_700 TEXT,
    t_710 TEXT,
    t_740 TEXT,
    t_752 TEXT,
    t_770 TEXT,
    t_772 TEXT,
    t_773 TEXT,
    t_774 TEXT,
    t_775 TEXT,
    t_776 TEXT,
    t_777 TEXT,
    t_787 TEXT,
    t_800 TEXT,
    t_810 TEXT,
    t_811 TEXT,
    t_830 TEXT,
    t_980 TEXT,
    t_994 TEXT,
    per_id TEXT,
    pais_de_publicacion TEXT,
    lengua_principal TEXT,
    otras_lenguas TEXT,
    lengua_original TEXT,
    fecha_de_publicacion TEXT,
    decada TEXT,
    siglo TEXT,
    deposito_legal TEXT,
    isbn TEXT,
    nipo TEXT,
    cdu TEXT,
    autores TEXT,
    titulo TEXT,
    mencion_de_autores TEXT,
    otros_titulos TEXT,
    edicion TEXT,
    lugar_de_publicacion TEXT,
    editorial TEXT,
    extension TEXT,
    otras_caracteristicas_fisicas TEXT,
    dimensiones TEXT,
    material_anejo TEXT,
    serie TEXT,
    nota_de_contenido TEXT,
    notas TEXT,
    procedencia TEXT,
    premios TEXT,
    tema TEXT,
    genero_forma TEXT,
    tipo_de_documento TEXT
    );
'''

mon_fts = '''
    CREATE VIRTUAL TABLE mon_fts USING FTS5(
        id,
        t_100,
        t_245,
        tokenize="unicode61 separators '|a'");
        
    insert into mon_fts (id,t_100,t_245) select id,t_100,t_245 from mon;
'''

mon_fts_per_id = '''
    CREATE VIRTUAL TABLE mon_fts USING FTS5(
        id,
        t_100,
        t_245,
        per_id,
        tokenize="unicode61 separators '|a'");
        
    insert into mon_fts (id,t_100,t_245, per_id) select id,t_100,t_245,per_id from mon;
'''