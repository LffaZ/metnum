# ΝΑΜΑ: Alifah Zuhrah U. S.
# NPM : 24083010033
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# interval
x = np.linspace(0, 10, 500)
# deret fungsi sinusoidal
f = np.sin(x) + 0.5*np.sin(2*x) + (1/3)*np.sin(3*x) + (1/4)*np.sin(4*x) + (1/5)*np.sin(5*x)

# Hitung integral dan diferensial dari fungsi 'f' untuk interval x
# ------- TURUNAN (Differensial) -------
f_prime = np.gradient(f, x)
# ------- Integral -------
dx = x[1] - x[0]
f_integral = np.cumsum((f[:-1] + f[1:]) / 2) * dx
f_integral = np.insert(f_integral, 0, 0)


# hitung secara terpisah bagian integral di atas dan di bawah y=0
def area_pos_neg(f_arr, x):
    f_pos = np.where(f_arr > 0, f_arr, 0)
    f_neg = np.where(f_arr < 0, f_arr, 0)
    area_pos = np.trapezoid(f_pos, x)
    area_neg = np.abs(np.trapezoid(f_neg, x))

    return f_pos, f_neg, area_pos, area_neg

# plot semua fungsi: f, f', F (atas dan bawah dengan area warna berbeda)
# --------- PLOTTING ---------
fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                    subplot_titles=("Fungsi f(x)", "Turunan dari f(x)", "Integral dari f(x)"))


data_list = [
    (f, "f(x)", 1),
    (f_prime, "f'(x)", 2),
    (f_integral, "∫f(x)dx", 3)
]

for y, label, row in data_list:
    y_pos, y_neg, area_pos, area_neg = area_pos_neg(y, x)

    fig.add_trace(go.Scatter(
        x=x, y=y, mode='lines', name=label,
        line=dict(color='#EF92D8', width=2),
        showlegend=(row == 1)
    ), row=row, col=1)

    fig.add_trace(go.Scatter(
        x=np.concatenate([x, x[::-1]]),
        y=np.concatenate([y_pos, np.zeros_like(x)]),
        fill='toself',
        fillcolor='rgba(168, 230, 163, 0.4)',
        line=dict(color='rgba(0,0,0,0)'),
        name=f"Luas area positif: {area_pos:.4f}",
        showlegend=(row == 1)
    ), row=row, col=1)

    fig.add_trace(go.Scatter(
        x=np.concatenate([x, x[::-1]]),
        y=np.concatenate([y_neg, np.zeros_like(x)]),
        fill='toself',
        fillcolor='rgba(245, 163, 163, 0.4)',
        line=dict(color='rgba(0,0,0,0)'),
        name=f"Luas area negatif: {area_neg:.4f}",
        showlegend=(row == 1)
    ), row=row, col=1)

    fig.add_trace(go.Scatter(
        x=[x[0], x[-1]], y=[0, 0],
        mode='lines',
        line=dict(color='black', dash='dash', width=1),
        hoverinfo='skip',
        showlegend=False
    ), row=row, col=1)

fig.update_layout(
    height=900,
    title_text="Plot f(x), Turunan, dan Integral dengan Area Positif/Negatif",
    showlegend=True,
    template='plotly_white',
    legend=dict(x=0.01, y=0.99),
)

fig.update_xaxes(title_text="x", row=3, col=1)
fig.update_yaxes(title_text="f(x)", row=1, col=1)
fig.update_yaxes(title_text="f'(x)", row=2, col=1)
fig.update_yaxes(title_text="∫f(x)dx", row=3, col=1)

fig.write_html("grafik.html")

# metode bebas, be creative!