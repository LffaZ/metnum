import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

istirahat= 6 # istirahat yang cukup
kuliah = 7.5
main = 6
organisasi = 5
res = 240

# Grid setup
xmin, xmax, ymin, ymax = 0, 24-istirahat, 0, 24-istirahat
x = np.linspace(xmin, xmax, res) # kuliah
y = np.linspace(ymin, ymax, res) # main
X, Y = np.meshgrid(x, y)

kuliah_pref = np.exp(-((x - kuliah)**2) / (10**2))
main_pref = np.exp(-((Y - main)**2) / (10**2))
# *Preferensi Organisasi* (faktor baru)
organisasi_pref = np.exp(-((X - organisasi)**2 + (Y - organisasi)**2) / (2 * 3**2))

# kalau total siklus main-kerja lebih dari 24 jam, merusak ritme sirkadian
total_waktu = X + Y
total_penalty = 0.2 * np.exp(total_waktu / 24.0)  # stronger, narrower penalty
#plt.plot(x, -total_penalty)

kebanyakan_main = 1 * np.exp(-((X - 2.0)**2 + (Y - 12.0)**2) / 0.8)   # kebanyakan main -> terlena
kebanyakan_lembur = 0.8 * np.exp(-((X - 18.0)**2 + (Y - 1.0)**2) / 0.6)  # kebanyakan lembur -> burnout

# naik-turun motivasi harian
NPM = 33
np.random.seed(NPM)
ripple = 0.4 * np.sin((0.3 * X)-1) * np.cos(1.0 * Y) -0.2
noise = np.random.normal(loc=0.0, scale=0.1, size=X.shape)
ripple += noise

plt.plot(x, np.exp(-((x -((45.0/7)))**2) / (10**2))) # kuliah
plt.plot(y, np.exp(-((y -4.0)**2) / (10**2))) # main
plt.plot(x, np.exp(-((x - organisasi)**2 + (y - organisasi)**2) / (2 * 3**2)))  # organisasi
plt.plot(x, -kebanyakan_main)
plt.plot(y, -kebanyakan_lembur )
plt.plot(x, 0.4 * np.sin((0.3 * x)-1) * np.cos(1.0 * y) -0.2)
plt.show()

# objective function
# quality of life
Z = 10.0 * (0.6 * kuliah_pref + 0.4 * main_pref)
Z = Z - kebanyakan_main - kebanyakan_lembur - total_penalty + ripple 
Z = Z + 0.3 * organisasi_pref

# clip tidak lebih dari 24 jam
Z -= 10.0 * np.maximum(total_waktu - 24.0, 0.0)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))  # 1 baris, 2 kolom
# === Grafik 1: Semua fenomena ===
Z_clip_all = np.clip(Z, -20, 20)
c1 = axes[0].pcolormesh(X, Y, Z_clip_all, cmap='jet_r', shading='auto')
contours1 = axes[0].contour(X, Y, Z_clip_all, levels=30, colors='black', linewidths=0.7)
fig.colorbar(c1, ax=axes[0])
axes[0].set_xlabel("kuliah (jam)")
axes[0].set_ylabel("main (jam)")
axes[0].set_title("Quality of Life (Semua Fenomena)")
# === Grafik 2: Fenomena 'sehat' saja ===
Z_clip_healthy = np.clip(Z, 0, 15)
c2 = axes[1].pcolormesh(X, Y, Z_clip_healthy, cmap='jet_r', shading='auto')
contours2 = axes[1].contour(X, Y, Z_clip_healthy, levels=30, colors='black', linewidths=0.7)
fig.colorbar(c2, ax=axes[1])
axes[1].set_xlabel("kuliah (jam)")
axes[1].set_ylabel("main (jam)")
axes[1].set_title("Quality of Life (Khusus Sehat)")

plt.tight_layout()
plt.show()

# *Titik Optimum*
max_value = -np.inf 
optimal_kuliah = 0
optimal_main = 0

for i in range(Z.shape[0]):  
    for j in range(Z.shape[1]):  
        if Z[i, j] > max_value:  
            max_value = Z[i, j]  
            optimal_kuliah = X[i, j]  
            optimal_main = Y[i, j]  

print(f"Titik optimum ditemukan pada: Kuliah = {optimal_kuliah:.2f} jam, Main = {optimal_main:.2f} jam")
print(f"Nilai kualitas hidup maksimum Z = {max_value:.2f}")

# --------- Pagi --------- 
# Kuliah: Aktivitas dimulai dengan 7,5 jam untuk kuliah, waktu yang cukup untuk belajar tanpa menyebabkan kelelahan berlebih. Saya pastikan waktu kuliah tidak melebihi 8 jam agar tetap produktif dan fokus.
# Istirahat: Tidur minimal 6 jam setiap malam sangat penting untuk memastikan tubuh dan pikiran siap untuk beraktivitas.
# --------- Siang --------- 
# Main: Setelah kuliah, saya luangkan 6 jam untuk kegiatan santai, seperti menonton, bermain game, atau bersosial media. Saya batasi waktu ini agar tidak mengganggu ritme harian dan menjaga keseimbangan antara pekerjaan dan relaksasi.
# Aktivitas Fisik: Selain itu, saya usahakan untuk tetap bergerak dengan olahraga ringan seperti berlajan-jalan sepulang kuliah untuk menjaga kebugaran.
# --------- Sore --------- 
# Organisasi: Saya alokasikan sekitar 5 jam untuk kegiatan organisasi. Aktivitas ini penting untuk pengembangan diri, namun saya batasi agar tidak mengganggu keseimbangan antara kuliah dan waktu pribadi.
# --------- Malam --------- 
# Istirahat: Setelah semua aktivitas, saya pastikan untuk tidur yang cukup agar tubuh dapat beristirahat dan mempersiapkan diri untuk hari berikutnya.

# Poin Penting
# Saya sadar bahwa keseimbangan antara kuliah, hiburan, organisasi, dan istirahat adalah kunci untuk menjaga kualitas hidup yang optimal. Meskipun produktivitas penting, istirahat yang cukup juga tidak kalah penting untuk menjaga kesehatan mental dan fisik.