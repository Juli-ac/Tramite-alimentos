# TrámiteAlimentos

Guía práctica de trámites alimentarios de la Provincia de Buenos Aires.
Es un sitio estático (HTML, CSS y JavaScript): funciona directo en GitHub Pages, sin servidor ni base de datos.

## Cómo publicarlo en GitHub Pages

1. Creá un repositorio nuevo en GitHub (por ejemplo, `tramite-alimentos`).
2. Subí **todo el contenido de la carpeta `sitio/`** a la raíz del repositorio: `index.html`, `guias/`, `assets/`, etc.
3. En el repo, andá a **Settings → Pages → Source: Deploy from a branch → main / (root)** y guardá.
4. En uno o dos minutos queda en `https://TU-USUARIO.github.io/tramite-alimentos/`.

## Cómo editar el contenido

**Opción A: editar el HTML directamente.** Cada ficha es un archivo en `guias/`. Sirve para cambios chicos, como corregir un dato o actualizar una fecha.

**Opción B (recomendada): editar los datos y regenerar el sitio.**
1. Abrí `fichas.py`: ahí está todo el contenido (fichas, novedades y fecha de revisión).
2. Cambiá lo que necesites. Por ejemplo, pasá `estado="rev"` a `estado="ok"` cuando confirmes los datos, o cambiá `REVISION`.
3. Corré `python3 build.py`. Se regenera la carpeta `sitio/` completa, con el menú, el buscador y la ruta guiada actualizados.
4. Subí la carpeta `sitio/` a GitHub.

El nombre del sitio (`NOMBRE`) y el link a la asesoría se cambian al principio de `build.py` y de `fichas.py`.

## Estructura

```
sitio/
├── index.html            Inicio
├── que-necesito.html     Ruta guiada (4 preguntas)
├── novedades.html        Novedades normativas
├── 404.html
├── guias/
│   ├── index.html        Todas las fichas, con filtro
│   └── *.html            Las 10 fichas
└── assets/
    ├── style.css
    ├── app.js            Menú, buscador, filtro y ruta guiada
    └── search-index.js   Índice del buscador (lo genera build.py)
```
