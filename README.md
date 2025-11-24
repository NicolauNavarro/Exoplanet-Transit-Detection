````markdown
# Exoplanet Transit Detection

Este proyecto permite descargar, limpiar y analizar curvas de luz de estrellas de la misión **Kepler**, detectando exoplanetas mediante el método de tránsitos usando el **Box Least Squares (BLS)**.

## Características

- Descarga automática de curvas de luz PDC para estrellas seleccionadas.
- Limpieza de datos eliminando valores NaN y outliers.
- Normalización de las curvas de luz.
- Detección de periodos de tránsito mediante BLS.
- Comparación del periodo detectado con el periodo oficial del exoplaneta.
- Visualización de:
  - Curva de luz limpia.
  - Tránsitos detectados.
  - Periodograma BLS.
- Gestión de archivos:
  - CSV de datos crudos y limpios.
  - CSV de comparación de periodos.
  - Imágenes PNG de curvas y periodogramas.
  - Archivos nombrados automáticamente según la estrella.
- Control mediante la variable `reinstalar`:
  - `True`: fuerza la descarga y limpieza de nuevo.
  - `False`: usa archivos existentes si ya están disponibles.

## Requisitos

- Python 3.9+
- [Lightkurve](https://docs.lightkurve.org/)
- [Astropy](https://www.astropy.org/)
- [NumPy](https://numpy.org/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- Jupyter Notebook o entorno compatible (opcional para visualización Markdown)

Instalación rápida de dependencias:

```bash
pip install lightkurve astropy numpy pandas matplotlib
```
````

> Nota: Lightkurve puede mostrar advertencias sobre submódulos opcionales (como `tpfmodel`). No afectan la ejecución principal del proyecto.

## Uso

1. Configura la estrella que quieres analizar en `main.py`:

```python
estrella = "Kepler-7"
reinstalar = False  # True para forzar la descarga y limpieza
```

2. Ejecuta el script:

```bash
python main.py
```

3. Archivos generados:

- `../data/<estrella>_raw.csv` → Curva de luz cruda.
- `../data/<estrella>_clean.csv` → Curva de luz limpia.
- `../output/<estrella>_comparacion_periodo.csv` → Tabla de comparación de periodos.
- `../output/<estrella>_curva_transitos.png` → Curva con tránsitos detectados.
- `../output/<estrella>_periodograma_BLS.png` → Periodograma BLS.

4. Si estás usando Jupyter Notebook, las visualizaciones se mostrarán automáticamente usando Markdown y Matplotlib.

## Estructura de Carpetas

```
project-root/
│
├─ data/                  # CSV de curvas de luz crudas y limpias
├─ output/                # Imágenes y CSV de comparación
├─ notebooks/             # Notebooks opcionales
└─ main.py                # Script principal
```

## Cómo funciona

1. Descarga la curva de luz de la estrella seleccionada desde la misión Kepler.
2. Une todos los quarters en un solo LightCurve.
3. Limpia los datos (elimina NaNs, outliers y normaliza).
4. Calcula el **periodograma BLS** para detectar el periodo de tránsito.
5. Compara el periodo detectado con el periodo oficial del planeta.
6. Genera gráficos y archivos CSV con los resultados.

## Referencias

- [Lightkurve Documentation](https://docs.lightkurve.org/)
- [Kepler Mission Exoplanet Catalog](https://exoplanets.nasa.gov/)

## Autor

Nicolau Navarro — proyecto personal de análisis de exoplanetas con Python y Lightkurve.
