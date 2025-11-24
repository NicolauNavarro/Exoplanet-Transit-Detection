# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lightkurve import search_lightcurve, LightCurve
from astropy.timeseries import BoxLeastSquares
from IPython.display import display, Markdown

# %%
# Configuración
estrella = "Kepler-15"
reinstalar = False  # si es False, no se volverá a descargar ni limpiar datos si existen

# Directorios de salida
data_dir = "../data"
output_dir = "../output"
os.makedirs(data_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# Nombres de archivos basados en la estrella
raw_csv = f"{data_dir}/{estrella}_raw.csv"
clean_csv = f"{data_dir}/{estrella}_clean.csv"
comparacion_csv = f"{output_dir}/{estrella}_comparacion_periodo.csv"
curva_transitos_img = f"{output_dir}/{estrella}_curva_transitos.png"
periodograma_img = f"{output_dir}/{estrella}_periodograma_BLS.png"

# %%
catalogo_oficial = {
    "Kepler-7": {
        "planeta": "Kepler-7b",
        "periodo_dias": 4.89,
        "KIC": "KIC 6922244",
        "url_info": "https://en.wikipedia.org/wiki/Kepler-7b?utm_source=chatgpt.com"
    },
    "Kepler-10": {
        "planeta": "Kepler-10b",
        "periodo_dias": 0.837,
        "KIC": "KIC 11904151",
        "url_info": "https://en.wikipedia.org/wiki/Kepler-10b"
    },
    "Kepler-15": {
        "planeta": "Kepler-15b",
        "periodo_dias": 4.94,
        "KIC": "KIC 11359879",
        "url_info": "https://science.nasa.gov/exoplanet-catalog/kepler-15-b/?utm_source=chatgpt.com"
    },
    "Kepler-22": {
        "planeta": "Kepler-22b",
        "periodo_dias": 289.9,
        "KIC": "KIC 10593626",
        "url_info": "https://science.nasa.gov/exoplanet-catalog/kepler-22-b"
    },
    "HD 209458": {
        "planeta": "HD 209458b",
        "periodo_dias": 3.5247,
        "KIC": "HIP 108859",
        "url_info": "https://en.wikipedia.org/wiki/HD_209458_b"
    }
}

planeta = catalogo_oficial[estrella]["planeta"]
kic_estrella = catalogo_oficial[estrella]["KIC"]
print(f"Planeta seleccionado: {planeta}")

# %%
# Descarga de datos si es necesario
if reinstalar or not os.path.exists(raw_csv):
    print("Descargando datos crudos...")
    resultado = search_lightcurve(kic_estrella, mission="Kepler", author="Kepler", cadence="long")
    if len(resultado) == 0:
        raise RuntimeError(f"No hay resultados para '{estrella}' en la misión indicada.")
    lcs = resultado.download_all()
    lc = lcs.stitch()
    # Guardar datos crudos como CSV
    pd.DataFrame({"time": lc.time.value, "flux": lc.flux.value}).to_csv(raw_csv, index=False)
else:
    print("Cargando datos crudos existentes...")
    df_lc = pd.read_csv(raw_csv)
    lc = LightCurve(time=df_lc["time"].values, flux=df_lc["flux"].values)

# %%
# Limpieza de datos
if reinstalar or not os.path.exists(clean_csv):
    print("Limpiando datos...")
    lc_limpia = (
        lc.remove_nans()
          .remove_outliers(sigma=6)
          .normalize(unit="ppm")
    )
    # Guardar CSV limpio
    pd.DataFrame({"time": lc_limpia.time.value, "flux": lc_limpia.flux.value}).to_csv(clean_csv, index=False)
else:
    print("Cargando datos limpios existentes...")
    df_clean = pd.read_csv(clean_csv)
    lc_limpia = LightCurve(time=df_clean["time"].values, flux=df_clean["flux"].values)

# %%
# Convertir a arrays para BLS
t = lc_limpia.time.value
y = lc_limpia.flux.value

# %%
# Periodograma BLS
model = BoxLeastSquares(t, y)
periods = np.linspace(0.3, 20, 5000)
durations = 0.1 * np.ones_like(periods)
bls_result = model.power(periods, durations)

periodo_detectado = bls_result.period[np.argmax(bls_result.power)]
periodo_oficial = catalogo_oficial[estrella]["periodo_dias"]
diferencia = abs(periodo_detectado - periodo_oficial)

# Guardar tabla de comparación
tabla = pd.DataFrame({
    "Planeta": [planeta],
    "Periodo detectado (días)": [periodo_detectado],
    "Periodo oficial (días)": [periodo_oficial],
    "Diferencia (días)": [diferencia]
})
tabla.to_csv(comparacion_csv, index=False)
print(tabla)

# %%
# Generar tránsitos
primer_dia = t[0]
ultimo_dia = t[-1]
transitos = primer_dia + periodo_detectado * np.arange(int((ultimo_dia - primer_dia)/periodo_detectado) + 1)

# %%
# Guardar figuras
plt.figure(figsize=(12,4))
plt.plot(t, y, 'k.', markersize=2)
for tr in transitos:
    plt.axvline(tr, color='red', linestyle='--', alpha=0.5)
plt.title(f"Curva con tránsitos — {estrella}")
plt.savefig(curva_transitos_img, dpi=300)
plt.close()

plt.figure(figsize=(12,4))
plt.plot(bls_result.period, bls_result.power)
plt.title(f"Periodograma BLS — {estrella}")
plt.savefig(periodograma_img, dpi=300)
plt.close()

# %%
# Mostrar resultados en Jupyter
display(Markdown("## Detección de exoplanetas por tránsito — Resumen"))
display(Markdown(f"### Estrella: {estrella} — Planeta: {planeta}"))
display(Markdown("### Comparación de periodos"))
display(tabla)

display(Markdown("### Curva de luz con tránsitos"))
plt.figure(figsize=(12,4))
plt.imshow(plt.imread(curva_transitos_img))
plt.axis('off')
plt.show()

display(Markdown("### Periodograma BLS"))
plt.figure(figsize=(12,4))
plt.imshow(plt.imread(periodograma_img))
plt.axis('off')
plt.show()
