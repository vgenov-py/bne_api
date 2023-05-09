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
CREATE TABLE IF NOT EXISTS 'per_fts_data'(id INTEGER PRIMARY KEY, block BLOB);
CREATE TABLE IF NOT EXISTS 'per_fts_idx'(segid, term, pgno, PRIMARY KEY(segid, term)) WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS 'per_fts_content'(id INTEGER PRIMARY KEY, c0, c1, c2, c3, c4, c5, c6, c7, c8);
CREATE TABLE IF NOT EXISTS 'per_fts_docsize'(id INTEGER PRIMARY KEY, sz BLOB);
CREATE TABLE IF NOT EXISTS 'per_fts_config'(k PRIMARY KEY, v) WITHOUT ROWID;
CREATE TABLE mon (
    id TEXT PRIMARY KEY,
    t_001 TEXT,
    t_008 TEXT,
    t_020 TEXT,
    t_035 TEXT,
    t_040 TEXT,
    t_100 TEXT,
    t_130 TEXT,
    t_245 TEXT,
    t_260 TEXT,
    t_300 TEXT,
    t_500 TEXT,
    t_700 TEXT,
    t_899 TEXT,
    t_927 TEXT,
    t_980 TEXT,
    t_994 TEXT,
    per_id TEXT
    );
CREATE TABLE IF NOT EXISTS 'mon_fts_data'(id INTEGER PRIMARY KEY, block BLOB);
CREATE TABLE IF NOT EXISTS 'mon_fts_idx'(segid, term, pgno, PRIMARY KEY(segid, term)) WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS 'mon_fts_content'(id INTEGER PRIMARY KEY, c0, c1, c2);
CREATE TABLE IF NOT EXISTS 'mon_fts_docsize'(id INTEGER PRIMARY KEY, sz BLOB);
CREATE TABLE IF NOT EXISTS 'mon_fts_config'(k PRIMARY KEY, v) WITHOUT ROWID;
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
CREATE INDEX per_id on per(id);
CREATE INDEX per_375 on per(t_375);
CREATE INDEX per_genero on per(genero);
CREATE INDEX mon_id on mon(id);
CREATE INDEX mon_t100 on mon(t_100);
CREATE INDEX mon_t245 on mon(t_245);
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
        tokenize="unicode61 separators '|a'")
/* per_fts(id,t_100,t_372,t_374,t_400,nombre_de_persona,campo_actividad,ocupacion,otros_nombres) */;
CREATE VIRTUAL TABLE mon_fts USING FTS5(
        id,
        t_100,
        t_245,
        tokenize="unicode61 separators '|a'")
/* mon_fts(id,t_100,t_245) */;
