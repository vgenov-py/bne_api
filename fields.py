fields = {
    "geo": [],
    "per":
    [
        {
            "name":"otros_identificadores",
            "t": "024",
            "description": "Identificadores de la persona en otros catálogos (viaf, lcnf, isni, etc.)",
            "t_description": "$2: $a"
        },
        {
            "name": "fecha_nacimiento",
            "t": "046",
            "description": "Fecha de nacimiento de la persona",
            "t_description": "Sólo contenido de $f"
        },
        {
            "name": "fecha_muerte",
            "t": "_2046",
            "description": "Fecha de muerte de la persona",
            "t_description": "Sólo contenido de $g"
        },
        {
            "name": "nombre_de_persona",
            "t": "100",
            "description": "Nombre de persona",
            "t_description": "$a{$b$c}($d)($q)"
        },
        {
            "name": "otros_atributos_persona",
            "t": "368",
            "description": "Título, cargo, etc. ",
            "t_description": "sólo contenido de $c$d"
        },
        {
            "name": "lugar_nacimiento",
            "t": "370",
            "description": "País, región, provincia y localidad donde ha nacido la persona",
            "t_description": "Sólo contenido de $a"
        },
        {
            "name": "lugar_muerte",
            "t": "_2370",
            "description": "País, región, provincia y localidad donde ha fallecido la persona",
            "t_description": "Sólo contenido de $b"
        },
        {
            "name": "pais_relacionado",
            "t": "_3370",
            "description": "Otro país relacionado con la persona",
            "t_description": "$c"
        },
        {
            "name": "otros_lugares_relacionados",
            "t": "_4370",
            "description": "Otros lugares relacionados con la persona",
            "t_description": "$f"
        },
        {
            "name": "lugar_residencia",
            "t": "_5370",
            "description": "Lugar de residencia de la persona, si es especialmente significativo",
            "t_description": "$e"
        },
        {
            "name": "campo_actividad",
            "t": "372",
            "description": "Disciplina o actividad a la que se dedica la persona",
            "t_description": "Sólo contenido de $a"
        },
        {
            "name": "grupo_o_entidad relacionada",
            "t": "373, 510",
            "description": "Grupo, organismo, etc., a la que pertenece la persona",
            "t_description": "373, sólo contenido de $a; 510, $a$b"
        },
        {
            "name": "ocupacion",
            "t": "374",
            "description": "Profesión desempeñada por la persona",
            "t_description": "Sólo contenido de $a"
        },
        {
            "name": "genero",
            "t": "375",
            "description": "Género de la persona (masculino, femenino u otros)",
            "t_description": "Sólo contenido de $a"
        },
        {
            "name": "lengua",
            "t": "377",
            "description": "Lengua en la que la persona escribe la mayor parte de su obra",
            "t_description": "Sólo contenido de $l"
        },
        {
            "name": "otros_nombres",
            "t": "400",
            "description": "Otros nombres por los que es conocida la persona",
            "t_description": "$a{$b$c}($d)($q)"
        },
        {
            "name": "persona_relacionada",
            "t": "500",
            "description": "Otras personas relacionadas con la persona",
            "t_description": "$a{$b$c}($d)($q)"
        },
        {
            "name": "nota_general",
            "t": "667",
            "description": "Más información sobre la persona",
            "t_description": "$a{$b$c}($d)($q)"
        },
        {
            "name": "fuentes_de_informacion",
            "t": "670",
            "description": "Fuentes de información de las que se han obtenido los datos de la persona",
            "t_description": "$a: $b ($u))"
        },
        {
            "name": "otros_datos_biográficos",
            "t": "678",
            "description": "Otra información biográfica de la persona",
            "t_description": "$a: $b ($u))"
        },
    ],
    "mon": [
        {
            "name": "pais_de_publicacion",
            "t": "008",
            "description": "País donde se ha publicado la monografía",
            "t_description": "008:15-17"
        },
        {
            "name": "lengua_principal",
            "t": "_2008, 041",
            "description": "Lengua del contenido principal del documento",
            "t_description": "008:35-37, 041: $a"
        },
        {
            "name": "otras_lenguas",
            "t": "_1041",
            "description": "Lenguas de otros contenidos (resúmenes, tablas de contenidos, notas, etc.)",
            "t_description": "$b, $d, $f,$j,$k"
        },
        {
            "name": "lengua_original",
            "t": "_2041",
            "description": "Lengua original de la que se ha traducido",
            "t_description": "$h"
        },
        {
            "name": "fecha_de_publicacion",
            "t": "_3008",
            "description": "Fecha en que se publicó la monografía o su primera entrega en caso de una monografía en varias partes",
            "t_description": "008/7-10"
        },
        {
            "name": "decada",
            "t": "_4008",
            "description": "Década en la que se publicó la monografía o su primera entrega en caso de una monografía en varias partes",
            "t_description": "A partir de fecha_de_publicacion"
        },
        {
            "name": "siglo",
            "t": "_5008",
            "description": "Siglo en el  que se publicó la monografía o su primera entrega en caso de una monografía en varias partes",
            "t_description": "A partir de fecha_de_publicacion"
        },
        {
            "name": "deposito_legal",
            "t": "017",
            "description": "Número de Depósito Legal",
            "t_description": "$a"
        },
        {
            "name": "isbn",
            "t": "020",
            "description": "International Standard Book Number",
            "t_description": "$a ($q) "
        },
        {
            "name": "nipo",
            "t": "024",
            "description": "Número de Identificación de Publicaciones Oficiales",
            "t_description": "$a ($q) "
        },
        {
            "name": "cdu",
            "t": "080",
            "description": "Número de la Clasificación Decimal Universalque representa el tema tratado en la monografía",
            "t_description": "Sólo contenido de $a"
        },
        {
            "name": "autores",
            "t": "100, 110, 700, 710",
            "description": "Responsables del contenido intelectual de la monografía",
            "t_description": "$a{$b$c}($d)($q)($e)"
        },
        {
            "name": "titulo",
            "t": "245",
            "description": "Título de la obra tal y como aparece citado en la monografía",
            "t_description": "$a:$b.$n,$p"
        },
        {
            "name": "mencion_de_autores",
            "t": "_2245",
            "description": "Responsables del contenido intelectual tal y como aparecen citados en la monografía",
            "t_description": "$c"
        },
        {
            "name": "otros_titulos",
            "t": "246, 740",
            "description": "Otros títulos de la obra que aparecen citados en la monografía",
            "t_description": "246: [$i]:$a:$b.$n,$p 740: $a$n, $p"
        },
        {
            "name": "edicion",
            "t": "250",
            "description": "Información sobre la edición",
            "t_description": "$a,$b"
        },
        {
            "name": "lugar_de_publicacion",
            "t": "260, 264",
            "description": "Localidad específica en la que se ha publicado la monografía",
            "t_description": "$a"
        },
        {
            "name": "editorial",
            "t": "_2260, 264",
            "description": "Nombre del editor responsable de la publicación de la monografía",
            "t_description": "$b"
        },
        {
            "name": "extension",
            "t": "300",
            "description": "Número de volúmenes, páginas, hojas, columnas, etc.",
            "t_description": "$a"
        },
        {
            "name": "otras_caracteristicas_fisicas",
            "t": "_2300",
            "description": "Ilustraciones, color, etc.",
            "t_description": "$b"
        },
        {
            "name": "dimensiones",
            "t": "_3300",
            "description": "Medida del alto de la publicación (en cm)",
            "t_description": "$c"
        },
        {
            "name": "material_anejo",
            "t": "_4300",
            "description": "Material complementario que acompaña a la publicación principal",
            "t_description": "$e"
        },
        {
            "name": "serie",
            "t": "440, 490",
            "description": "Colección a la que pertenece la monografía",
            "t_description": "$a$v"
        },
        {
            "name": "nota_de_contenido",
            "t": "505",
            "description": "Más información sobre el contenido de la obra",
            "t_description": "$a"
        },
        {
            "name": "notas",
            "t": "500, 504, 546, 563, 594",
            "description": "Más información sobre la monografía",
            "t_description": "$a"
        },
        {
            "name": "procedencia",
            "t": "561",
            "description": "Nombre del último propietario del ejemplar antes de pasar a la BNE",
            "t_description": "$a"
        },
        {
            "name": "premios",
            "t": "586",
            "description": "Premios con los que ha sido galardonada la obra",
            "t_description": "$a"
        },
        {
            "name": "tema",
            "t": "600, 610, 611, 630, 650, 651, 653",
            "description": "Materia sobre la que trata la monografía",
            "t_description": "Todos los subbcampos menos $2 subcampos separados por guiones"
        },
        {
            "name": "genero_forma",
            "t": "655",
            "description": "Género al que pertenece la obra y forma que toma",
            "t_description": "Todos los subbcampos menos $2 subcampos separados por guiones"
        },
        {
            "name": "tipo_ de_documento",
            "t": "994",
            "description": "MONOMODER",
            "t_description": '"si $aMONOMODER: "Monografía en papel (posterior a 1830)" ∂si $aMONOMODER-RECELE: "Monografía electrónica""',
        }
    ],
    "ent": [
        {
            "name": "otros_identificadores",
            "t": "024",
            "description": "Identificadores de la entidad en otros catálogos (viaf, lcnf, isni, etc.)",
            "t_description": "$2: $a ",
        },
        {
            "name": "fecha_establecimiento",
            "t": "046",
            "description": "Fecha de creación o inicio de actividad de la entidad",
            "t_description": "Si hay  $q: sólo $q (aunque haya más $) Si no hay $q, $s si lo hay",
        },
        {
            "name": "fecha_finalizacion",
            "t": "_2046",
            "description": "Fecha de desapaprición o cese de actividad de la entidad",
            "t_description": "Si hay  $r: sólo $r (aunque haya más $) Si no hay $r, $t si lo hay",
        },
        {
            "name": "nombre_de_entidad",
            "t": "110",
            "description": "Nombre de la entidad corporativa",
            "t_description": "$a,$b, $b...($e)",
        },
        {
            "name": "tipo_entidad",
            "t": "368",
            "description": "tipo de entidad corporativa",
            "t_description": "Sólo contenido de $a",
        },
        {
            "name": "pais",
            "t": "370",
            "description": "País relacionado con la entidad",
            "t_description": "Sólo contenido de $c",
        },
        {
            "name": "sede",
            "t": "_2370",
            "description": "Lugar donde se encuentra la sede de la entidad, si es especialmente significativo",
            "t_description": "Sólo contenido de $e",
        },
        {
            "name": "campo_actividad",
            "t": "372",
            "description": "Disciplina o actividad a la que se dedica la entidad",
            "t_description": "Sólo contenido de $a",
        },
        {
            "name": "lengua",
            "t": "377",
            "description": "Lengua en la que la entidad suele publicar",
            "t_description": "Sólo contenido de $l",
        },
        {
            "name": "otros_nombres",
            "t": "410",
            "description": "Otros nombres por los que es conocida la entidad",
            "t_description": "$a,$b, $b...($e)",
        },
        {
            "name": "persona_relacionada",
            "t": "500",
            "description": "Personas relacionadas con la entidad",
            "t_description": "$a{$b$c}($d)($q)",
        },
        {
            "name": "grupo_o_entidad_relacionada",
            "t": "510",
            "description": "Grupo, organismo, etc., relacionado con la entidad",
            "t_description": "$a,$b, $b...($e)",
        },
        {
            "name": "nota_de_relacion",
            "t": "663",
            "description": "Otras relaciones de la entidad con personas, otras entidades, etc.",
            "t_description": "$a $b(puede haber varios $b",
        },
        {
            "name": "otros_datos_historicos",
            "t": "665, 678",
            "description": "Otra información histórica de la entidad",
            "t_description": "Sólo contenido de $a",
        },
        {
            "name": "nota_general",
            "t": "667",
            "description": "Más información sobre la entidad",
            "t_description": "Sólo contenido de $a",
        },
        {
            "name": "fuentes_de_informacion",
            "t": "670",
            "description": "Fuentes de información de las que se han obtenido los datos de la entidad",
            "t_description": "$a: $b ($u)",
        },
        {
            "name": "otros_datos_historicos",
            "t": "_2678",
            "description": "Sólo contenido de $a",
            "t_description": "otra información histórica de la entidad",
        }
    ]
}
