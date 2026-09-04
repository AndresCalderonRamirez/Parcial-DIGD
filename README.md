# Parcial-DIGD — Análisis del dataset MovieLens 32M

Parcial de la materia **Análisis de Datos (DIGD)**. El repositorio contiene el proceso completo de
limpieza y exploración del dataset **MovieLens ml-32m**, más el análisis de la relación entre ese
dataset y el top 20 de películas favoritas del grupo.

## Grupo 2

| Integrante |
|---|
| Andrés Felipe Calderón Ramírez |
| Ricardo Andrés Ayala Garzón |
| Jonatan Palomares Castañeda |
| Juan Carlos Bohórquez Monroy |
| Juan Esteban Téllez Valencia |

---

## 1. El dataset

**MovieLens 32M (`ml-32m`)**, publicado por GroupLens (University of Minnesota). Describe la
actividad de calificación (escala de 5 estrellas, en pasos de media estrella) y de etiquetado de
texto libre del servicio de recomendación MovieLens.

* Generado el **13 de octubre de 2023**, con actividad registrada entre el **9 de enero de 1995** y
  el **12 de octubre de 2023**.
* Los usuarios fueron seleccionados al azar y todos habían calificado al menos 20 películas. No hay
  información demográfica: cada usuario es solo un identificador anonimizado.
* Solo se incluyen películas con al menos una calificación o una etiqueta.
* `movieId` y `userId` son consistentes entre todos los archivos.

### Tamaños: datos crudos vs. datos procesados

| Tabla | Crudo (`ml-32m`) | Procesado (`data/processed`) | Registros conservados |
|---|---:|---:|---:|
| `movies` | 87,585 | **86,967** | 99.294% |
| `ratings` | 32,000,204 | **31,963,989** | 99.887% |
| `tags` | 2,000,072 | **1,992,636** | 99.628% |

> **Importante:** los notebooks de exploración trabajan **siempre** con los archivos procesados. La
> cifra de 32,000,204 calificaciones pertenece al dataset crudo y **no** debe citarse como resultado
> del análisis.

### Esquema de los datos procesados

```
movies.csv    movieId, title, genres, release_year
              86,967 filas · una fila = una película
              title sin el año (se extrajo a release_year, con formato YYYY-01-01)
              genres separados por '|' (18 géneros válidos + "(no genres listed)")

ratings.csv   userId, movieId, rating, rating_datetime
              31,963,989 filas · una fila = una calificación de un usuario a una película
              rating entre 0.5 y 5.0 en pasos de 0.5 · sin duplicados de (userId, movieId)

tags.csv      userId, movieId, tag, tag_datetime
              1,992,636 filas · una fila = una etiqueta aplicada por un usuario a una película
```

Modelo relacional:

```
movies.movieId (PK)
   ├── ratings.movieId  (FK)   →  PK compuesta: (userId, movieId)
   └── tags.movieId     (FK)   →  PK compuesta: (userId, movieId, tag)

ratings.userId  ←→  tags.userId   (el mismo usuario en ambas tablas)
```

`links.csv` (IMDb/TMDb) del dataset original **no** forma parte de los datos procesados, así que no
hay metadatos externos como reparto, dirección o taquilla.

### Limpieza aplicada (`presentation_cleaning.ipynb`)

* Se extrajo `release_year` desde el título y se eliminaron las películas sin año.
* Se eliminó la única película con título vacío.
* Se convirtieron los `timestamp` UNIX a `rating_datetime` y `tag_datetime`.
* Se eliminaron los tags y los ratings que no apuntan a ninguna película del catálogo.
* Se eliminaron los tags nulos y las tuplas `(userId, movieId, tag)` duplicadas (comparando en
  minúsculas).
* Se eliminaron las calificaciones **anteriores** a la fecha de estreno de la película.

---

## 2. Estructura del repositorio

```
Parcial-DIGD/
├── data/                                  # ignorado por git (ver .gitignore)
│   ├── raw/                               # CSV originales de ml-32m (solo para la limpieza)
│   └── processed/                         # CSV limpios: movies.csv, ratings.csv, tags.csv
├── notebooks/
│   ├── presentation_cleaning/
│   │   └── presentation_cleaning.ipynb    # descripción del dataset + limpieza
│   └── exploration/
│       ├── main/                          # exploración por tabla y por combinaciones
│       │   ├── movies.ipynb
│       │   ├── ratings.ipynb
│       │   ├── tags.ipynb
│       │   ├── movies_ratings.ipynb
│       │   ├── movies_tags.ipynb
│       │   ├── ratings_tags.ipynb
│       │   └── movies_tags_ratings.ipynb
│       └── group_20_movies/
│           └── group_20_movies.ipynb      # top 20 del grupo vs. dataset procesado
├── src/parcial_digd/
│   └── utils_.py                          # utilidades compartidas (columnas de género)
├── pyproject.toml                         # dependencias del proyecto
├── uv.lock                                # versiones bloqueadas
└── .python-version                        # 3.12
```

### Notebooks y responsables

| Notebook | Contenido | Responsable(s) |
|---|---|---|
| `presentation_cleaning.ipynb` | Descripción del dataset y limpieza completa | Jonatan Palomares Castañeda |
| `main/movies.ipynb` | Catálogo: géneros, años de estreno, cobertura | Andrés Felipe Calderón Ramírez |
| `main/ratings.ipynb` | Calificaciones: distribución y actividad por usuario | Andrés Felipe Calderón Ramírez |
| `main/tags.ipynb` | Etiquetas: vocabulario, calidad del texto, concentración | Andrés Felipe Calderón Ramírez · Ricardo Andrés Ayala Garzón |
| `main/movies_ratings.ipynb` | Popularidad vs. calidad, géneros y evolución temporal | Ricardo Andrés Ayala Garzón |
| `main/movies_tags.ipynb` | Perfilamiento de películas por etiquetas | Juan Carlos Bohórquez Monroy |
| `main/ratings_tags.ipynb` | Patrones de opinión de los usuarios | Juan Carlos Bohórquez Monroy |
| `main/movies_tags_ratings.ipynb` | Integración de las tres tablas | Ricardo Andrés Ayala Garzón |
| `group_20_movies/group_20_movies.ipynb` | Top 20 del grupo dentro del dataset | Juan Esteban Téllez Valencia |

---

## 3. Instalación

### Requisitos

* **Python 3.12** o superior (el proyecto fija `3.12` en `.python-version`).
* **[uv](https://docs.astral.sh/uv/)** como gestor de entorno y dependencias (recomendado).
* Al menos **8 GB de RAM libres** para los notebooks que cargan `ratings.csv` completo.
* Unos **3 GB de disco** para los datos (procesados y, opcionalmente, crudos).

### Opción A — con `uv` (recomendada)

```bash
# 1. Clonar el repositorio
git clone https://github.com/AndresCalderonRamirez/Parcial-DIGD.git
cd Parcial-DIGD

# 2. Crear el entorno e instalar TODAS las dependencias, incluidas las de desarrollo
#    (jupyterlab, ipykernel, ruff). uv descarga Python 3.12 solo si hace falta.
uv sync

# 3. Abrir JupyterLab
uv run jupyter lab
```

`uv sync` crea la carpeta `.venv/` en la raíz del proyecto (ignorada por git) e instala las versiones
exactas de `uv.lock`, de modo que todos los integrantes trabajan con el mismo entorno.

### Opción B — con `venv` y `pip`

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Linux / macOS
source .venv/bin/activate

pip install "pandas>=3.0.5" "numpy>=2.5.2" "matplotlib>=3.11.1" "seaborn>=0.13.2" jupyterlab ipykernel
pip install -e .          # instala el paquete local parcial_digd

jupyter lab
```

### Ejecutar un notebook sin abrir JupyterLab

```bash
cd notebooks/exploration/group_20_movies
uv run jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=1800 group_20_movies.ipynb
```

---

## 4. Preparación de los datos

Los CSV **no están en el repositorio**: `.gitignore` excluye la carpeta `data/` porque `ratings.csv`
pesa más de 1 GB. Hay que colocarlos manualmente antes de ejecutar cualquier notebook.

1. Consigue el archivo **`processed.zip`** que comparte el equipo.
2. Descomprímelo y deja los tres CSV directamente dentro de `data/processed/`.

La estructura final debe ser **exactamente** esta:

```
Parcial-DIGD/
└── data/
    └── processed/
        ├── movies.csv     (~4.5 MB)
        ├── ratings.csv    (~1.2 GB)
        └── tags.csv       (~90 MB)
```

> Al descomprimir, algunos gestores crean una carpeta intermedia (`data/processed/processed/...`).
> Si ocurre, mueve los CSV un nivel hacia arriba: los notebooks buscan `data/processed/movies.csv`,
> no `data/processed/processed/movies.csv`.

Solo si vas a **re-ejecutar la limpieza** necesitas además los datos crudos: descarga
[`ml-32m.zip`](https://files.grouplens.org/datasets/movielens/ml-32m.zip) y deja `movies.csv`,
`ratings.csv`, `tags.csv` y `links.csv` dentro de `data/raw/`.

### Verificar que los datos son los correctos

```bash
uv run python -c "for a, n in [('movies', 86967), ('tags', 1992636), ('ratings', 31963989)]: f = open(f'data/processed/{a}.csv', encoding='utf-8'); r = sum(1 for _ in f) - 1; print(a, r, 'OK' if r == n else f'ATENCION: se esperaban {n}')"
```

---

## 5. Cosas a tener en cuenta

**Datos**

* **Usa siempre `data/processed`.** No mezcles cifras de `data/raw` con resultados del análisis: el
  dataset crudo tiene 32,000,204 calificaciones y el procesado 31,963,989.
* **Nunca subas los CSV al remoto.** `data/` está en `.gitignore`; no lo quites ni uses `git add -f`
  sobre esa carpeta.
* `movieId` llega hasta 292,757 aunque solo hay 86,967 películas: es el identificador original de
  MovieLens, no un índice secuencial del subconjunto.
* 3,115 películas del catálogo no tienen ninguna calificación.

**Ejecución de los notebooks**

* **Ábrelos desde su propia carpeta**: las rutas son relativas (`../../../data/processed/...`).
  Ejecutarlos desde la raíz del repositorio rompe la carga de datos.
* Selecciona el kernel del entorno del proyecto (`.venv`), no una instalación global de Python.
* Los notebooks importan las utilidades comunes con este patrón, ya incluido en cada uno:

  ```python
  import os, sys
  project_root = os.path.abspath('../../..')
  sys.path.insert(0, os.path.join(project_root, 'src'))
  from parcial_digd import utils_
  ```

**Memoria y rendimiento**

* `ratings.csv` tiene 32 millones de filas. Cargarlo con `pd.read_csv` sin más puede consumir varios
  GB de RAM. Conviene usar `usecols` y tipos compactos:

  ```python
  ratings = pd.read_csv(
      'ruta/ratings.csv',
      usecols=['userId', 'movieId', 'rating'],
      dtype={'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'},
  )   # ~380 MB en memoria
  ```

* Convierte `rating_datetime` a fecha **solo** en el subconjunto que lo necesite: parsear los 32 M de
  timestamps es la operación más costosa de todo el proyecto.
* Si hay que filtrar y agregar a la vez, lee por bloques (`chunksize=5_000_000`) y haz ambas cosas en
  la misma pasada en vez de leer el archivo dos veces.
* Ejecutar de principio a fin un notebook que carga `ratings` completo tarda entre 2 y 5 minutos.

**Texto y codificación**

* Abre y guarda los archivos en **UTF-8**. Hay títulos y tags con caracteres especiales (`WALL·E`,
  títulos en otros idiomas) que se corrompen con otras codificaciones. En Windows, la consola puede
  mostrarlos mal aunque los datos estén correctos.
* En `tags` hay casos de *mojibake* heredados del dataset original, documentados en `tags.ipynb`.
* Los títulos de MovieLens posponen el artículo (`Truman Show, The`), incluyen alias
  (`Men in Black (a.k.a. MIB)`) y títulos alternativos entre paréntesis. Además hay títulos
  repetidos: existen seis películas distintas llamadas `Venom`. Para localizar una película,
  empareja por **título normalizado + año**, nunca solo por título (ver `group_20_movies.ipynb`).

**Trabajo en equipo**

* Los notebooks se guardan **con sus salidas ejecutadas**, para que el trabajo sea revisable sin
  volver a correrlo todo.
* Antes de hacer `push`, ejecuta `git status` y confirma que no aparece ningún archivo de `data/`.
