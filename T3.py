import numpy as np
import matplotlib.pyplot as plt

# Number of points
n = 200
NPM= 33

# Generate random x values between 0 and 4π
np.random.seed(NPM)
x = np.random.uniform(0, 4*np.pi, n)

# Original function
y_true = 4 * np.sin(2*x + 0.2)

# Add Gaussian noise
noise = np.random.normal(0, 0.4, n)  # mean=0, std=0.5
y_noisy = y_true + noise

# Plot
# plt.scatter(x, y_noisy, label="Noisy data", color="red", alpha=0.6)
# # plt.plot(np.sort(x), 4*np.sin(4*np.sort(x) + 0.2), label="True function", color="blue")
# plt.xlabel("x")
# plt.ylabel("y")
# plt.legend()
# plt.show()

# TUGAS: temukan kembali fungsi asli dengan interpolasi dari titik-titik data acak (y_noisy)
sorted_indices = np.argsort(x)
x_sorted = x[sorted_indices]
y_sorted = y_noisy[sorted_indices]

x_new = np.linspace(x_sorted[0], x_sorted[-1], 1000)
plt.figure(figsize=(12, 8))

plt.scatter(x, y_noisy, label="Data noisy", color="red", alpha=0.5)

plt.plot(x_new, 4 * np.sin(2*x_new + 0.2), label="Fungsi asli", color="green", linestyle="--")

for order in range(1, 6): 
    p = np.polyfit(x_sorted, y_sorted, order)
    y_poly = np.polyval(p, x_new)

    plt.plot(x_new, y_poly, label=f"Polinomial Ordo {order}")

plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.title("Interpolasi Polinomial dari Data Noisy (Orde 1 hingga 5)")
plt.show()