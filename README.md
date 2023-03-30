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
* Caso fallido
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
    "lugar_jerarquico": "España, Cataluña",
    ...
    },
    ...
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
* Cada campo adicional debe ser separado por comas.

Ejemplo de respuesta:
```json
"success": true,
"length": 10,
"time": 0.01,
"data": [
    {
    "id":"XX450536",
    "t_024": "|ahttp://id.loc.gov/authorities/names/n79089624|2lcnaf /**/ |ahttp://viaf.org/viaf/316429160|2viaf"
    },
    ...
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
* El valor introducido será buscado dentro del campo diana/objetivo. Si indicamos <strong>esp</strong> en el campo <strong>lugar_jerarquico</strong> entregará todos los registros que cotengan las letras <strong>esp</strong>

Ejemplo de respuesta:
```js
GET /geo?lugar_jerarquico=esp
```
```json
"success": true,
"length": 1000,
"time": 0.0123...,
"data": [
    {
    "id":"XX450537",
    "lugar_jerarquico": "España, Andalucía",
    ...
    },
    ...
]
```

# Diagramas

![request api](https://raw.githubusercontent.com/vgenov-py/bne_api/develop/draw/request_api.png)

### Modelo geográfico

![Modelo geográfico](https://raw.githubusercontent.com/vgenov-py/bne_api/develop/draw/geo_model.png)

### Modelo persona

![Modelo persona](https://raw.githubusercontent.com/vgenov-py/bne_api/develop/draw/per_model.png)