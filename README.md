# TokuSuperheroes

## Proyecto para la prueba de Superheroes API para la empresa Toku

El siguiente proyecto fue programado con un backend escrito en Python con el framework FastApi y frontend en JavaScript con la librería React,
con el fin de facilitar su despliegue, el proyecto completo está contenerizado en Docker con docker compose V2 para que se pueda levantar con el siguiente comando.

### `docker compose up`

En el caso de querer levantar la aplicación reconstruyendo los contenedores se utilizará el siguiente comando.

### `docker compose up --build -d`

Las características son las siguientes:

1. Se crean los equipos generando IDs aleatorias para luego obtener la información de cada personaje consumiendo SuperHeroes API asincrónicamente.
2. Una vez obtenida la información, se calculan las estadísticas según la fórmula ofrecida y se envía al frontend.
3. Se habilitó un endpoint de simular batalla para poder probar hacer la simulación todas las veces que se quiera.
4. Se habilitó un endpoint para envío de correo por mailgun para enviar un resumen de las batallas.

Observaciones:

1. Primero tuve el interés de desarrollar el backend con Python/Django por ser un framework robusto, sin embargo, durante el desarrollo lo descarté
por poseer muchas características que finalmente no utilicé, por lo que consumía recursos de forma innecesaria, reduciendo el rendimiento, finalmente
me decidí por desarrollar el backend en FastApi por la simpleza de su sintaxis, permitiendo hacer lo mismo que quería hacer en Django con menos código
y con mayor rendimiento. Para declarar un registro de esta observación mantuve el framework anterior bajo el nombre de `backend_old`

Este proyecto fue hecho con ♥ por Ignacio Figueroa.

