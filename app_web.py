import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import psutil
import os
import time

# Configuration de la page
st.set_page_config(
    page_title="Calcul des Concentrations",
    page_icon="⚗️",
    layout="wide"
)

st.title("⚗️ Calcul des Concentrations par Étage")
st.write("Application de calcul des compositions avec profil chimie")

# Début chrono et RAM
start_time = time.perf_counter()
process = psutil.Process(os.getpid())
mem_start = process.memory_info().rss

# Barre latérale pour les paramètres
st.sidebar.header("Paramètres")
G_prime = st.sidebar.number_input("G_prime (flux de gaz)", value=50.0, min_value=0.1)
m = st.sidebar.number_input("m (coefficient)", value=25.0, min_value=0.1)
L = st.sidebar.number_input("L (longueur)", value=100.0, min_value=0.1)
x0 = st.sidebar.number_input("x0 (concentration initiale)", value=0.015, min_value=0.0)
N_etages = st.sidebar.slider("Nombre d'étages", min_value=1, max_value=20, value=3)

# =====================
# Calcul du facteur
# =====================
S = (G_prime * m) / L
st.info(f"**Facteur de désorption S = {S:.4f}**")

# =====================
# Calcul vectorisé
# =====================
etages = np.arange(1, N_etages+1)
x_sortant = x0 / (1 + S) ** etages
x_entrant = np.concatenate(([x0], x_sortant[:-1]))

# =====================
# Affichage du tableau
# =====================
st.subheader("Tableau des compositions")
df = pd.DataFrame({
    "Étage": etages,
    "x_entrant": x_entrant,
    "x_sortant": x_sortant
})

col1, col2 = st.columns(2)
with col1:
    st.dataframe(df, use_container_width=True)

with col2:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Télécharger CSV",
        data=csv,
        file_name="concentrations.csv",
        mime="text/csv"
    )

# =====================
# Graphique
# =====================
st.subheader("Évolution des concentrations")
fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(etages, x_entrant, 'bo-', label="x entrant", linewidth=2, markersize=8)
ax.plot(etages, x_sortant, 'ro-', label="x sortant", linewidth=2, markersize=8)

ax.set_title("Évolution des concentrations par étage", fontsize=14, fontweight='bold')
ax.set_xlabel("Nombre d'étages", fontsize=12)
ax.set_ylabel("Concentration x", fontsize=12)
ax.legend(fontsize=11)
ax.grid(True, linestyle="--", alpha=0.7)

st.pyplot(fig)

# =====================
# Statistiques
# =====================
end_time = time.perf_counter()
mem_end = process.memory_info().rss
mem_used = (mem_end - mem_start) / (1024 ** 2)

st.subheader("📊 Statistiques")
metrics_col1, metrics_col2 = st.columns(2)
with metrics_col1:
    st.metric("⏱️ Temps d'exécution", f"{end_time - start_time:.6f}s")
with metrics_col2:
    st.metric("💾 Mémoire utilisée", f"{mem_used:.6f} Mo")

# Statistiques supplémentaires
st.write("---")
col_stats1, col_stats2, col_stats3 = st.columns(3)
with col_stats1:
    st.metric("x_entrant (min)", f"{x_entrant.min():.6f}")
with col_stats2:
    st.metric("x_sortant (min)", f"{x_sortant.min():.6f}")
with col_stats3:
    st.metric("Écart moyen", f"{(x_entrant - x_sortant).mean():.6f}")
