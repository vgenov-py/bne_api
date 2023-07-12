from constants import DB_FILE
import sqlite3
from flask import g
import re
from uuid import uuid4
import msgspec
from typing import Optional
import datetime as dt
import orjson as json
import time
import csv

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_FILE)
    return db

'''
FOR TESTING PURPOSE:
'''
# def get_db():
#     return sqlite3.connect(DB_FILE)

countries = {'': '', 'aa': 'Albania', 'abc': 'Alberta', 'ac': 'Islas Ashmore y Cartier', 'aca': 'Territorio de la Capital Australiana', 'ae': 'Argelia', 'af': 'Afganistán', 'ag': 'Argentina', 'ai': 'Armenia (República)', 'air': 'RSS de Armenia', 'aj': 'Azerbaiyán', 'ajr': 'RSS de Azerbaiyán', 'aku': 'Alaska', 'alu': 'Alabama', 'am': 'Anguila', 'an': 'Andorra', 'ao': 'Angola', 'aq': 'Antigua y Barbuda', 'aru': 'Arkansas', 'as': 'Samoa Americana', 'at': 'Australia', 'au': 'Austria', 'aw': 'Aruba', 'ay': 'Antártida', 'azu': 'Arizona', 'ba': 'Baréin', 'bb': 'Barbados', 'bcc': 'Columbia Británica', 'bd': 'Burundi', 'be': 'Bélgica', 'bf': 'Bahamas', 'bg': 'Bangladés', 'bh': 'Belice', 'bi': 'Territorio Británico del Océano Índico', 'bl': 'Brasil', 'bm': 'Islas Bermudas', 'bn': 'Bosnia y Herzegovina', 'bo': 'Bolivia', 'bp': 'Islas Salomón', 'br': 'Birmania', 'bs': 'Botsuana', 'bt': 'Bután', 'bu': 'Bulgaria', 'bv': 'Isla Bouvet', 'bw': 'Bielorrusia', 'bwr': 'RSS de Bielorrusia', 'bx': 'Brunéi', 'ca': 'Países Bajos Caribeños', 'cau': 'California', 'cb': 'Camboya', 'cc': 'China', 'cd': 'Chad', 'ce': 'Sri Lanka', 'cf': 'Congo (Brazzaville)', 'cg': 'Congo (República Democrática)', 'ch': 'China (República: 1949- )', 'ci': 'Croacia', 'cj': 'Islas Caimán', 'ck': 'Colombia', 'cl': 'Chile', 'cm': 'Camerún', 'cn': 'Canadá', 'co': 'Curazao', 'cou': 'Colorado', 'cp': 'Islas de Cantón y Enderbury', 'cq': 'Comoras', 'cr': 'Costa Rica', 'cs': 'Checoslovaquia', 'ctu': 'Connecticut', 'cu': 'Cuba', 'cv': 'Cabo Verde', 'cw': 'Islas Cook', 'cx': 'República Centroafricana', 'cy': 'Chipre', 'cz': 'Zona del Canal', 'dcu': 'Distrito de Columbia', 'deu': 'Delaware', 'dk': 'Dinamarca', 'dm': 'Benín', 'dq': 'Dominica', 'dr': 'República Dominicana', 'ea': 'Eritrea', 'ec': 'Ecuador', 'eg': 'Guinea Ecuatorial', 'em': 'Timor Oriental', 'enk': 'Inglaterra', 'er': 'Estonia', 'err': 'Estonia', 'es': 'El Salvador', 'et': 'Etiopía', 'fa': 'Islas Feroe', 'fg': 'Guayana Francesa', 'fi': 'Finlandia', 'fj': 'Fiyi', 'fk': 'Islas Malvinas', 'flu': 'Florida', 'fm': 'Estados Federados de Micronesia', 'fp': 'Polinesia Francesa', 'fr': 'Francia', 'fs': 'Tierras Australes y Antárticas Francesas', 'ft': 'Yibuti', 'gau': 'Georgia', 'gb': 'Kiribati', 'gd': 'Granada', 'ge': 'Alemania Oriental', 'gg': 'Guernsey', 'gh': 'Ghana', 'gi': 'Gibraltar', 'gl': 'Groenlandia', 'gm': 'Gambia', 'gn': 'Islas Gilbert y Ellice', 'go': 'Gabón', 'gp': 'Guadalupe', 'gr': 'Grecia', 'gs': 'Georgia (República)', 'gsr': 'RSS de Georgia', 'gt': 'Guatemala', 'gu': 'Guam', 'gv': 'Guinea', 'gw': 'Alemania', 'gy': 'Guyana', 'gz': 'Franja de Gaza', 'hiu': 'Hawái', 'hk': 'Hong Kong', 'hm': 'Islas Heard y McDonald', 'ho': 'Honduras', 'ht': 'Haití', 'hu': 'Hungría', 'iau': 'Iowa', 'ic': 'Islandia', 'idu': 'Idaho', 'ie': 'Irlanda', 'ii': 'India', 'ilu': 'Illinois', 'im': 'Isla de Man', 'inu': 'Indiana', 'io': 'Indonesia', 'iq': 'Irak', 'ir': 'Irán', 'is': 'Israel', 'it': 'Italia', 'iu': 'Zonas Desmilitarizadas de Israel y Siria', 'iv': 'Costa de Marfil', 'iw': 'Zonas Desmilitarizadas de Israel y Jordania', 'iy': 'Zona Neutral de Irak y Arabia Saudita', 'ja': 'Japón', 'je': 'Jersey', 'ji': 'Atolón Johnston', 'jm': 'Jamaica', 'jn': 'Jan Mayen', 'jo': 'Jordania', 'ke': 'Kenia', 'kg': 'Kirguistán', 'kgr': 'RSS de Kirguistán', 'kn': 'Corea del Norte', 'ko': 'Corea del Sur', 'ksu': 'Kansas', 'ku': 'Kuwait', 'kv': 'Kosovo', 'kyu': 'Kentucky', 'kz': 'Kazajistán', 'kzr': 'RSS de Kazajistán', 'lau': 'Luisiana', 'lb': 'Liberia', 'le': 'Líbano', 'lh': 'Liechtenstein', 'li': 'Lituania', 'lir': 'Lituania', 'ln': 'Islas del Sur y Central', 'lo': 'Lesoto', 'ls': 'Laos', 'lu': 'Luxemburgo', 'lv': 'Letonia', 'lvr': 'Letonia', 'ly': 'Libia', 'mau': 'Massachusetts', 'mbc': 'Manitoba', 'mc': 'Mónaco', 'mdu': 'Maryland', 'meu': 'Maine', 'mf': 'Mauricio', 'mg': 'Madagascar', 'mh': 'Macao', 'miu': 'Míchigan', 'mj': 'Montserrat', 'mk': 'Omán', 'ml': 'Malí', 'mm': 'Malta', 'mnu': 'Minnesota', 'mo': 'Montenegro', 'mou': 'Misuri', 'mp': 'Mongolia', 'mq': 'Martinica', 'mr': 'Marruecos', 'msu': 'Misisipi', 'mtu': 'Montana', 'mu': 'Mauritania', 'mv': 'Moldavia', 'mvr': 'RSS de Moldavia', 'mw': 'Malaui', 'mx': 'México', 'my': 'Malasia', 'mz': 'Mozambique', 'na': 'Antillas Neerlandesas', 'nbu': 'Nebraska', 'ncu': 'Carolina del Norte', 'ndu': 'Dakota del Norte', 'ne': 'Países Bajos', 'nfc': 'Terranova y Labrador', 'ng': 'Níger', 'nhu': 'Nuevo Hampshire', 'nik': 'Irlanda del Norte', 'nju': 'Nueva Jersey', 'nkc': 'Nuevo Brunswick', 'nl': 'Nueva Caledonia', 'nm': 'Islas Marianas del Norte', 'nmu': 'Nuevo México', 'nn': 'Vanuatu', 'no': 'Noruega', 'np': 'Nepal', 'nq': 'Nicaragua', 'nr': 'Nigeria', 'nsc': 'Nueva Escocia', 'ntc': 'Territorios del Noroeste', 'nu': 'Nauru', 'nuc': 'Nunavut', 'nvu': 'Nevada', 'nw': 'Islas Marianas del Norte', 'nx': 'Isla Norfolk', 'nyu': 'Estado de Nueva York', 'nz': 'Nueva Zelanda', 'ohu': 'Ohio', 'oku': 'Oklahoma', 'onc': 'Ontario', 'oru': 'Oregón', 'ot': 'Mayotte', 'pau': 'Pensilvania', 'pc': 'Isla Pitcairn', 'pe': 'Perú', 'pf': 'Islas Paracel', 'pg': 'Guinea-Bisáu', 'ph': 'Filipinas', 'pic': 'Isla del Príncipe Eduardo', 'pk': 'Pakistán', 'pl': 'Polonia', 'pn': 'Panamá', 'po': 'Portugal', 'pp': 'Papúa Nueva Guinea', 'pr': 'Puerto Rico', 'pt': 'Timor Portugués', 'pw': 'Palaos', 'py': 'Paraguay', 'qa': 'Catar', 'qea': 'Queensland', 'quc': 'Quebec (Provincia)', 'rb': 'Serbia', 're': 'Reunión', 'rh': 'Zimbabue', 'riu': 'Rhode Island', 'rm': 'Rumania', 'ru': 'Federación Rusa', 'rur': 'RSS de la URSS', 'rw': 'Ruanda', 'ry': 'Islas Ryukyu, Sur', 'sa': 'Sudáfrica', 'sb': 'Svalbard', 'sc': 'San Bartolomé', 'scu': 'Carolina del Sur', 'sd': 'Sudán del Sur', 'sdu': 'Dakota del Sur', 'se': 'Seychelles', 'sf': 'Santo Tomé y Príncipe', 'sg': 'Senegal', 'sh': 'África del Norte Española', 'si': 'Singapur', 'sj': 'Sudán', 'sk': 'Sikkim', 'sl': 'Sierra Leona', 'sm': 'San Marino', 'sn': 'Sint Maarten', 'snc': 'Saskatchewan', 'so': 'Somalia', 'sp': 'España', 'sq': 'Esuatini', 'sr': 'Surinam', 'ss': 'Sáhara Occidental', 'st': 'San Martín', 'stk': 'Escocia', 'su': 'Arabia Saudita', 'sv': 'Islas Swan', 'sw': 'Suecia', 'sx': 'Namibia', 'sy': 'Siria', 'sz': 'Suiza', 'ta': 'Tayikistán', 'tar': 'RSS de Tayikistán', 'tc': 'Islas Turcas y Caicos', 'tg': 'Togo', 'th': 'Tailandia', 'ti': 'Túnez', 'tk': 'Turkmenistán', 'tkr': 'RSS de Turkmenistán', 'tl': 'Tokelau', 'tma': 'Tasmania', 'tnu': 'Tennessee', 'to': 'Tonga', 'tr': 'Trinidad y Tobago', 'ts': 'Emiratos Árabes Unidos', 'tt': 'Territorio en Fideicomiso de las Islas del Pacífico', 'tu': 'Turquía', 'tv': 'Tuvalu', 'txu': 'Texas', 'tz': 'Tanzania', 'ua': 'Egipto', 'uc': 'Islas del Caribe de Estados Unidos', 'ug': 'Uganda', 'ui': 'Islas Varias del Reino Unido', 'uik': 'Islas Varias del Reino Unido', 'uk': 'Reino Unido', 'un': 'Ucrania', 'unr': 'Ucrania', 'up': 'Islas Varias del Pacífico de Estados Unidos', 'ur': 'Unión Soviética', 'us': 'Estados Unidos', 'utu': 'Utah', 'uv': 'Burkina Faso', 'uy': 'Uruguay', 'uz': 'Uzbekistán', 'uzr': 'RSS de Uzbekistán', 'vau': 'Virginia.', 'vb': 'Islas Vírgenes Británicas', 'vc': 'Ciudad del Vaticano', 've': 'Venezuela', 'vi': 'Islas Vírgenes de los Estados Unidos', 'vm': 'Vietnam', 'vn': 'Vietnam del Norte', 'vp': 'Varios lugares', 'vra': 'Victoria', 'vs': 'Vietnam del Sur', 'vtu': 'Vermont', 'wau': 'Estado de Washington', 'wb': 'Berlín Oeste', 'wea': 'Australia Occidental', 'wf': 'Wallis y Futuna', 'wiu': 'Wisconsin', 'wj': 'Margen Occidental del Río Jordán', 'wk': 'Isla Wake', 'wlk': 'Gales', 'ws': 'Samoa', 'wvu': 'Virginia Occidental', 'wyu': 'Wyoming', 'xa': 'Isla de Navidad (Océano Índico)', 'xb': 'Islas Cocos (Keeling)', 'xc': 'Maldivas', 'xd': 'San Cristóbal y Nieves', 'xe': 'Islas Marshall', 'xf': 'Islas Midway', 'xga': 'Territorio de las Islas del Mar del Coral', 'xh': 'Niue', 'xi': 'San Cristóbal y Nieves-Anguila', 'xj': 'Santa Elena', 'xk': 'Santa Lucía', 'xl': 'San Pedro y Miquelón', 'xm': 'San Vicente y las Granadinas', 'xn': 'Macedonia del Norte', 'xna': 'Nueva Gales del Sur', 'xo': 'Eslovaquia', 'xoa': 'Territorio del Norte', 'xp': 'Isla Spratly', 'xr': 'República Checa', 'xra': 'Australia Meridional', 'xs': 'Islas Georgias del Sur y Sandwich del Sur', 'xv': 'Eslovenia', 'xx': 'Sin lugar, desconocido o indeterminado', 'xxc': 'Canadá', 'xxk': 'Islas varias del Reino Unido', 'xxr': 'Unión Soviética', 'xxu': 'Estados Unidos', 'ye': 'Yemen', 'ykc': 'Territorio de Yukón', 'ys': 'Yemen (República Democrática Popular)', 'yu': 'Serbia y Montenegro', 'za': 'Zambia'}        
languages = {'': '', 'aar': 'Afar', 'abk': 'abjasio', 'ace': 'achinés', 'ach': 'acoli', 'ada': 'adangme', 'ady': 'adigué', 'afa': 'afroasiático (otros)', 'afh': 'afrihili (lengua artificial)', 'afr': 'afrikáans', 'ain': 'ainu', 'ajm': 'aljamía', 'aka': 'akan', 'akk': 'acadio', 'alb': 'albanés', 'ale': 'aleutiano', 'alg': 'algonquino (otros)', 'alt': 'altai', 'amh': 'amárico', 'ang': 'inglés antiguo (ca. 450-1100)', 'anp': 'angika', 'apa': 'lenguas apache', 'ara': 'árabe', 'arc': 'arameo', 'arg': 'aragonés', 'arm': 'armenio', 'arn': 'mapuche', 'arp': 'arapaho', 'art': 'artificial (otros)', 'arw': 'arahuaco', 'asm': 'asamés', 'ast': 'bable', 'ath': 'atapascos (otros)', 'aus': 'lenguas australianas', 'ava': 'ávaro', 'ave': 'avéstico', 'awa': 'awadhi', 'aym': 'aimara', 'aze': 'azerí', 'bad': 'lenguas banda', 'bai': 'lenguas bamileke', 'bak': 'bashkir', 'bal': 'baluchi', 'bam': 'bambara', 'ban': 'balinés', 'baq': 'vasco', 'bas': 'basa', 'bat': 'báltico (otros)', 'bej': 'beja', 'bel': 'bielorruso', 'bem': 'bemba', 'ben': 'bengalí', 'ber': 'bereber (otros)', 'bho': 'bhojpuri', 'bih': 'bihari (otros)', 'bik': 'bikol', 'bin': 'edo', 'bis': 'bislama', 'bla': 'siksika', 'bnt': 'bantú (otros)', 'bos': 'bosnio', 'bra': 'braj', 'bre': 'bretón', 'btk': 'batak', 'bua': 'buriat', 'bug': 'bugis', 'bul': 'búlgaro', 'bur': 'birmano', 'byn': 'bilin', 'cad': 'caddo', 'cai': 'indio centroamericano (otros)', 'cam': 'jemer', 'car': 'caribe', 'cat': 'catalán', 'cau': 'caucásico (otros)', 'ceb': 'cebuano', 'cel': 'céltico (otros)', 'cha': 'chamorro', 'chb': 'chibcha', 'che': 'checheno', 'chg': 'chagatai', 'chi': 'chino', 'chk': 'chuukés', 'chm': 'mari', 'chn': 'jerga chinook', 'cho': 'choctaw', 'chp': 'chipewyan', 'chr': 'cheroqui', 'chu': 'eslavo eclesiástico', 'chv': 'chuvasio', 'chy': 'cheyenne', 'cmc': 'lenguas cham', 'cnr': 'montenegrino', 'cop': 'copto', 'cor': 'córnico', 'cos': 'corso', 'cpe': 'criollos y pidgins basados en el inglés (otros)', 'cpf': 'criollos y pidgins basados en el francés (otros)', 'cpp': 'criollos y pidgins basados en el portugués (otros)', 'cre': 'cree', 'crh': 'tártaro de Crimea', 'crp': 'criollos y pidgins (otros)', 'csb': 'casubio', 'cus': 'cushita (otros)', 'cze': 'checo', 'dak': 'dakota', 'dan': 'danés', 'dar': 'dargwa', 'day': 'dayak', 'del': 'delaware', 'den': 'slavey', 'dgr': 'dogrib', 'din': 'dinka', 'div': 'divehi', 'doi': 'dogri', 'dra': 'dravidiano (otros)', 'dsb': 'sorbio inferior', 'dua': 'duala', 'dum': 'neerlandés medio (ca. 1050-1350)', 'dut': 'neerlandés', 'dyu': 'dyula', 'dzo': 'dzongkha', 'efi': 'efik', 'egy': 'egipcio', 'eka': 'ekajuk', 'elx': 'elamita', 'eng': 'inglés', 'enm': 'inglés medio (1100-1500)', 'epo': 'esperanto', 'esk': 'lenguas esquimales', 'esp': 'esperanto', 'est': 'estonio', 'eth': 'etiópico', 'ewe': 'ewe', 'ewo': 'ewondo', 'fan': 'fang', 'fao': 'feroés', 'far': 'feroés', 'fat': 'fanti', 'fij': 'fiyiano', 'fil': 'filipino', 'fin': 'finlandés', 'fiu': 'fino-ugrio (otros)', 'fon': 'fon', 'fre': 'francés', 'fri': 'frisón', 'frm': 'francés medio (ca. 1300-1600)', 'fro': 'francés antiguo (ca. 842-1300)', 'frr': 'frisón septentrional', 'frs': 'frisón oriental', 'fry': 'frisón', 'ful': 'fula', 'fur': 'friulano', 'gaa': 'gã', 'gae': 'gaélico escocés', 'gag': 'gallego', 'gal': 'oromo', 'gay': 'gayo', 'gba': 'gbaya', 'gem': 'germánico (otros)', 'geo': 'georgiano', 'ger': 'alemán', 'gez': 'etiópico', 'gil': 'gilbertés', 'gla': 'gaélico escocés', 'gle': 'irlandés', 'glg': 'gallego', 'glv': 'manés', 'gmh': 'alemán medio alto (ca. 1050-1500)', 'goh': 'alemán antiguo alto (ca. 750-1050)', 'gon': 'gondi', 'gor': 'gorontalo', 'got': 'gótico', 'grb': 'grebo', 'grc': 'griego antiguo (hasta 1453)', 'gre': 'griego moderno (1453-)', 'grn': 'guaraní', 'gsw': 'alemán suizo', 'gua': 'guaraní', 'guj': 'guyaratí', 'gwi': "gwich'in", 'hai': 'haida', 'hat': 'criollo francés haitiano', 'hau': 'hausa', 'haw': 'hawaiano', 'heb': 'hebreo', 'her': 'herero', 'hil': 'hiligaynon', 'him': 'lenguas pahari occidentales', 'hin': 'hindi', 'hit': 'hitita', 'hmn': 'hmong', 'hmo': 'hiri motu', 'hrv': 'croata', 'hsb': 'alto sorbio', 'hun': 'húngaro', 'hup': 'hupa', 'iba': 'iban', 'ibo': 'igbo', 'ice': 'islandés', 'ido': 'ido', 'iii': 'yi de sichuán', 'ijo': 'ijo', 'iku': 'inuktitut', 'ile': 'interlingue', 'ilo': 'ilocano', 'ina': 'interlingua (Asociación de la Lengua Auxiliar Internacional)', 'inc': 'índico (otros)', 'ind': 'indonesio', 'ine': 'indoeuropeo (otros)', 'inh': 'ingush', 'int': 'interlingua (Asociación Lingüística Internacional Auxiliar)', 'ipk': 'inupiaq', 'ira': 'iraní (otros)', 'iri': 'irlandés', 'iro': 'iroquiano (otros)', 'ita': 'italiano', 'jav': 'javanés', 'jbo': 'lojban (lengua artificial)', 'jpn': 'japonés', 'jpr': 'judeo-persa', 'jrb': 'judeo-árabe', 'kaa': 'karakalpako', 'kab': 'cabila', 'kac': 'kachin', 'kal': 'kalaallisut', 'kam': 'kamba', 'kan': 'kannada', 'kar': 'lenguas karen', 'kas': 'cachemiro', 'kau': 'kanuri', 'kaw': 'kawi', 'kaz': 'kazajo', 'kbd': 'cabardiano', 'kha': 'khasi', 'khi': 'khoisan (otros)', 'khm': 'jemer', 'kho': 'hotanés', 'kik': 'kikuyu', 'kin': 'kinyarwanda', 'kir': 'kirguís', 'kmb': 'kimbundu', 'kok': 'konkani', 'kom': 'komi', 'kon': 'kongo', 'kor': 'coreano', 'kos': 'kosraeano', 'kpe': 'kpelle', 'krc': 'karachay-bálcaro', 'krl': 'carelio', 'kro': 'kru (otros)', 'kru': 'kurukh', 'kua': 'kuanyama', 'kum': 'kumyk', 'kur': 'kurdo', 'kus': 'kusaie', 'kut': 'kootenai', 'lad': 'ladino', 'lah': 'lahndā', 'lam': 'lamba (Zambia y Congo)', 'lan': 'occitano (después de 1500)', 'lao': 'lao', 'lap': 'sami', 'lat': 'latín', 'lav': 'letón', 'lez': 'lezgiano', 'lim': 'limburgués', 'lin': 'lingala', 'lit': 'lituano', 'lol': 'mongo-nkundu', 'loz': 'lozi', 'ltz': 'luxemburgués', 'lua': 'luba-lulua', 'lub': 'luba-katanga', 'lug': 'ganda', 'lui': 'luiseño', 'lun': 'lunda', 'luo': 'luo (Kenia y Tanzania)', 'lus': 'lushai', 'mac': 'macedonio', 'mad': 'madurés', 'mag': 'magahi', 'mah': 'marshalés', 'mai': 'maithili', 'mak': 'makasar', 'mal': 'malayalam', 'man': 'mandingo', 'mao': 'maorí', 'map': 'austronesio (otros)', 'mar': 'marathi', 'mas': 'masái', 'max': 'manés', 'may': 'malayo', 'mdf': 'moksha', 'mdr': 'mandar', 'men': 'mende', 'mga': 'irlandés medio (ca. 1100-1550)', 'mic': 'micmac', 'min': 'minangkabau', 'mis': 'lenguas varias', 'mkh': 'mon-jemer (otros)', 'mla': 'malgache', 'mlg': 'malgache', 'mlt': 'maltés', 'mnc': 'manchú', 'mni': 'manipuri', 'mno': 'lenguas manobo', 'moh': 'mohawk', 'mol': 'moldavo', 'mon': 'mongol', 'mos': 'mooré', 'mul': 'varios idiomas', 'mun': 'munda (otros)', 'mus': 'creek', 'mwl': 'mirandés', 'mwr': 'marwari', 'myn': 'lenguas mayas', 'myv': 'erzya', 'nah': 'náhuatl', 'nai': 'indio norteamericano (otros)', 'nap': 'italiano napolitano', 'nau': 'nauruano', 'nav': 'navajo', 'nbl': 'ndebele (Sudáfrica)', 'nde': 'ndebele (Zimbabue)', 'ndo': 'ndonga', 'nds': 'bajo alemán', 'nep': 'nepalí', 'new': 'newari', 'nia': 'nias', 'nic': 'nigerocongo (otros)', 'niu': 'niueano', 'nno': 'noruego (nynorsk)', 'nob': 'noruego (bokmål)', 'nog': 'nogai', 'non': 'nórdico antiguo', 'nor': 'noruego', 'nqo': "n'ko", 'nso': 'sotho septentrional', 'nub': 'nilo-sahariano (otros)', 'nwc': 'newari antiguo', 'nya': 'nyanya', 'nym': 'nyamwesi', 'nyn': 'nyankole', 'nyo': 'nyoro', 'nzi': 'nzima', 'oci': 'occitano (después de 1500)', 'oji': 'ojibwa', 'ori': 'oriya', 'orm': 'oromo', 'osa': 'osage', 'oss': 'osetio', 'ota': 'turco otomano', 'oto': 'lenguas otomí', 'paa': 'papú (otros)', 'pag': 'pangasinán', 'pal': 'pahleví', 'pam': 'pampanga', 'pan': 'punjabi', 'pap': 'papiamento', 'pau': 'palauano', 'peo': 'persa antiguo (ca. 600-400 a.C.)', 'per': 'persa', 'phi': 'filipino (otros)', 'phn': 'fenicio', 'pli': 'pali', 'pol': 'polaco', 'pon': 'pohnpeiano', 'por': 'portugués', 'pra': 'prácrito', 'pro': 'provenzal (hasta 1500)', 'pus': 'pashto', 'que': 'quechua', 'raj': 'rajasthani', 'rap': 'rapanui', 'rar': 'rarotongano', 'roa': 'romance (otros)', 'roh': 'rético-romance', 'rom': 'romaní', 'rum': 'rumano', 'run': 'rundi', 'rup': 'aromaniano', 'rus': 'ruso', 'sad': 'sandawe', 'sag': 'sango (ubangiense criollo)', 'sah': 'yakuto', 'sai': 'indio sudamericano (otros)', 'sal': 'lenguas salish', 'sam': 'arameo samaritano', 'san': 'sánscrito', 'sao': 'samoano', 'sas': 'sasak', 'sat': 'santalí', 'scc': 'serbio', 'scn': 'siciliano italiano', 'sco': 'escocés', 'scr': 'croata', 'sel': 'selkup', 'sem': 'semítico (otros)', 'sga': 'irlandés antiguo (hasta 1100)', 'sgn': 'lenguas de signos', 'shn': 'shan', 'sho': 'shona', 'sid': 'sidamo', 'sin': 'cingalés', 'sio': 'siouan (otros)', 'sit': 'sino-tibetano (otros)', 'sla': 'eslavo (otros)', 'slo': 'eslovaco', 'slv': 'esloveno', 'sma': 'sami meridional', 'sme': 'sami septentrional', 'smi': 'sami', 'smj': 'sami lule', 'smn': 'sami inari', 'smo': 'samoano', 'sms': 'sami skolt', 'sna': 'shona', 'snd': 'sindhi', 'snh': 'cingalés', 'snk': 'soninké', 'sog': 'sogdiano', 'som': 'somalí', 'son': 'songhay', 'sot': 'sotho', 'spa': 'español', 'srd': 'sardo', 'srn': 'sranan', 'srp': 'serbio', 'srr': 'serer', 'ssa': 'nilosahariano (otros)', 'sso': 'sotho', 'ssw': 'suazi', 'suk': 'sukuma', 'sun': 'sundanés', 'sus': 'susu', 'sux': 'sumerio', 'swa': 'suajili', 'swe': 'sueco', 'swz': 'suazi', 'syc': 'siríaco', 'syr': 'siríaco moderno', 'tag': 'tagalo', 'tah': 'tahitiano', 'tai': 'tai (otros)', 'taj': 'tayiko', 'tam': 'tamil', 'tar': 'tártaro', 'tat': 'tártaro', 'tel': 'telugu', 'tem': 'temne', 'ter': 'terena', 'tet': 'tetum', 'tgk': 'tayiko', 'tgl': 'tagalo', 'tha': 'tailandés', 'tib': 'tibetano', 'tig': 'tigre', 'tir': 'tigriña', 'tiv': 'tiv', 'tkl': 'tokelauano', 'tlh': 'klingon (lengua artificial)', 'tli': 'tlingit', 'tmh': 'támazight', 'tog': 'tonga (Nyasa)', 'ton': 'tongano', 'tpi': 'tok pisin', 'tru': 'chuukés', 'tsi': 'tsimshiano', 'tsn': 'tswana', 'tso': 'tsonga', 'tsw': 'tswana', 'tuk': 'turcomano', 'tum': 'tumbuka', 'tup': 'lenguas tupi', 'tur': 'turco', 'tut': 'altaico (otros)', 'tvl': 'tuvaluano', 'twi': 'twi', 'tyv': 'tuviniano', 'udm': 'udmurto', 'uga': 'ugarítico', 'uig': 'uigur', 'ukr': 'ucraniano', 'umb': 'umbundu', 'und': 'indeterminado', 'urd': 'urdu', 'uzb': 'uzbeko', 'vai': 'vai', 'ven': 'venda', 'vie': 'vietnamita', 'vol': 'volapük', 'vot': 'votic', 'wak': 'lenguas wakash', 'wal': 'wolaytta', 'war': 'waray', 'was': 'washo', 'wel': 'galés', 'wen': 'sorbio (otro)', 'wln': 'walloon', 'wol': 'wolof', 'xal': 'oirat', 'xho': 'xhosa', 'yao': 'yao (África)', 'yap': 'yapés', 'yid': 'yiddish', 'yor': 'yoruba', 'ypk': 'lenguas yupik', 'zap': 'zapotec', 'zbl': 'símbolos Bliss', 'zen': 'zenaga', 'zha': 'zhuang', 'znd': 'lenguas zándicas', 'zul': 'zulú', 'zun': 'zuñi', 'zxx': 'Sin contenido:Optional[str] =Noneal', 'zza': 'Zazaki'}

class Per(msgspec.Struct, omit_defaults=True):
    id: Optional[str] = None
    t_001: Optional[str] = None
    t_024: Optional[str] = None
    t_046: Optional[str] = None
    t_100: Optional[str] = None
    t_368: Optional[str] = None
    t_370: Optional[str] = None
    t_372: Optional[str] = None
    t_373: Optional[str] = None
    t_374: Optional[str] = None
    t_375: Optional[str] = None
    t_377: Optional[str] = None
    t_400: Optional[str] = None
    t_500: Optional[str] = None
    t_510: Optional[str] = None
    t_670: Optional[str] = None
    otros_identificadores: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    fecha_muerte: Optional[str] = None
    nombre_de_persona: Optional[str] = None
    otros_atributos_persona: Optional[str] = None
    lugar_nacimiento: Optional[str] = None
    lugar_muerte: Optional[str] = None
    pais_relacionado: Optional[str] = None
    otros_lugares_relacionados: Optional[str] = None
    lugar_residencia: Optional[str] = None
    campo_actividad: Optional[str] = None
    grupo_o_entidad_relacionada: Optional[str] = None
    ocupacion: Optional[str] = None
    genero: Optional[str] = None
    lengua: Optional[str] = None
    otros_nombres: Optional[str] = None
    persona_relacionada: Optional[str] = None
    fuentes_de_informacion: Optional[str] = None
    obras_relacionadas_en_el_catalogo_BNE: Optional[str] = None

class Geo(msgspec.Struct, omit_defaults=True):
    id:Optional[str] = None
    t_001:Optional[str] = None
    t_024:Optional[str] = None
    t_034:Optional[str] = None
    t_080:Optional[str] = None
    t_151:Optional[str] = None
    t_451:Optional[str] = None
    t_510:Optional[str] = None
    t_550:Optional[str] = None
    t_551:Optional[str] = None
    t_667:Optional[str] = None
    t_670:Optional[str] = None
    t_781:Optional[str] = None
    otros_identificadores:Optional[str] = None
    coordenadas_lat_lng:Optional[str] = None
    CDU:Optional[str] = None
    nombre_de_lugar:Optional[str] = None
    otros_nombres_de_lugar:Optional[str] = None
    entidad_relacionada:Optional[str] = None
    materia_relacionada:Optional[str] = None
    lugar_relacionado:Optional[str] = None
    nota_general:Optional[str] = None
    fuentes_de_informacion:Optional[str] = None
    lugar_jerarquico:Optional[str] = None
    obras_relacionadas_en_el_catalogo_BNE:Optional[str] = None

class Mon(msgspec.Struct, omit_defaults=True):
    id:Optional[str] = None
    t_001:Optional[str] =None
    t_008:Optional[str] =None
    t_017:Optional[str] =None
    t_020:Optional[str] =None
    t_024:Optional[str] =None
    t_035:Optional[str] =None
    t_040:Optional[str] =None
    t_041:Optional[str] =None
    t_080:Optional[str] =None
    t_100:Optional[str] =None
    t_110:Optional[str] =None
    t_130:Optional[str] =None
    t_245:Optional[str] =None
    t_246:Optional[str] =None
    t_260:Optional[str] =None
    t_264:Optional[str] =None
    t_300:Optional[str] =None
    t_440:Optional[str] =None
    t_490:Optional[str] =None
    t_500:Optional[str] =None
    t_504:Optional[str] =None
    t_505:Optional[str] =None
    t_546:Optional[str] =None
    t_561:Optional[str] =None
    t_586:Optional[str] =None
    t_594:Optional[str] =None
    t_600:Optional[str] =None
    t_610:Optional[str] =None
    t_611:Optional[str] =None
    t_630:Optional[str] =None
    t_650:Optional[str] =None
    t_651:Optional[str] =None
    t_653:Optional[str] =None
    t_655:Optional[str] =None
    t_700:Optional[str] =None
    t_710:Optional[str] =None
    t_740:Optional[str] =None
    t_752:Optional[str] =None
    t_770:Optional[str] =None
    t_772:Optional[str] =None
    t_773:Optional[str] =None
    t_774:Optional[str] =None
    t_775:Optional[str] =None
    t_776:Optional[str] =None
    t_777:Optional[str] =None
    t_787:Optional[str] =None
    t_800:Optional[str] =None
    t_810:Optional[str] =None
    t_811:Optional[str] =None
    t_830:Optional[str] =None
    t_980:Optional[str] =None
    t_994:Optional[str] =None
    per_id:Optional[str] =None
    pais_de_publicacion:Optional[str] =None
    lengua_principal:Optional[str] =None
    otras_lenguas:Optional[str] =None
    lengua_original:Optional[str] =None
    fecha_de_publicacion:Optional[str] =None
    decada:Optional[str] =None
    siglo:Optional[str] =None
    deposito_legal:Optional[str] =None
    isbn:Optional[str] =None
    nipo:Optional[str] =None
    cdu:Optional[str] =None
    autores:Optional[str] =None
    titulo:Optional[str] =None
    mencion_de_autores:Optional[str] =None
    otros_titulos:Optional[str] =None
    edicion:Optional[str] =None
    lugar_de_publicacion:Optional[str] =None
    editorial:Optional[str] =None
    extension:Optional[str] =None
    otras_caracteristicas_fisicas:Optional[str] =None
    dimensiones:Optional[str] =None
    material_anejo:Optional[str] =None
    serie:Optional[str] =None
    nota_de_contenido:Optional[str] =None
    notas:Optional[str] =None
    procedencia:Optional[str] =None
    premios:Optional[str] =None
    tema:Optional[str] =None
    genero_forma:Optional[str] =None
    tipo_de_documento:Optional[str] =None

class Ent(msgspec.Struct, omit_defaults=True):
    id: Optional[str] = None
    t_001: Optional[str] = None
    t_024: Optional[str] = None
    t_046: Optional[str] = None
    t_110: Optional[str] = None
    t_368: Optional[str] = None
    t_370: Optional[str] = None
    t_372: Optional[str] = None
    t_377: Optional[str] = None
    t_410: Optional[str] = None
    t_500: Optional[str] = None
    t_510: Optional[str] = None
    t_663: Optional[str] = None
    t_665: Optional[str] = None
    t_667: Optional[str] = None
    t_670: Optional[str] = None
    t_678: Optional[str] = None
    otros_identificadores: Optional[str] = None
    fecha_establecimiento: Optional[str] = None
    fecha_finalizacion: Optional[str] = None
    nombre_de_entidad: Optional[str] = None
    tipo_entidad: Optional[str] = None
    pais: Optional[str] = None
    sede: Optional[str] = None
    campo_actividad: Optional[str] = None
    lengua: Optional[str] = None
    otros_nombres: Optional[str] = None
    persona_relacionada: Optional[str] = None
    grupo_o_entidad_relacionada: Optional[str] = None
    nota_de_relacion: Optional[str] = None
    otros_datos_historicos: Optional[str] = None
    nota_general: Optional[str] = None
    fuentes_de_informacion: Optional[str] = None

class Queries(msgspec.Struct, omit_defaults=True):
    id:Optional[str]=None
    query:Optional[str]=None
    length:Optional[str]=None
    date:Optional[str]=None
    ip:Optional[str]=None
    dataset:Optional[str]=None
    time:Optional[str]=None
structs = {
    "geo": Geo,"per":Per, "mon":Mon, "ent":Ent, "queries":Queries
}

class QMO:
    def __init__(self,dataset:str,  args:dict=None, json_file:str=None):
        self.dataset = dataset
        self.args = args
        self.json_file = json_file
    
    @property
    def con(self):
        return get_db()
    
    @property
    def cur(self):
        return self.con.cursor()
    
    @property
    def available_fields(self) -> list:
        return [row[1] for row in self.cur.execute(f"pragma table_info({self.dataset});")]
    
    @property
    def virtual_fields(self) -> list:
        return [row[1] for row in self.cur.execute(f"pragma table_info({self.dataset}_fts);")]
    
    @property
    def marc_fields(self) -> str:
        result = ""
        for field in self.cur.execute(f"pragma table_info({self.dataset});"):
            field:str = field[1]
            if field.startswith("t_"):
                result += f", {self.dataset}_fts.{field}"
            else:
                result += f", NULL"
        return result[2:]

    @property
    def human_fields(self) -> str:
        result = ""
        for field in self.cur.execute(f"pragma table_info({self.dataset});"):
            field:str = field[1]
            if not field.startswith("t_"):
                result += f", {self.dataset}_fts.{field}"
            else:
                result += f", NULL"
        return result[2:]
        
    @property
    def splitter(self):
        return " /**/ "
    
    @property
    def res_json(self):
        res = {"success":False}
        return res

    @property
    def purgue(self) -> dict:
        f'''
        This function will clean the data coming from the query params and also will raise errors when one or
        more fields where bad designated or mal used

        purgue() will return a dict/json object that can contain the followings:
        success: boolean
        limit: int
        view: human|marc
        fields: []string
        dataset_2: dict:string
        args: dict:string
        message: string

        when success == False a message will be supplied with the error that has occurred
        '''
        res_json = self.res_json
        args = self.args.copy()
        fields = args.pop("fields", None)
        limit = args.pop("limit", "1000")
        view = args.pop("view", False)
        for k in args.keys():
            if k in structs.keys():
                dataset_2 = {k:args.pop(k)}
                break
            else:
                dataset_2 = None
        if limit:
            try:
                 int(limit)
            except ValueError as e:
                res_json["message"] = f"Limit value should be an integer"
                return res_json
        res_json["limit"] = limit  
        for field in fields.split(",") if fields else ():
            field:str = field.strip()
            if field not in self.available_fields:
                res_json["message"] = f"This field doesn't exist in the db: {field} - available fields: {self.available_fields}"
                return res_json
            field:str = f"{self.dataset}.{field.strip()}"
        if fields:
            result = ""
            for field in self.available_fields:
                if field in fields.split(","):
                    result += f",{self.dataset}_fts.{field}"
                else:
                    result += f",NULL"
            res_json["fields"] = result[1:]
        else:
            res_json["fields"] = fields
        
        not_available_field = next(filter(lambda kv: kv[0] not in self.available_fields, args.items()), None)
        if not_available_field:
            res_json["message"] = f"This field doesn't exist in the db: {not_available_field[0]}  - available fields: {self.available_fields}"
            return res_json
        if view:
            if view == "marc":
                res_json["fields"] = self.marc_fields
            elif view == "human":
                res_json["fields"] = self.human_fields
        res_json["args"] = args
        res_json["success"] = True
        try:
            res_json["dataset_2"] = dataset_2
        except UnboundLocalError:
            pass
        return res_json
    
    def where(self, args: dict, dataset:str = None) -> str:
        '''
        where() will return a valid sqlite3 query syntax formed by the args supplied
        dataset: [str]|None
        if dataset supplied, will build the query based on a different dataset from the one available on self properties
        '''
        dataset = dataset if dataset else self.dataset  
        # print(dataset, "XX", self.dataset)
        args = dict(args)
        if not args:
            return ""
        result = "WHERE ("
        and_or = " AND "
        for k,value in args.items():
            '''
            VIRTUAL START
            '''
            # if True:
            # if k in self.virtual_fields and value.find("null") == -1 and dataset == self.dataset:
                # v = re.sub("\|\||¬|!", "", value)
                # v = value.replace("||", "* OR ")
                # # v_where = f''' {self.dataset} match '{k}:NEAR("{v}*")'  {and_or}'''
                # v_where = f''' {self.dataset}_fts.{k} match '{v}*'  {and_or}'''
                # result += v_where
        # else:
            k = f"{dataset}.{k}"
            value: str = value.lower()
            if value[-2:] == "||":
                and_or = " OR  "
                value = value[0:-2]
            else:
                and_or = " AND "
            if value[0] == "!":
                value = value.replace("!", "NOT LIKE ", 1)
            else:
                value = f"LIKE {value}"
            
            value = value.replace("||", f" OR {k} LIKE ")
            value = value.replace("¬", f" AND {k} LIKE ")
            value = value.replace("LIKE !", "NOT LIKE ")
            if value.find("NOT") >= 0:
                value_splitted = value[6:].split(" ", 1)
            elif value.find("OR") >= 0:
                value_splitted = value.split(" ")
            else:
                value_splitted = value.split(" ", 1)
            for v in value_splitted:
                if v.islower() and v not in self.available_fields or not v.isalnum() and v:
                    if v == "null":
                        value = value.replace(v, "NULL")
                        if value.find("NOT LIKE NULL") >= 0:
                            value = value.replace("NOT LIKE NULL", "IS NOT NULL")
                        elif value.find("LIKE NULL") >= 0:
                            value = value.replace("LIKE NULL", "IS NULL")
                    else:
                        if k.find("t_") >= 0:
                            if not v.startswith(f"{self.dataset}."):
                                value = value.replace(v, f"'|%{v}%'")
                        elif k.find("siglo") >= 0:
                            value = value.replace(v, f"'{v}'")
                        else:
                            value = value.replace(v, f"' %{v}%'")

            result += f"{k} {value}{and_or}"        
        result = re.sub("\%\'\s{1,}\'\%|\%\'\s{1,}\'\|%", " ", result)
        return result[0:-5] + ")"
    
    def where_fts(self, args: dict, dataset:str = None) -> str:
        args = dict(args)
        dataset = dataset if dataset else self.dataset
        if not args:
            return ""
        result = f"WHERE "
        and_or = " AND "
        for k,value in args.items():
            v = value.strip()
            if v.find("null") >= 0:
                v_where = f'''{dataset}_fts.{k} IS NULL{and_or}'''
                if v.find("!") >= 0:
                    v_where = v_where.replace("IS NULL", "IS NOT NULL")
            elif v.find("!") >= 0:
                v_where = f'''{dataset}_fts.{k} NOT LIKE '%{v}%'{and_or}'''
                v_where = v_where.replace("!", "")
            elif k == "all":
                v_where = f'''{dataset}_fts MATCH '{v}*'{and_or}'''
            elif k == "siglo" or k == "decada":
                v_where = f'''{dataset}_fts.{k} MATCH '{v}'{and_or}'''
            else:
                if v.find("||") >= 0:
                    v = v.replace("||", "* OR ")
                v_where = f'''{dataset}_fts.{k} MATCH '{v}*'{and_or}'''

            result += v_where
        # result = re.sub("\%\'\s{1,}\'\%|\%\'\s{1,}\'\|%", " ", result)
        return result[:-5]

    def joining(self, dataset_2:dict) -> str:
        dataset = list(dataset_2.keys())[0].strip()
        result = {dataset:{}}
        filters = dataset_2[dataset].split(",") 
        print(filters)
        for v in filters:
            k,v = v.split(":")
            result[dataset][k] = v.strip()
        return result
    
    def query(self) -> dict:
        
        res_json = self.purgue
        if not res_json["success"]:
            return {"success":False,"message":res_json["message"]}
        
        all_fields=""
        for field in self.available_fields:
            all_fields += f"{self.dataset}_fts.{field}, "
        fields = res_json['fields'] if res_json['fields'] else all_fields[0:-2]
        if not fields:
            fields = " * "
        else:
            for field in fields.split(" "):
                if field.find("NULL") >= 0:
                    pass
        query = f"SELECT {fields} FROM {self.dataset}_fts "
        if res_json.get("dataset_2"):
            d_2 = list(res_json["dataset_2"].keys())[0]
            query += f" WHERE {'per_id' if d_2 == 'per' else 'id'} IN (SELECT {'id' if d_2 == 'per' else 'per_id'} from {d_2}_fts "
            print("ON JOINING")
            joining_dict = self.joining(res_json["dataset_2"])
            d_2_where = self.where_fts(joining_dict[d_2], d_2)
            query += d_2_where +")"
            d_1_where = self.where_fts(res_json["args"].items())
            if d_1_where:
                d_1_where = d_1_where.replace("WHERE", "")
                query += f" AND ({d_1_where})"
            # where_dataset = where_dataset.replace("WHERE", " AND ")
            # joining_where = joining_where.replace("WHERE", f"WHERE per_id in (select id from per_fts WHERE ")
            # if where_dataset:
            #     joining_where += d_1_where
            # query += joining_where

        else:
            query += self.where_fts(res_json["args"].items())
        query += f" LIMIT {res_json['limit']};" 
        print(f"\n{query}\n".center(50 + len(query),"#"))
        with open("logs/query.log", mode="r+", encoding="utf-8") as file:
            if len(file.readlines()) <= 10:
                file.write("")
            lines = file.readlines()
            lines.extend(f"\n{dt.datetime.now()} | {query}\n")
            file.writelines(lines)
        '''
        saving query:
        '''
        self.enter(query, error=True)
        try:
            res = self.cur.execute(query)
        except sqlite3.OperationalError as e:
            res = {}
            res["success"] = False
            res["message"] = "SQLite3 Operational Error"
            res["Error"] = f"{e}"
            return res
        res_json = self.res_json
        res_json["success"] = True
        res_json["data"] = map(lambda row:structs[self.dataset](*row),res)
        res_json["query"] = query
        return res_json
    
    def searches(self) -> dict:
        qu = self.cur.execute("SELECT * FROM queries ORDER BY date DESC;")
        res = {}
        result = {"data":[]}
        # res["data"] = map(lambda row:structs[self.dataset](*row),qu)
        res["data"] = map(lambda row:dict(zip(self.available_fields, row)),qu)
        for r in res["data"]:
            r["plan"] = list(self.cur.execute(f"EXPLAIN QUERY PLAN {r.get('query')}"))[0][3]
            result["data"].append(r)
        return result
        
    def enter(self, query:str, length:int=None, date:str=None, dataset:str=None, time:float=None,is_from_web:bool=False ,error:bool=None, update:bool=False):
        if update:
            last_id = tuple(self.cur.execute("SELECT id FROM queries ORDER BY date LIMIT 1;"))[0][0]
            print(f"LAST ID: {last_id}")
            query_str = f'''
                        UPDATE queries SET length = ?, date=?, dataset=?, time=?, is_from_web=?, error=0 WHERE id = '{last_id}';
                        '''
            self.cur.execute(query_str, (length, date, dataset, time, False))
            self.con.commit()
        else:
            query_str = f'''
                    INSERT INTO queries VALUES(
                    '{uuid4().hex}',
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                    )
                    '''
            self.cur.execute(query_str, (query, length, date, dataset, time,is_from_web ,error))
            self.con.commit()
    
    def blunt_query(self):
        query: str = self.args.get("query")
        res_json = self.res_json
        blacklisted = ("update", "delete", "create", "insert", "pragma", "table_info", "drop", "alter" , "commit", "into")
        if query:
            q = query.lower()
            for bl in blacklisted:
                if q.find(bl) >= 0:
                    res_json["message"] = "Not a valid query"
                    return res_json
        print(query)
        try:
            # res = list(self.cur.execute(query))
            res = self.cur.execute(query)
        except Exception as e:
            res_json["message"] = "Bad formulated query"
            res_json["error"] = f"{e}"
            return res_json
        res_json["success"] = True
        res_json["data"] = res
        return res_json

    def insert(self):
        res_json = {"success":False}
        with open(f"converter/{self.dataset}.json", encoding="utf-8") as file:
            # try:
                s = time.perf_counter()
                data = json.loads(file.read())
                data = data
                query = f"insert or ignore into {self.dataset} values ({'?, '*len(self.available_fields)})"
                query = query.replace(", )", ")")
                print(query.center(50 + len(query), "#"))
                self.cur.executemany(query,map(lambda record: self.extract_values(self.dataset, record), data))
                self.con.commit()
                res_json["success"] = True
                res_json["time"] = time.perf_counter() - s
                return res_json