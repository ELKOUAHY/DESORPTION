import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import psutil
import os

# -----------------------
# Début du chrono
# -----------------------
start_time = time.perf_counter()

# -----------------------
# Début mesure RAM
# -----------------------
process = psutil.Process(os.getpid())
mem_start = process.memory_info().rss  # en bytes

# -----------------------
# Données
# -----------------------
G_prime = 50
m = 25
L = 100
x0 = 0.015
N_etages = 3

# -----------------------
# Calcul du facteur de désorption
# -----------------------
S = (G_prime * m) / L
print(f"Facteur de désorption S = {S:.4f}")

# -----------------------
# Calcul vectorisé des compositions
# -----------------------
etages = np.arange(1, N_etages+1)
x_sortant = x0 / (1 + S) ** etages
x_entrant = np.concatenate(([x0], x_sortant[:-1]))

# -----------------------
# Tableau avec pandas
# -----------------------
df = pd.DataFrame({
    "Etage": etages,
    "x_entrant": x_entrant,
    "x_sortant": x_sortant
})
print("\nTableau des étages :")
print(df.to_string(index=False))

# -----------------------
# Tracé avec thème chimie
# -----------------------
plt.style.use('seaborn-v0_8-darkgrid')
plt.figure(figsize=(8,5))

plt.plot(etages, x_entrant, 'bo-', label="x entrant")
plt.plot(etages, x_sortant, 'ro-', label="x sortant")

plt.title("Évolution des concentrations par étage (Thème Chimie)", fontsize=14, fontweight='bold')
plt.xlabel("Nombre d'étages")
plt.ylabel("Concentration x")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.7)
plt.show()

# -----------------------
# Fin chrono + RAM
# -----------------------
end_time = time.perf_counter()
mem_end = process.memory_info().rss

# Conversion en Mo
mem_used = (mem_end - mem_start) / (1024 ** 2)

print(f"\nTemps d'exécution total : {end_time - start_time:.6f} secondes")
print(f"Mémoire utilisée : {mem_used:.6f} Mo")
