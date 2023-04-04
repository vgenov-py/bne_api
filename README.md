# BNE API

### Para hacer uso del API deberá indicar el conjunto de datos a consultar

URL BASE: http://139.162.183.85/api
```
Geográfico: geo,
Persona: per,
Monografías modernas: mon
```

## dataset
```js
GET /geo
```
* Las respuestas serán emitidas en formato JSON y contarán con las siguientes claves en el caso exitoso:
```
success: boolean
length: integer
time: float
data: array 
```
* Caso fallido:
```
success: boolean
message: str
```

### Ejemplo de respuesta:
```json
"success": true,
"length": 1000,
"time": 0.01,
"data": [
    {
    "id":"XX450536",
    "lugar_jerarquico": "España, Cataluña"
    }
]
```
## Parámetros opcionales:


## limit
```js
GET /geo?limit=10
```
* El parámetro <strong>limit</strong> permite limitar la cantidad de resultados a mostrar, el valor por defecto es 1000.

## fields

```js
GET /geo?limit=10&fields=id,t_024
```

* El parámetro <strong>fields</strong> permite seleccionar los campos a mostrar por cada registro.
* Cada campo adicional deberá ser separado por comas.

Ejemplo de respuesta:
```js
GET /geo?t_024=viaf&fields=id,t_024
```
```json
"success": true,
"length": 10,
"time": 0.01,
"data": [
    {
    "id":"XX450536",
    "t_024": "|ahttp://id.loc.gov/authorities/names/n79089624|2lcnaf /**/ |ahttp://viaf.org/viaf/316429160|2viaf"
    }
]
```

Si indicamos un campo inexistente en el conjunto se mostrará el siguiente error:

```json
"success": false,
"message": "This field doesn't exist in the db: 1 - available fields: ('id', 't_001', 't_024'..."
```

### Campos filtro

Para filtrar una búsqueda por un determinado valor deberemos indicar como parámetro la columna a buscar y el valor por el cual queramos filtrar.

```js
GET /geo?t_024=Andalucía
```

* Las etiquetas MARC deben ser indicadas con el prefijo <strong>t_</strong>
* Cada filtro adicional debe ser agregado como un nuevo parámetro utilizando el caracter <strong>&</strong>

```js
GET /geo?t_024=Andalucía&lugar_jerarquico=España
```

* La búsqueda será <strong>insensible</strong> a las mayúsculas.
* El valor introducido será buscado dentro del campo diana/objetivo. Si indicamos <strong>esp</strong> en el campo <strong>lugar_jerarquico</strong> entregará todos los registros que contengan las letras <strong>esp</strong>

Ejemplo de respuesta:
```js
GET /geo?lugar_jerarquico=esp
```
```json
"success": true,
"length": 1000,
"time": 0.0123,
"data": [
    {
    "id":"XX450537",
    "lugar_jerarquico": "España, Andalucía"
    }
]
```

Por defecto todo filtro, será agregado con un operador <strong>AND</strong>, si queremos utilizar el operador <strong>OR</strong>, agregar <strong>||</strong> al final del valor 

Ejemplo de respuesta:
```js
GET /per?t_100=fernández||&nombre_de_persona=sánchez
```
```json
"success": true,
"length": 1000,
"time": 0.0123,
"data": [
    {
    "id":"XX819245",
    "t_100": "|aSánchez del Águila, José Manuel|d1957-",
    "nombre_de_persona": "Sánchez del Águila, José Manuel, (1957-)"
    },
    {
        "id":"XX819498",
        "t_100": "|aFernández Ferrer, María José",
        "nombre_de_persona":"Fernández Ferrer, María José"
    }
]
```
Buscar diferentes ocurrencias en un mismo campo
Si queremos buscar múltiples ocurrencias en un mismo campo, debemos separar cada uno de ellos con el operador <strong>OR</strong> -> <strong>||</strong>

Ejemplo de respuesta:
```js
GET /per?t_100=fernández||sánchez
```
```json
"success": true,
"length": 1000,
"time": 0.0123,
"data": [
    {
    "id":"XX819245",
    "t_100": "|aSánchez del Águila, José Manuel|d1957-",
    "nombre_de_persona": "Sánchez del Águila, José Manuel, (1957-)"
    },
    {
        "id":"XX819498",
        "t_100": "|aFernández Ferrer, María José",
        "nombre_de_persona":"Fernández Ferrer, María José"
    }
]
```


Es posible hacer búsquedas "negativas", para éste cometido agregar <strong>!</strong> al principio del valor.
Ejemplo de respuesta:
```js
GET /geo?lugar_jerarquico=!esp
```
```json
"success": true,
"length": 1000,
"time": 0.0123,
"data": [
    {
    "id":"XX450557",
    "lugar_jerarquico": "Gran Bretaña, Escocia"
    }
]
```
Es posible buscar campos sin valor, utilizar <strong>null</strong> o <strong>!null</strong> para buscar campos con valor

Ejemplo de respuesta:
```js
GET /geo?lugar_jerarquico=null
```
```json
"success": true,
"length": 1000,
"time": 0.0123,
"data": [
    {
    "id":"XX450557",
    "lugar_jerarquico": null
    }
]
```

# Diagramas

![request api](https://raw.githubusercontent.com/vgenov-py/bne_api/develop/draw/request_api.png)

### Modelo geográfico

![Modelo geográfico](https://raw.githubusercontent.com/vgenov-py/bne_api/develop/draw/geo_model.png)

### Modelo persona

![Modelo persona](https://raw.githubusercontent.com/vgenov-py/bne_api/develop/draw/per_model.png)