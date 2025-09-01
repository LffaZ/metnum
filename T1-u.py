# Nama: Alifah Zuhrah Ulyya Suhada
# NPM: 24083010033

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skewnorm

# === Distribusi harga pasar (penjualan) ===
harga_jual = np.linspace(3000, 10000, 500)

# Parameter distribusi (skewed ke kanan)
skewness = 6
rata2_harga = 3500
sebaran = 1500

# Probabilitas penjualan per harga
penjualan_prob = skewnorm.pdf(harga_jual, a=skewness, loc=rata2_harga, scale=sebaran)
penjualan_prob *= 1000  # skala probabilitas

# Penambahan noise agar data lebih realistis
np.random.seed(33)  # Ganti dengan NPM jika diperlukan
penjualan_prob += np.random.normal(0, 0.005, size=harga_jual.shape)
penjualan_prob *= 1000

# === Data Produksi ===
jumlah_unit = np.linspace(0, 1000, len(harga_jual))
biaya_produksi = np.linspace(3000, 2000, len(jumlah_unit)) 
biaya_produksi += np.random.normal(0, 0.1, size=jumlah_unit.shape) * 100

# === Visualisasi ===
plt.figure(figsize=(8,5))

plt.plot(harga_jual, penjualan_prob, color="navy", label="Kurva Permintaan", linewidth=2) 
plt.plot(biaya_produksi, jumlah_unit, color="red", label="Biaya Produksi per Unit", linewidth=2)

plt.title("Analisis Titik Temu Permintaan dan Biaya Produksi - Toko Roti Maknyus")
plt.xlabel("Harga / Biaya per Unit (Rp)") 
plt.ylabel("Jumlah Unit")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

sort_indices = np.argsort(penjualan_prob)
sorted_penjualan = penjualan_prob[sort_indices]
sorted_harga = harga_jual[sort_indices]

# --- Interpolasi Harga Jual ---
harga_jual_per_unit = np.interp(jumlah_unit, sorted_penjualan, sorted_harga)
keuntungan = (harga_jual_per_unit - biaya_produksi) * jumlah_unit

# --- Titik Maksimum ---
indeks_max = np.argmax(keuntungan)
volume_optimal = jumlah_unit[indeks_max]
keuntungan_maksimum = keuntungan[indeks_max]

# --- Visualisasi Kurva Keuntungan ---
plt.figure(figsize=(9, 5))
plt.plot(jumlah_unit, keuntungan, color='green', label='Kurva Keuntungan')
plt.axvline(x=volume_optimal, color='r', linestyle='--', label=f'Produksi Optimal ({volume_optimal:.0f} unit)')
plt.title('Analisis Kurva Keuntungan')
plt.xlabel('Jumlah Unit Produksi')
plt.ylabel('Total Keuntungan (Rp)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

print("=== ANALISIS KEUNTUNGAN MAKSIMUM ===\n")
print(f"Volume Produksi Optimal : {volume_optimal:.0f} unit")
print(f"Keuntungan Maksimum : Rp {keuntungan_maksimum:,.0f}")