from constants import DB_FILE
from flask import g
import sqlite3
import re
import time
import orjson as json
from uuid import uuid4
from views.api.models import create_statements as models

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

class MMO:
    '''
    The intended use of this Object is for mapping and entering records.
    '''
    def __init__(self, dataset:str):
        self.dataset = dataset

    @property
    def countries(self):
        return {'': '', 'aa': 'Albania', 'abc': 'Alberta', 'ac': 'Islas Ashmore y Cartier', 'aca': 'Territorio de la Capital Australiana', 'ae': 'Argelia', 'af': 'Afganistán', 'ag': 'Argentina', 'ai': 'Armenia (República)', 'air': 'RSS de Armenia', 'aj': 'Azerbaiyán', 'ajr': 'RSS de Azerbaiyán', 'aku': 'Alaska', 'alu': 'Alabama', 'am': 'Anguila', 'an': 'Andorra', 'ao': 'Angola', 'aq': 'Antigua y Barbuda', 'aru': 'Arkansas', 'as': 'Samoa Americana', 'at': 'Australia', 'au': 'Austria', 'aw': 'Aruba', 'ay': 'Antártida', 'azu': 'Arizona', 'ba': 'Baréin', 'bb': 'Barbados', 'bcc': 'Columbia Británica', 'bd': 'Burundi', 'be': 'Bélgica', 'bf': 'Bahamas', 'bg': 'Bangladés', 'bh': 'Belice', 'bi': 'Territorio Británico del Océano Índico', 'bl': 'Brasil', 'bm': 'Islas Bermudas', 'bn': 'Bosnia y Herzegovina', 'bo': 'Bolivia', 'bp': 'Islas Salomón', 'br': 'Birmania', 'bs': 'Botsuana', 'bt': 'Bután', 'bu': 'Bulgaria', 'bv': 'Isla Bouvet', 'bw': 'Bielorrusia', 'bwr': 'RSS de Bielorrusia', 'bx': 'Brunéi', 'ca': 'Países Bajos Caribeños', 'cau': 'California', 'cb': 'Camboya', 'cc': 'China', 'cd': 'Chad', 'ce': 'Sri Lanka', 'cf': 'Congo (Brazzaville)', 'cg': 'Congo (República Democrática)', 'ch': 'China (República: 1949- )', 'ci': 'Croacia', 'cj': 'Islas Caimán', 'ck': 'Colombia', 'cl': 'Chile', 'cm': 'Camerún', 'cn': 'Canadá', 'co': 'Curazao', 'cou': 'Colorado', 'cp': 'Islas de Cantón y Enderbury', 'cq': 'Comoras', 'cr': 'Costa Rica', 'cs': 'Checoslovaquia', 'ctu': 'Connecticut', 'cu': 'Cuba', 'cv': 'Cabo Verde', 'cw': 'Islas Cook', 'cx': 'República Centroafricana', 'cy': 'Chipre', 'cz': 'Zona del Canal', 'dcu': 'Distrito de Columbia', 'deu': 'Delaware', 'dk': 'Dinamarca', 'dm': 'Benín', 'dq': 'Dominica', 'dr': 'República Dominicana', 'ea': 'Eritrea', 'ec': 'Ecuador', 'eg': 'Guinea Ecuatorial', 'em': 'Timor Oriental', 'enk': 'Inglaterra', 'er': 'Estonia', 'err': 'Estonia', 'es': 'El Salvador', 'et': 'Etiopía', 'fa': 'Islas Feroe', 'fg': 'Guayana Francesa', 'fi': 'Finlandia', 'fj': 'Fiyi', 'fk': 'Islas Malvinas', 'flu': 'Florida', 'fm': 'Estados Federados de Micronesia', 'fp': 'Polinesia Francesa', 'fr': 'Francia', 'fs': 'Tierras Australes y Antárticas Francesas', 'ft': 'Yibuti', 'gau': 'Georgia', 'gb': 'Kiribati', 'gd': 'Granada', 'ge': 'Alemania Oriental', 'gg': 'Guernsey', 'gh': 'Ghana', 'gi': 'Gibraltar', 'gl': 'Groenlandia', 'gm': 'Gambia', 'gn': 'Islas Gilbert y Ellice', 'go': 'Gabón', 'gp': 'Guadalupe', 'gr': 'Grecia', 'gs': 'Georgia (República)', 'gsr': 'RSS de Georgia', 'gt': 'Guatemala', 'gu': 'Guam', 'gv': 'Guinea', 'gw': 'Alemania', 'gy': 'Guyana', 'gz': 'Franja de Gaza', 'hiu': 'Hawái', 'hk': 'Hong Kong', 'hm': 'Islas Heard y McDonald', 'ho': 'Honduras', 'ht': 'Haití', 'hu': 'Hungría', 'iau': 'Iowa', 'ic': 'Islandia', 'idu': 'Idaho', 'ie': 'Irlanda', 'ii': 'India', 'ilu': 'Illinois', 'im': 'Isla de Man', 'inu': 'Indiana', 'io': 'Indonesia', 'iq': 'Irak', 'ir': 'Irán', 'is': 'Israel', 'it': 'Italia', 'iu': 'Zonas Desmilitarizadas de Israel y Siria', 'iv': 'Costa de Marfil', 'iw': 'Zonas Desmilitarizadas de Israel y Jordania', 'iy': 'Zona Neutral de Irak y Arabia Saudita', 'ja': 'Japón', 'je': 'Jersey', 'ji': 'Atolón Johnston', 'jm': 'Jamaica', 'jn': 'Jan Mayen', 'jo': 'Jordania', 'ke': 'Kenia', 'kg': 'Kirguistán', 'kgr': 'RSS de Kirguistán', 'kn': 'Corea del Norte', 'ko': 'Corea del Sur', 'ksu': 'Kansas', 'ku': 'Kuwait', 'kv': 'Kosovo', 'kyu': 'Kentucky', 'kz': 'Kazajistán', 'kzr': 'RSS de Kazajistán', 'lau': 'Luisiana', 'lb': 'Liberia', 'le': 'Líbano', 'lh': 'Liechtenstein', 'li': 'Lituania', 'lir': 'Lituania', 'ln': 'Islas del Sur y Central', 'lo': 'Lesoto', 'ls': 'Laos', 'lu': 'Luxemburgo', 'lv': 'Letonia', 'lvr': 'Letonia', 'ly': 'Libia', 'mau': 'Massachusetts', 'mbc': 'Manitoba', 'mc': 'Mónaco', 'mdu': 'Maryland', 'meu': 'Maine', 'mf': 'Mauricio', 'mg': 'Madagascar', 'mh': 'Macao', 'miu': 'Míchigan', 'mj': 'Montserrat', 'mk': 'Omán', 'ml': 'Malí', 'mm': 'Malta', 'mnu': 'Minnesota', 'mo': 'Montenegro', 'mou': 'Misuri', 'mp': 'Mongolia', 'mq': 'Martinica', 'mr': 'Marruecos', 'msu': 'Misisipi', 'mtu': 'Montana', 'mu': 'Mauritania', 'mv': 'Moldavia', 'mvr': 'RSS de Moldavia', 'mw': 'Malaui', 'mx': 'México', 'my': 'Malasia', 'mz': 'Mozambique', 'na': 'Antillas Neerlandesas', 'nbu': 'Nebraska', 'ncu': 'Carolina del Norte', 'ndu': 'Dakota del Norte', 'ne': 'Países Bajos', 'nfc': 'Terranova y Labrador', 'ng': 'Níger', 'nhu': 'Nuevo Hampshire', 'nik': 'Irlanda del Norte', 'nju': 'Nueva Jersey', 'nkc': 'Nuevo Brunswick', 'nl': 'Nueva Caledonia', 'nm': 'Islas Marianas del Norte', 'nmu': 'Nuevo México', 'nn': 'Vanuatu', 'no': 'Noruega', 'np': 'Nepal', 'nq': 'Nicaragua', 'nr': 'Nigeria', 'nsc': 'Nueva Escocia', 'ntc': 'Territorios del Noroeste', 'nu': 'Nauru', 'nuc': 'Nunavut', 'nvu': 'Nevada', 'nw': 'Islas Marianas del Norte', 'nx': 'Isla Norfolk', 'nyu': 'Estado de Nueva York', 'nz': 'Nueva Zelanda', 'ohu': 'Ohio', 'oku': 'Oklahoma', 'onc': 'Ontario', 'oru': 'Oregón', 'ot': 'Mayotte', 'pau': 'Pensilvania', 'pc': 'Isla Pitcairn', 'pe': 'Perú', 'pf': 'Islas Paracel', 'pg': 'Guinea-Bisáu', 'ph': 'Filipinas', 'pic': 'Isla del Príncipe Eduardo', 'pk': 'Pakistán', 'pl': 'Polonia', 'pn': 'Panamá', 'po': 'Portugal', 'pp': 'Papúa Nueva Guinea', 'pr': 'Puerto Rico', 'pt': 'Timor Portugués', 'pw': 'Palaos', 'py': 'Paraguay', 'qa': 'Catar', 'qea': 'Queensland', 'quc': 'Quebec (Provincia)', 'rb': 'Serbia', 're': 'Reunión', 'rh': 'Zimbabue', 'riu': 'Rhode Island', 'rm': 'Rumania', 'ru': 'Federación Rusa', 'rur': 'RSS de la URSS', 'rw': 'Ruanda', 'ry': 'Islas Ryukyu, Sur', 'sa': 'Sudáfrica', 'sb': 'Svalbard', 'sc': 'San Bartolomé', 'scu': 'Carolina del Sur', 'sd': 'Sudán del Sur', 'sdu': 'Dakota del Sur', 'se': 'Seychelles', 'sf': 'Santo Tomé y Príncipe', 'sg': 'Senegal', 'sh': 'África del Norte Española', 'si': 'Singapur', 'sj': 'Sudán', 'sk': 'Sikkim', 'sl': 'Sierra Leona', 'sm': 'San Marino', 'sn': 'Sint Maarten', 'snc': 'Saskatchewan', 'so': 'Somalia', 'sp': 'España', 'sq': 'Esuatini', 'sr': 'Surinam', 'ss': 'Sáhara Occidental', 'st': 'San Martín', 'stk': 'Escocia', 'su': 'Arabia Saudita', 'sv': 'Islas Swan', 'sw': 'Suecia', 'sx': 'Namibia', 'sy': 'Siria', 'sz': 'Suiza', 'ta': 'Tayikistán', 'tar': 'RSS de Tayikistán', 'tc': 'Islas Turcas y Caicos', 'tg': 'Togo', 'th': 'Tailandia', 'ti': 'Túnez', 'tk': 'Turkmenistán', 'tkr': 'RSS de Turkmenistán', 'tl': 'Tokelau', 'tma': 'Tasmania', 'tnu': 'Tennessee', 'to': 'Tonga', 'tr': 'Trinidad y Tobago', 'ts': 'Emiratos Árabes Unidos', 'tt': 'Territorio en Fideicomiso de las Islas del Pacífico', 'tu': 'Turquía', 'tv': 'Tuvalu', 'txu': 'Texas', 'tz': 'Tanzania', 'ua': 'Egipto', 'uc': 'Islas del Caribe de Estados Unidos', 'ug': 'Uganda', 'ui': 'Islas Varias del Reino Unido', 'uik': 'Islas Varias del Reino Unido', 'uk': 'Reino Unido', 'un': 'Ucrania', 'unr': 'Ucrania', 'up': 'Islas Varias del Pacífico de Estados Unidos', 'ur': 'Unión Soviética', 'us': 'Estados Unidos', 'utu': 'Utah', 'uv': 'Burkina Faso', 'uy': 'Uruguay', 'uz': 'Uzbekistán', 'uzr': 'RSS de Uzbekistán', 'vau': 'Virginia.', 'vb': 'Islas Vírgenes Británicas', 'vc': 'Ciudad del Vaticano', 've': 'Venezuela', 'vi': 'Islas Vírgenes de los Estados Unidos', 'vm': 'Vietnam', 'vn': 'Vietnam del Norte', 'vp': 'Varios lugares', 'vra': 'Victoria', 'vs': 'Vietnam del Sur', 'vtu': 'Vermont', 'wau': 'Estado de Washington', 'wb': 'Berlín Oeste', 'wea': 'Australia Occidental', 'wf': 'Wallis y Futuna', 'wiu': 'Wisconsin', 'wj': 'Margen Occidental del Río Jordán', 'wk': 'Isla Wake', 'wlk': 'Gales', 'ws': 'Samoa', 'wvu': 'Virginia Occidental', 'wyu': 'Wyoming', 'xa': 'Isla de Navidad (Océano Índico)', 'xb': 'Islas Cocos (Keeling)', 'xc': 'Maldivas', 'xd': 'San Cristóbal y Nieves', 'xe': 'Islas Marshall', 'xf': 'Islas Midway', 'xga': 'Territorio de las Islas del Mar del Coral', 'xh': 'Niue', 'xi': 'San Cristóbal y Nieves-Anguila', 'xj': 'Santa Elena', 'xk': 'Santa Lucía', 'xl': 'San Pedro y Miquelón', 'xm': 'San Vicente y las Granadinas', 'xn': 'Macedonia del Norte', 'xna': 'Nueva Gales del Sur', 'xo': 'Eslovaquia', 'xoa': 'Territorio del Norte', 'xp': 'Isla Spratly', 'xr': 'República Checa', 'xra': 'Australia Meridional', 'xs': 'Islas Georgias del Sur y Sandwich del Sur', 'xv': 'Eslovenia', 'xx': 'Sin lugar, desconocido o indeterminado', 'xxc': 'Canadá', 'xxk': 'Islas varias del Reino Unido', 'xxr': 'Unión Soviética', 'xxu': 'Estados Unidos', 'ye': 'Yemen', 'ykc': 'Territorio de Yukón', 'ys': 'Yemen (República Democrática Popular)', 'yu': 'Serbia y Montenegro', 'za': 'Zambia'}        
    
    @property
    def languages(self):
        return {'': '', 'aar': 'Afar', 'abk': 'abjasio', 'ace': 'achinés', 'ach': 'acoli', 'ada': 'adangme', 'ady': 'adigué', 'afa': 'afroasiático (otros)', 'afh': 'afrihili (lengua artificial)', 'afr': 'afrikáans', 'ain': 'ainu', 'ajm': 'aljamía', 'aka': 'akan', 'akk': 'acadio', 'alb': 'albanés', 'ale': 'aleutiano', 'alg': 'algonquino (otros)', 'alt': 'altai', 'amh': 'amárico', 'ang': 'inglés antiguo (ca. 450-1100)', 'anp': 'angika', 'apa': 'lenguas apache', 'ara': 'árabe', 'arc': 'arameo', 'arg': 'aragonés', 'arm': 'armenio', 'arn': 'mapuche', 'arp': 'arapaho', 'art': 'artificial (otros)', 'arw': 'arahuaco', 'asm': 'asamés', 'ast': 'bable', 'ath': 'atapascos (otros)', 'aus': 'lenguas australianas', 'ava': 'ávaro', 'ave': 'avéstico', 'awa': 'awadhi', 'aym': 'aimara', 'aze': 'azerí', 'bad': 'lenguas banda', 'bai': 'lenguas bamileke', 'bak': 'bashkir', 'bal': 'baluchi', 'bam': 'bambara', 'ban': 'balinés', 'baq': 'vasco', 'bas': 'basa', 'bat': 'báltico (otros)', 'bej': 'beja', 'bel': 'bielorruso', 'bem': 'bemba', 'ben': 'bengalí', 'ber': 'bereber (otros)', 'bho': 'bhojpuri', 'bih': 'bihari (otros)', 'bik': 'bikol', 'bin': 'edo', 'bis': 'bislama', 'bla': 'siksika', 'bnt': 'bantú (otros)', 'bos': 'bosnio', 'bra': 'braj', 'bre': 'bretón', 'btk': 'batak', 'bua': 'buriat', 'bug': 'bugis', 'bul': 'búlgaro', 'bur': 'birmano', 'byn': 'bilin', 'cad': 'caddo', 'cai': 'indio centroamericano (otros)', 'cam': 'jemer', 'car': 'caribe', 'cat': 'catalán', 'cau': 'caucásico (otros)', 'ceb': 'cebuano', 'cel': 'céltico (otros)', 'cha': 'chamorro', 'chb': 'chibcha', 'che': 'checheno', 'chg': 'chagatai', 'chi': 'chino', 'chk': 'chuukés', 'chm': 'mari', 'chn': 'jerga chinook', 'cho': 'choctaw', 'chp': 'chipewyan', 'chr': 'cheroqui', 'chu': 'eslavo eclesiástico', 'chv': 'chuvasio', 'chy': 'cheyenne', 'cmc': 'lenguas cham', 'cnr': 'montenegrino', 'cop': 'copto', 'cor': 'córnico', 'cos': 'corso', 'cpe': 'criollos y pidgins basados en el inglés (otros)', 'cpf': 'criollos y pidgins basados en el francés (otros)', 'cpp': 'criollos y pidgins basados en el portugués (otros)', 'cre': 'cree', 'crh': 'tártaro de Crimea', 'crp': 'criollos y pidgins (otros)', 'csb': 'casubio', 'cus': 'cushita (otros)', 'cze': 'checo', 'dak': 'dakota', 'dan': 'danés', 'dar': 'dargwa', 'day': 'dayak', 'del': 'delaware', 'den': 'slavey', 'dgr': 'dogrib', 'din': 'dinka', 'div': 'divehi', 'doi': 'dogri', 'dra': 'dravidiano (otros)', 'dsb': 'sorbio inferior', 'dua': 'duala', 'dum': 'neerlandés medio (ca. 1050-1350)', 'dut': 'neerlandés', 'dyu': 'dyula', 'dzo': 'dzongkha', 'efi': 'efik', 'egy': 'egipcio', 'eka': 'ekajuk', 'elx': 'elamita', 'eng': 'inglés', 'enm': 'inglés medio (1100-1500)', 'epo': 'esperanto', 'esk': 'lenguas esquimales', 'esp': 'esperanto', 'est': 'estonio', 'eth': 'etiópico', 'ewe': 'ewe', 'ewo': 'ewondo', 'fan': 'fang', 'fao': 'feroés', 'far': 'feroés', 'fat': 'fanti', 'fij': 'fiyiano', 'fil': 'filipino', 'fin': 'finlandés', 'fiu': 'fino-ugrio (otros)', 'fon': 'fon', 'fre': 'francés', 'fri': 'frisón', 'frm': 'francés medio (ca. 1300-1600)', 'fro': 'francés antiguo (ca. 842-1300)', 'frr': 'frisón septentrional', 'frs': 'frisón oriental', 'fry': 'frisón', 'ful': 'fula', 'fur': 'friulano', 'gaa': 'gã', 'gae': 'gaélico escocés', 'gag': 'gallego', 'gal': 'oromo', 'gay': 'gayo', 'gba': 'gbaya', 'gem': 'germánico (otros)', 'geo': 'georgiano', 'ger': 'alemán', 'gez': 'etiópico', 'gil': 'gilbertés', 'gla': 'gaélico escocés', 'gle': 'irlandés', 'glg': 'gallego', 'glv': 'manés', 'gmh': 'alemán medio alto (ca. 1050-1500)', 'goh': 'alemán antiguo alto (ca. 750-1050)', 'gon': 'gondi', 'gor': 'gorontalo', 'got': 'gótico', 'grb': 'grebo', 'grc': 'griego antiguo (hasta 1453)', 'gre': 'griego moderno (1453-)', 'grn': 'guaraní', 'gsw': 'alemán suizo', 'gua': 'guaraní', 'guj': 'guyaratí', 'gwi': "gwich'in", 'hai': 'haida', 'hat': 'criollo francés haitiano', 'hau': 'hausa', 'haw': 'hawaiano', 'heb': 'hebreo', 'her': 'herero', 'hil': 'hiligaynon', 'him': 'lenguas pahari occidentales', 'hin': 'hindi', 'hit': 'hitita', 'hmn': 'hmong', 'hmo': 'hiri motu', 'hrv': 'croata', 'hsb': 'alto sorbio', 'hun': 'húngaro', 'hup': 'hupa', 'iba': 'iban', 'ibo': 'igbo', 'ice': 'islandés', 'ido': 'ido', 'iii': 'yi de sichuán', 'ijo': 'ijo', 'iku': 'inuktitut', 'ile': 'interlingue', 'ilo': 'ilocano', 'ina': 'interlingua (Asociación de la Lengua Auxiliar Internacional)', 'inc': 'índico (otros)', 'ind': 'indonesio', 'ine': 'indoeuropeo (otros)', 'inh': 'ingush', 'int': 'interlingua (Asociación Lingüística Internacional Auxiliar)', 'ipk': 'inupiaq', 'ira': 'iraní (otros)', 'iri': 'irlandés', 'iro': 'iroquiano (otros)', 'ita': 'italiano', 'jav': 'javanés', 'jbo': 'lojban (lengua artificial)', 'jpn': 'japonés', 'jpr': 'judeo-persa', 'jrb': 'judeo-árabe', 'kaa': 'karakalpako', 'kab': 'cabila', 'kac': 'kachin', 'kal': 'kalaallisut', 'kam': 'kamba', 'kan': 'kannada', 'kar': 'lenguas karen', 'kas': 'cachemiro', 'kau': 'kanuri', 'kaw': 'kawi', 'kaz': 'kazajo', 'kbd': 'cabardiano', 'kha': 'khasi', 'khi': 'khoisan (otros)', 'khm': 'jemer', 'kho': 'hotanés', 'kik': 'kikuyu', 'kin': 'kinyarwanda', 'kir': 'kirguís', 'kmb': 'kimbundu', 'kok': 'konkani', 'kom': 'komi', 'kon': 'kongo', 'kor': 'coreano', 'kos': 'kosraeano', 'kpe': 'kpelle', 'krc': 'karachay-bálcaro', 'krl': 'carelio', 'kro': 'kru (otros)', 'kru': 'kurukh', 'kua': 'kuanyama', 'kum': 'kumyk', 'kur': 'kurdo', 'kus': 'kusaie', 'kut': 'kootenai', 'lad': 'ladino', 'lah': 'lahndā', 'lam': 'lamba (Zambia y Congo)', 'lan': 'occitano (después de 1500)', 'lao': 'lao', 'lap': 'sami', 'lat': 'latín', 'lav': 'letón', 'lez': 'lezgiano', 'lim': 'limburgués', 'lin': 'lingala', 'lit': 'lituano', 'lol': 'mongo-nkundu', 'loz': 'lozi', 'ltz': 'luxemburgués', 'lua': 'luba-lulua', 'lub': 'luba-katanga', 'lug': 'ganda', 'lui': 'luiseño', 'lun': 'lunda', 'luo': 'luo (Kenia y Tanzania)', 'lus': 'lushai', 'mac': 'macedonio', 'mad': 'madurés', 'mag': 'magahi', 'mah': 'marshalés', 'mai': 'maithili', 'mak': 'makasar', 'mal': 'malayalam', 'man': 'mandingo', 'mao': 'maorí', 'map': 'austronesio (otros)', 'mar': 'marathi', 'mas': 'masái', 'max': 'manés', 'may': 'malayo', 'mdf': 'moksha', 'mdr': 'mandar', 'men': 'mende', 'mga': 'irlandés medio (ca. 1100-1550)', 'mic': 'micmac', 'min': 'minangkabau', 'mis': 'lenguas varias', 'mkh': 'mon-jemer (otros)', 'mla': 'malgache', 'mlg': 'malgache', 'mlt': 'maltés', 'mnc': 'manchú', 'mni': 'manipuri', 'mno': 'lenguas manobo', 'moh': 'mohawk', 'mol': 'moldavo', 'mon': 'mongol', 'mos': 'mooré', 'mul': 'varios idiomas', 'mun': 'munda (otros)', 'mus': 'creek', 'mwl': 'mirandés', 'mwr': 'marwari', 'myn': 'lenguas mayas', 'myv': 'erzya', 'nah': 'náhuatl', 'nai': 'indio norteamericano (otros)', 'nap': 'italiano napolitano', 'nau': 'nauruano', 'nav': 'navajo', 'nbl': 'ndebele (Sudáfrica)', 'nde': 'ndebele (Zimbabue)', 'ndo': 'ndonga', 'nds': 'bajo alemán', 'nep': 'nepalí', 'new': 'newari', 'nia': 'nias', 'nic': 'nigerocongo (otros)', 'niu': 'niueano', 'nno': 'noruego (nynorsk)', 'nob': 'noruego (bokmål)', 'nog': 'nogai', 'non': 'nórdico antiguo', 'nor': 'noruego', 'nqo': "n'ko", 'nso': 'sotho septentrional', 'nub': 'nilo-sahariano (otros)', 'nwc': 'newari antiguo', 'nya': 'nyanya', 'nym': 'nyamwesi', 'nyn': 'nyankole', 'nyo': 'nyoro', 'nzi': 'nzima', 'oci': 'occitano (después de 1500)', 'oji': 'ojibwa', 'ori': 'oriya', 'orm': 'oromo', 'osa': 'osage', 'oss': 'osetio', 'ota': 'turco otomano', 'oto': 'lenguas otomí', 'paa': 'papú (otros)', 'pag': 'pangasinán', 'pal': 'pahleví', 'pam': 'pampanga', 'pan': 'punjabi', 'pap': 'papiamento', 'pau': 'palauano', 'peo': 'persa antiguo (ca. 600-400 a.C.)', 'per': 'persa', 'phi': 'filipino (otros)', 'phn': 'fenicio', 'pli': 'pali', 'pol': 'polaco', 'pon': 'pohnpeiano', 'por': 'portugués', 'pra': 'prácrito', 'pro': 'provenzal (hasta 1500)', 'pus': 'pashto', 'que': 'quechua', 'raj': 'rajasthani', 'rap': 'rapanui', 'rar': 'rarotongano', 'roa': 'romance (otros)', 'roh': 'rético-romance', 'rom': 'romaní', 'rum': 'rumano', 'run': 'rundi', 'rup': 'aromaniano', 'rus': 'ruso', 'sad': 'sandawe', 'sag': 'sango (ubangiense criollo)', 'sah': 'yakuto', 'sai': 'indio sudamericano (otros)', 'sal': 'lenguas salish', 'sam': 'arameo samaritano', 'san': 'sánscrito', 'sao': 'samoano', 'sas': 'sasak', 'sat': 'santalí', 'scc': 'serbio', 'scn': 'siciliano italiano', 'sco': 'escocés', 'scr': 'croata', 'sel': 'selkup', 'sem': 'semítico (otros)', 'sga': 'irlandés antiguo (hasta 1100)', 'sgn': 'lenguas de signos', 'shn': 'shan', 'sho': 'shona', 'sid': 'sidamo', 'sin': 'cingalés', 'sio': 'siouan (otros)', 'sit': 'sino-tibetano (otros)', 'sla': 'eslavo (otros)', 'slo': 'eslovaco', 'slv': 'esloveno', 'sma': 'sami meridional', 'sme': 'sami septentrional', 'smi': 'sami', 'smj': 'sami lule', 'smn': 'sami inari', 'smo': 'samoano', 'sms': 'sami skolt', 'sna': 'shona', 'snd': 'sindhi', 'snh': 'cingalés', 'snk': 'soninké', 'sog': 'sogdiano', 'som': 'somalí', 'son': 'songhay', 'sot': 'sotho', 'spa': 'español', 'srd': 'sardo', 'srn': 'sranan', 'srp': 'serbio', 'srr': 'serer', 'ssa': 'nilosahariano (otros)', 'sso': 'sotho', 'ssw': 'suazi', 'suk': 'sukuma', 'sun': 'sundanés', 'sus': 'susu', 'sux': 'sumerio', 'swa': 'suajili', 'swe': 'sueco', 'swz': 'suazi', 'syc': 'siríaco', 'syr': 'siríaco moderno', 'tag': 'tagalo', 'tah': 'tahitiano', 'tai': 'tai (otros)', 'taj': 'tayiko', 'tam': 'tamil', 'tar': 'tártaro', 'tat': 'tártaro', 'tel': 'telugu', 'tem': 'temne', 'ter': 'terena', 'tet': 'tetum', 'tgk': 'tayiko', 'tgl': 'tagalo', 'tha': 'tailandés', 'tib': 'tibetano', 'tig': 'tigre', 'tir': 'tigriña', 'tiv': 'tiv', 'tkl': 'tokelauano', 'tlh': 'klingon (lengua artificial)', 'tli': 'tlingit', 'tmh': 'támazight', 'tog': 'tonga (Nyasa)', 'ton': 'tongano', 'tpi': 'tok pisin', 'tru': 'chuukés', 'tsi': 'tsimshiano', 'tsn': 'tswana', 'tso': 'tsonga', 'tsw': 'tswana', 'tuk': 'turcomano', 'tum': 'tumbuka', 'tup': 'lenguas tupi', 'tur': 'turco', 'tut': 'altaico (otros)', 'tvl': 'tuvaluano', 'twi': 'twi', 'tyv': 'tuviniano', 'udm': 'udmurto', 'uga': 'ugarítico', 'uig': 'uigur', 'ukr': 'ucraniano', 'umb': 'umbundu', 'und': 'indeterminado', 'urd': 'urdu', 'uzb': 'uzbeko', 'vai': 'vai', 'ven': 'venda', 'vie': 'vietnamita', 'vol': 'volapük', 'vot': 'votic', 'wak': 'lenguas wakash', 'wal': 'wolaytta', 'war': 'waray', 'was': 'washo', 'wel': 'galés', 'wen': 'sorbio (otro)', 'wln': 'walloon', 'wol': 'wolof', 'xal': 'oirat', 'xho': 'xhosa', 'yao': 'yao (África)', 'yap': 'yapés', 'yid': 'yiddish', 'yor': 'yoruba', 'ypk': 'lenguas yupik', 'zap': 'zapotec', 'zbl': 'símbolos Bliss', 'zen': 'zenaga', 'zha': 'zhuang', 'znd': 'lenguas zándicas', 'zul': 'zulú', 'zun': 'zuñi', 'zxx': 'Sin contenido:Optional[str] =Noneal', 'zza': 'Zazaki'}

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
    def splitter(self):
        return " /**/ "
    
    def stripper(f):
        def inner(*args):
            result:str = f(*args)
            if result:
                return result.strip()
            return result
        return inner
    
    def extract_values(self,dataset:str ,record:dict) -> tuple:
        result = []
        if dataset == "geo":
            result.append(record.get("001")[2:] if record.get("001") else uuid4().hex)
            result.append(record.get("001"))
            result.append(record.get("024"))
            result.append(record.get("034"))
            result.append(record.get("080"))
            result.append(record.get("151"))
            result.append(record.get("451"))
            result.append(record.get("510"))
            result.append(record.get("550"))
            result.append(record.get("551"))
            result.append(record.get("667"))
            result.append(record.get("670"))
            result.append(record.get("781"))
            humans = []
            # humans.append(self.dollar_parser(record.get("001"))  if record.get("001") else None)
            humans.append(self.other_identifiers(record.get("024")))
            humans.append(self.f_lat_lng(record.get("034")) if self.f_lat_lng(record.get("034")) else None)
            #CDU:
            humans.append(self.dollar_parser(record.get("080")) if record.get("080") else None)
            #nombre de lugar:
            humans.append(self.dollar_parser(record.get("151"))  if record.get("151") else None)
            #otros nombres de lugar
            humans.append(self.dollar_parser(record.get("451"))  if record.get("451") else None)
            #entidad relacionada
            humans.append(self.dollar_parser(record.get("510"))  if record.get("510") else None)
            #materia relacionada
            humans.append(self.dollar_parser(record.get("550"))  if record.get("550") else None)
            #lugar relacionado
            humans.append(self.related_place(record.get("551"))  if record.get("551") else None)
            #nota general
            humans.append(self.dollar_parser(record.get("667"))  if record.get("667") else None)
            #fuentes de información
            humans.append(self.sources(record.get("670"))  if record.get("670") else None)
            #lugar jerárquico
            humans.append(self.dollar_parser(record.get("781")) if record.get("781") else None)
            #obras relacionadas en el catálogo BNE
            humans.append(self.gen_url(record.get("001"))  if record.get("001") else None)
            result.extend(humans)

        elif dataset == "per":
            result.append(record.get("001")[2:] if record.get("001") else uuid4().hex)
            result.append(record.get("001"))
            result.append(record.get("024"))
            result.append(record.get("046"))
            result.append(record.get("100"))
            result.append(record.get("368"))
            result.append(record.get("370"))
            result.append(record.get("372"))
            result.append(record.get("373"))
            result.append(record.get("374"))
            result.append(record.get("375"))
            result.append(record.get("377"))
            result.append(record.get("400"))
            result.append(record.get("500"))
            result.append(record.get("510"))
            result.append(record.get("670"))
            #HUMANS:
            # otros_identificadores
            result.append(self.other_identifiers(record.get("024")))
            # fecha de nacimiento
            result.append(self.get_single_dollar(record.get("046"), "f"))
            # fecha de muerte
            result.append(self.get_single_dollar(record.get("046"), "g"))
            # nombre de persona
            result.append(self.per_person_name(record.get("100")))
            # otros atributos persona
            result.append(self.per_other_attributes(record.get("368")))
            #lugar de nacimiento
            result.append(self.get_single_dollar(record.get("370"), "a"))
            #lugar de muerte
            result.append(self.get_single_dollar(record.get("370"), "b"))
            #país relacionado
            result.append(self.get_single_dollar(record.get("370"), "c"))
            #otros lugares relacionados
            result.append(self.get_single_dollar(record.get("370"), "f"))
            #lugar residencia
            result.append(self.get_single_dollar(record.get("370"), "e"))
            #campo_actividad
            result.append(self.get_single_dollar(record.get("372"), "a"))
            #grupo o entidad relacionada
            result.append(self.group_or_entity(record))
            #ocupacion
            result.append(self.dollar_parser(record.get("374")))
            #género
            result.append(self.get_single_dollar(record.get("375"), "a"))
            #lengua
            result.append(self.get_single_dollar(record.get("377"), "l"))
            #otros nombres
            result.append(self.per_person_name(record.get("400")))
            #persona relacionada
            result.append(self.per_person_name(record.get("500")))
            #nota general
            # result.append(self.dollar_parser(record.get("667")))
            #fuentes de información
            result.append(self.per_other_sources(record.get("670")))
            #otros datos biográficos
            # result.append(self.dollar_parser(record.get("678")))
            #obras relacionadas en el catálogo BNE
            result.append(self.per_gen_url(record.get("001")))

        elif dataset == "mon":
            result.append(record.get("001")[2:] if record.get("001") else uuid4().hex)
            result.append(record.get("001"))
            result.append(record.get("008"))
            result.append(record.get("017"))
            result.append(record.get("020"))
            result.append(record.get("024"))
            result.append(record.get("035"))
            result.append(record.get("040"))
            result.append(record.get("041"))
            result.append(record.get("080"))
            result.append(record.get("100"))
            result.append(record.get("110"))
            result.append(record.get("130"))
            result.append(record.get("245"))
            result.append(record.get("246"))
            result.append(record.get("260"))
            result.append(record.get("264"))
            result.append(record.get("300"))
            result.append(record.get("440"))
            result.append(record.get("490"))
            result.append(record.get("500"))
            result.append(record.get("504"))
            result.append(record.get("505"))
            result.append(record.get("546"))
            result.append(record.get("561"))
            result.append(record.get("586"))
            result.append(record.get("594"))
            result.append(record.get("600"))
            result.append(record.get("610"))
            result.append(record.get("611"))
            result.append(record.get("630"))
            result.append(record.get("650"))
            result.append(record.get("651"))
            result.append(record.get("653"))
            result.append(record.get("655"))
            result.append(record.get("700"))
            result.append(record.get("710"))
            result.append(record.get("740"))
            result.append(record.get("752"))
            result.append(record.get("770"))
            result.append(record.get("772"))
            result.append(record.get("773"))
            result.append(record.get("774"))
            result.append(record.get("775"))
            result.append(record.get("776"))
            result.append(record.get("777"))
            result.append(record.get("787"))
            result.append(record.get("800"))
            result.append(record.get("810"))
            result.append(record.get("811"))
            result.append(record.get("830"))
            result.append(record.get("980"))
            result.append(record.get("994"))
            result.append(self.mon_per_id(record.get("100")))

            "Map dated Jun 5:"

            result.append(self.country_of_publication(record.get("008")))
            result.append(self.main_language(record.get("008")))
            result.append(self.other_languages(record.get("041")))
            result.append(self.original_language(record.get("041")))

            "Jun 6:"
            '''publication date:'''
            result.append(self.publication_date(record.get("008")))
            '''decade:'''
            result.append(self.decade(record.get("008")))
            '''century:'''
            result.append(self.century(record.get("008")))
            '''legal deposit:'''
            result.append(self.legal_deposit(record.get("017")))
            '''isbn:'''
            result.append(self.isbn(record.get("020")))
            '''nipo:'''
            result.append(self.isbn(record.get("024")))
            '''cdu:'''
            result.append(self.get_single_dollar(record.get("080"), "a"))
            "Autores:"
            result.append(self.mon_authors(record.get("100"), record.get("700")))
            "Título:"
            result.append(self.mon_title(record.get("245")))
            "Mención de autores:"
            result.append(self.get_single_dollar(record.get("245"), "c"))
            "Otros títulos:"
            result.append(self.mon_other_titles(record.get("246"), record.get("740")))
            "Edición:"
            result.append(self.mon_edition(record.get("250")))
            "Lugar de publicación:"
            result.append(self.mon_publication_place(record.get("260"), record.get("264")))
            "Editorial:"
            result.append(self.mon_publisher(record.get("260"), record.get("264")))
            "Extensión:"
            result.append(self.get_single_dollar(record.get("300"), "a"))
            "Otras características físicas:"
            result.append(self.get_single_dollar(record.get("300"), "b"))
            "Dimensiones:"
            result.append(self.get_single_dollar(record.get("300"), "c"))
            "Material anejo:"
            result.append(self.get_single_dollar(record.get("300"), "e"))
            "Serie:"
            result.append(self.mon_serie(record.get("440"), record.get("490")))
            "Nota de contenido:"
            result.append(self.get_single_dollar(record.get("505"), "a"))
            "Notas:"
            result.append(self.mon_notes(record))
            "Procedencia:"
            result.append(self.get_single_dollar(record.get("561"), "a"))
            "Premios:"
            result.append(self.get_single_dollar(record.get("586"), "a"))
            "Tema:"
            result.append(self.mon_subject(record, ("600", "610", "611", "630", "650", "651", "653")))
            "Genero forma:"
            result.append(self.mon_subject(record, ("655", "752", "770","772", "773", "774", "775", "776", "777", "787", "800", "810", "811", "830", "980")))
            "Tipo de documento:"
            result.append(self.mon_document_type(record.get("994")))

        elif dataset == "ent":
            result.append(record.get("001")[2:] if record.get("001") else uuid4().hex)
            result.append(record.get("001"))
            result.append(record.get("024"))
            result.append(record.get("046"))
            result.append(record.get("110"))
            result.append(record.get("368"))
            result.append(record.get("370"))
            result.append(record.get("372"))
            result.append(record.get("377"))
            result.append(record.get("410"))
            result.append(record.get("500"))
            result.append(record.get("510"))
            result.append(record.get("663"))
            result.append(record.get("665"))
            result.append(record.get("667"))
            result.append(record.get("670"))
            result.append(record.get("678"))
            '''
            HUMANS:
            '''
            "Otros identificadores:"
            result.append(self.ent_other_identifiers(record.get("024")))
            "fecha_establecimiento:"
            result.append(self.ent_establishment_date(record.get("046")))
            "fecha_finalización:"
            result.append(self.ent_finish_date(record.get("046")))
            '''Nombre de entidad:'''
            result.append(self.ent_entity_name(record.get("110")))
            '''Tipo de entidad:'''
            result.append(self.get_single_dollar(record.get("368"), "a"))
            '''País:'''
            result.append(self.get_single_dollar(record.get("370"), "c"))
            '''Sede:'''
            result.append(self.get_single_dollar(record.get("370"), "e"))
            '''Campo actividad:'''
            result.append(self.get_single_dollar(record.get("372"), "a"))
            '''Lengua:'''
            result.append(self.get_single_dollar(record.get("377"), "l"))
            '''otros nombres'''
            result.append(self.ent_entity_name(record.get("410")))
            '''Persona relacionada:'''
            result.append(self.per_person_name(record.get("500")))
            '''Grupo o entidad relacionada:'''
            result.append(self.ent_entity_name(record.get("510")))
            '''nota_de_relación:'''
            result.append(self.ent_relationship_note(record.get("663")))
            '''Otros datos históricos:'''
            d_665 = self.get_single_dollar(record.get("665"), "a")
            d_678 = self.get_single_dollar(record.get("678"), "a")
            if d_665 and d_678:
                result.append(self.get_single_dollar(record.get("665"), "a") + self.get_single_dollar(record.get("678"), "a"))
            elif d_665:
                result.append(self.get_single_dollar(record.get("665"), "a"))
            else:
                result.append(self.get_single_dollar(record.get("678"), "a"))


            '''Nota general:'''
            result.append(self.get_single_dollar(record.get("667"), "a"))
            '''Fuentes de información:'''
            result.append(self.per_other_sources(record.get("670")))
        
        return tuple(result)

    def get_single_dollar(self, value:str, dollar: str) -> str:
        if not value:
            return None
        re_selected_dollar = f"\|{dollar}([ \S]*?)\||\|{dollar}([ \S+]+)"
        value = re.search(re_selected_dollar, value)
        if value:
             for match in value.groups():
                  if match:
                       return match
    
    def dollar_parser(self, value: str) -> str:
        if not value:
            return None
        re_dollar = "\|\w{1}"
        result = re.sub(re_dollar, "", value, 1)
        result = re.sub(re_dollar, ", ", result)
        return result
    
    def other_identifiers(self, value:str) -> str:
        if not value:
            return None
        result = ""
        value_splitted = value.split(self.splitter)
        for v_s in value_splitted:
            try:
                _, url, source = re.split("\|\w{1}", v_s)
                result += f"{source}: {url}{self.splitter}"
            except Exception:
                    pass
        return result
    
    def related_place(self, value:str) -> str:
        result = ""
        value_splitted = value.split(self.splitter)
        for v_s in value_splitted:
            try:
                _, place = re.split("\|a", v_s, 1)
                # place = self.get_single_dollar(v_s, "a")
                result += f"{place}{self.splitter}"
            except Exception:
                pass
        return result
    
    def sources(self, value: str) -> str:
        result = ""
        value_splitted = value.split(self.splitter)
        for v_s in value_splitted:
            try:
                _, source, place = re.split("\|\w{1}", v_s)
                result += f"{source}: {place}{self.splitter}"
            except:
                pass
        return result

    def gen_url(self, value: str) -> str:
        result = "http://catalogo.bne.es/uhtbin/cgisirsi/0/x/0/05?searchdata1="
        result += value[4:]
        return result          

    def f_lat_lng(self, v):
        re_coord = "\w{2}\d{1,}"
        result = ""
        try:
            a = re.findall(re_coord, v)
            for i, coord in enumerate(a):
                if i % 2 == 0:
                    coord = coord[1:]
                    c_point = coord[0]
                    digits = coord[1:]
                    n = float(f"{digits[0:3]}.{digits[3:]}")
                    if c_point == "W" or c_point == "E":
                        if c_point == "W":
                            n = -n
                        result += f"{n}"
                    else:
                        if c_point == "S":
                            n = -n
                        result += f", {n}"
        
    
            return result
        except:
            return None

    '''
    PER:
    '''

    def per_geo_id(self, v: str) -> str:
        '''
        This would get de geo id from the 370's
        '''
        if v: 
            result = re.findall("XX\d{4,7}", v)
            if len(result):
                return result[0]
        else:
            return        

    def per_person_name(self, value: str) -> str:
        if not value:
            return
        dollar_a = self.get_single_dollar(value, "a")
        result = f"{dollar_a}"
        dollar_b = self.get_single_dollar(value, "b")
        if dollar_b:
            result += f", {dollar_b}"
        dollar_c = self.get_single_dollar(value, "c")
        if dollar_c:
            result += f", {dollar_c}"
        dollar_d = self.get_single_dollar(value, "d")
        if dollar_d:
            result += f", ({dollar_d})" 
        dollar_q = self.get_single_dollar(value, "q")
        if dollar_q:
            result += f", ({dollar_q})"
        return result
    
    def per_other_attributes(self, value:str) -> str:
        if not value:
            return
        result = ""
        value_splitted = value.split(self.splitter)
        for v_s in value_splitted:
            try:
                if self.get_single_dollar(v_s, "c"):
                    result += self.get_single_dollar(v_s, "c") + self.splitter
                if self.get_single_dollar(v_s, "d"):
                    result += self.get_single_dollar(v_s, "d") + self.splitter
            except Exception:
                    pass
        return result[0:-6]
        
    def per_other_sources(self, value:str) -> str:
        if not value:
            return
        result = ""
        for v_s in value.split(self.splitter):
            dollar_a = self.get_single_dollar(v_s, "a")
            dollar_b = self.get_single_dollar(v_s, "b")
            dollar_u = self.get_single_dollar(v_s, "u")
            if dollar_a and dollar_b:
                if result:
                    result += f", {dollar_a}: {dollar_b}"
                else:
                    result = f"{dollar_a}: {dollar_b}"
                if dollar_u:
                    result += f" ({dollar_u})"
        return result
    
    def per_gen_url(self, value: str) -> str:
        if not value:
            return None
        result = "http://catalogo.bne.es/uhtbin/cgisirsi/0/x/0/05?searchdata1=%5ea"
        result += value[4:]
        return result   

    def group_or_entity(self, record:dict) -> str:
        t_373 = record.get("373")
        t_510 = record.get("510")
        if not t_373 and not t_510:
            return
        result = ""
        if t_373:
            t_373 = self.dollar_parser(t_373)
            for value in t_373.split("/**/"):
                result += value.split(", ")[0]
        if t_510:
            t_510 = self.dollar_parser(t_510)
            result += f"{self.splitter}{t_510}"
        return result

    def get_all_by_single_dollar(self, value: str, dollar:str) -> str:
        if not value:
            return
        result = ""
        for v_s in value.split(self.splitter):
            try:
                result += self.get_single_dollar(v_s, dollar)
            except:
                pass
        return result

    '''
    MON:
    '''

    def mon_per_id(self, value:str) -> str:
        if not value:
            return
        result = self.get_single_dollar(value, "0")
        if result:
            return result
    
    def country_of_publication(self, value:str) -> str:
        if not value:
            return
        try:
            return self.countries[value[17:21].strip()]
        except:
            return value[17:21].strip()
    
    def main_language(self, value:str) -> str:
        if not value:
            return
        try:
            return self.languages[value[38:41].strip()]
        except:
            return value[38:41].strip()

    def other_languages(self, value:str) -> str:
        if not value:
            return
        r = []
        dollars = ["b", "d", "f", "j", "k"]
        for d in dollars:
            lang = self.get_single_dollar(value, d)
            while lang:
                r.append(lang)
                value = value.replace(f"|{d}{lang}", "")
                lang = self.get_single_dollar(value, d)
        result = ""
        for v in r:
            lang = self.languages.get(v.strip())
            if lang:
                result += f"{lang}, "
            else:
                result += f"{v}, "
        return result[0:-2]
    
    def original_language(self, value:str) -> str:
        if not value:
            return
        lang = self.get_single_dollar(value, "h")
        if lang:
            lang = self.languages.get(lang.strip())
            return lang
    
    def publication_date(self, value:str) -> str:
        if not value:
            return
        return value[10:14]
    
    def decade(self, value:str) -> str:
        if not value:
            return
        n:str = value[10:14]
        try:
            if n[2].isdigit():
                return f"{n[2]}0"
        except IndexError:
            return
    
    def century(self, value:str) -> str:
        if not value:
            return
        centuries = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI"]
        n = value[10:14]
        n = re.sub("(?![0-9]).", "0", n)
        try:
            return centuries[int(n)//100]
        except:
            return f"{value} CENTURY"
    
    def legal_deposit(self, value:str) -> str:
        if not value:
            return
        r = ""
        catched: str = self.get_single_dollar(value, "a")
        while catched:
            value = value.replace(f"|a{catched}", "")
            r += f"{catched}{self.splitter}"
            catched = self.get_single_dollar(value,"a")
        return r[:-6]
    
    def isbn(self,value:str) -> str:
        '''
        This would be used for NIPO too
        '''
        if not value:
            return
        r = ""
        for s in value.split(self.splitter):
            d_a = self.get_single_dollar(s, "a")
            d_q = self.get_single_dollar(s, "q")
            if d_q:
                r += f"{d_a} ({d_q}) {self.splitter}"
                continue
            r+= f"{d_a} {self.splitter}"
        return r[:-7]

    def mon_authors(self, value_100:str, value_700:str) -> str:
        if not value_100:
            return
        
        value_100_e = self.get_single_dollar(value_100, "e")
        value_100 = self.per_person_name(value_100)
        if value_100_e:
            value_100 = f"{value_100}({value_100_e})"
        if value_700:
            value_700_e = self.get_single_dollar(value_700, "e")
            value_700 = self.per_person_name(value_700)
            if value_700_e:
                value_700 = f"{value_700}({value_700_e})"
        if value_700:
            return f"{value_100} /**/ {value_700}"
        return value_100

    def mon_title(self, value:str) -> str:
        '''245: Mención de autores |a:|b.|n,|p'''
        if not value:
            return
        r = ""
        d_a = self.get_single_dollar(value,"a")
        d_b = self.get_single_dollar(value,"b")
        d_n = self.get_single_dollar(value,"n")
        d_p = self.get_single_dollar(value,"p")
        r += f"{d_a}: "
        if d_b:
            r+=f"{d_b}. "
        if d_n:
            r+=f"{d_n}, "
        if d_p:
            r+=f"{d_p}"
        return r.strip()
    
    def mon_other_titles(self, value_246:str, value_740:str) -> str:
        '''
        246: otros títulos [|i]:|a:|b.|n,|p
        740: |a.|n,|p
        '''
        if not value_246:
            return
        r = ""
        d_i = self.get_single_dollar(value_246, "i")
        d_a = self.get_single_dollar(value_246, "a")
        d_b = self.get_single_dollar(value_246, "b")
        d_n = self.get_single_dollar(value_246, "n")
        d_p = self.get_single_dollar(value_246, "p")
        if d_i:
            r += f"{d_i}: "
        r += f"{d_a}: "
        if d_b:
            r += f"{d_b}. "
        if d_n:
            r += f"{d_n}, "
        if d_p:
            r += d_p
        if not value_740:
            return r
        r += self.splitter
        d_a = self.get_single_dollar(value_740, "a")
        d_n = self.get_single_dollar(value_740, "n")
        d_p = self.get_single_dollar(value_740, "p")
        r += d_a
        if d_n:
            r += f". {d_n}. "
        if d_p:
            r += f"{d_p}"
        return r
    
    def mon_edition(self, value:str) -> str:
        "250 edición |a, |b"
        if not value:
            return
        d_a = self.get_single_dollar(value, "a")
        d_b = self.get_single_dollar(value, "b")
        r = d_a
        if d_b:
            r += f", {d_b}"
        return r
    
    def mon_publication_place(self, value_260:str, value_264:str) -> str:
        "260: |a 264: |a lugar de publicación\nsolo uno"
        if not value_260 and not value_264:
            return
        if value_260:
            return self.get_single_dollar(value_260, "a")
        return self.get_single_dollar(value_264, "a")
    
    def mon_publisher(self, value_260:str, value_264:str) -> str:
        "260: |b 264: |b lugar de publicación\nsolo uno"
        if not value_260 and not value_264:
            return
        if value_260:
            return self.get_single_dollar(value_260, "b")
        return self.get_single_dollar(value_264, "b")
    
    def mon_serie(self, value_440:str, value_490:str) -> str:
        "440: |a|v splitter 490 |a|v"
        if not value_440 and not value_490:
            return
        r = ""
        d_a = self.get_single_dollar(value_440, "a")
        d_v = self.get_single_dollar(value_440, "v")
        if d_a:
            r += d_a
        if d_v:
            r+= d_v
        d_a = self.get_single_dollar(value_490, "a")
        d_v = self.get_single_dollar(value_490, "v")
        if d_a:
            if value_440:
                r += self.splitter
            r += d_a
        if d_v:
            r+= d_v
        return r

    def mon_notes(self, record:dict) -> str:
        '''"500","594","504","563","546":|a'''
        dollars = ("500","594","504","563","546")
        r = ""
        for d in dollars:
            d = self.get_single_dollar(record.get(d), "a")
            if d:
                r += f"{d}{self.splitter}"
        if r:
            return r[:-6]    
    
    def mon_subject(self, record:dict, dollars:tuple) -> str:
        '''
        600
        610
        611
        630
        650
        651
        653
        '''
        r = ""
        for d in dollars:
            d:str = record.get(d)
            if d:
                d_2 = self.get_single_dollar(d, "2")
                d = d.replace(f"|2{d_2}", "") 
                d = re.split("\|[a-z0-13-9]{1}", d)
                for v in d:
                    if v:
                        r += f"{v} - "
        if r:
            return r[:-3]
    
    def mon_document_type(self, value:str) -> str:
        '''994:a\nsi |aMONOMODER: "Monografía en papel (posterior a 1830)"\nsi |aMONOMODER-RECELE: "Monografía electrónica"'''
        if not value:
            return
        r = ""
        d_a = self.get_single_dollar(value, "a")
        if d_a:
            if d_a.find("MONOMODER:") >= 0:
                r = f"Monografía en papel (posterior a 1830)"
                return r
            return 'MONOMODER-RECELE: "Monografía electrónica"'
    
    '''
    ENT:
    '''

    def ent_other_identifiers(self, value:str) -> str:
        '''024 -> |2: |a'''
        if not value:
            return
        d_2 = self.get_single_dollar(value, "2")
        d_a = self.get_single_dollar(value, "a")
        return f"{d_2}: {d_a}"
    
    @stripper   
    def ent_establishment_date(self, value:str) -> str:
        '''046 -> IF |q -> q || | !|q -> |s'''
        if not value:
            return
        d_q = self.get_single_dollar(value, "q")
        if d_q:
            return d_q
        d_s = self.get_single_dollar(value, "s")
        if d_s:
            return d_s
    
    @stripper
    def ent_finish_date(self, value:str) -> str:
        '''
        046: r?r:t
        '''
        if not value:
            return
        d_r = self.get_single_dollar(value, "r")
        if d_r:
            return d_r
        d_t = self.get_single_dollar(value, "t")
        if d_t:
            return d_t

    @stripper
    def ent_entity_name(self, value:str) -> str:
        '''
        110: |a, |b, |b...(|e)
        '''
        if not value:
            return
        d_a = self.get_single_dollar(value, "a")
        d_b = self.get_single_dollar(value, "b")
        d_e = self.get_single_dollar(value, "e")
        if d_b:
            if d_e:
                return f"{d_a}, {d_b}, {d_b}...{d_e}"
            return f"{d_a}, {d_b}, {d_b}..."
        return d_a
    
    @stripper
    def ent_relationship_note(self, value:str) -> str:
        '''663: |a all_|b, '''
        if not value:
            return
        d_a = self.get_single_dollar(value, "a")
        d_bs = ""
        while self.get_single_dollar(value, "b"):
            d_b = self.get_single_dollar(value, "b")
            d_bs += f"{d_b.strip()}, "
            value = value.replace(f"|b{d_b}", "")
        return f"{d_a} {d_bs[:-2]}"
     
    def insert(self):
        res_json = {"success":False}
        with open(f"converter/{self.dataset}.json", encoding="utf-8") as file:
            print(models.get(self.dataset))
            self.cur.execute(models.get(self.dataset))
            self.cur.execute(models.get(f"{self.dataset}_fts"))
            self.con.commit()
            s = time.perf_counter()
            data = json.loads(file.read())
            data = data
            query = f"insert or ignore into {self.dataset}_fts values ({'?, '*len(self.available_fields)})"
            print(self.available_fields)
            query = query.replace(", )", ")")
            print(query.center(50 + len(query), "#"))
            self.cur.executemany(query,map(lambda record: self.extract_values(self.dataset, record), data))
            self.con.commit()
            res_json["success"] = True
            res_json["time"] = time.perf_counter() - s
            return res_json