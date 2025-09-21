import matplotlib.pyplot as plt
import numpy as np

# Визначення функції та межі інтегрування
def f(x):
    return x ** 3 + 2 * x ** 2 + x + 1

a = 0  # Нижня межа
b = 2  # Верхня межа
N_points = 3000 # Кількість випадкових точок

xs_dense = np.linspace(a, b, 2000)
M = f(xs_dense).max()

# Створення діапазону значень для x
x = np.linspace(-0.5, 2.5, 400)
y = f(x)

# Створення графіка
fig, ax = plt.subplots()

# Малювання функції
ax.plot(x, y, 'r', linewidth=2)

# Заповнення області під кривою
ix = np.linspace(a, b)
iy = f(ix)
ax.fill_between(ix, iy, color='gray', alpha=0.3)

# --- випадкові точки у прямокутнику [a,b]×[0,M] ---
rng = np.random.default_rng(42)
xs = rng.uniform(a, b, N_points)
ys = rng.uniform(0, M, N_points)
below = ys <= f(xs)     # під графіком
above = ~below          # над графіком

# жовті під графіком, сині над графіком
ax.scatter(xs[below], ys[below], s=12, alpha=0.7, c='gold', edgecolors='none', label="Під графіком (жовті)")
ax.scatter(xs[above], ys[above], s=12, alpha=0.7, c='tab:blue', edgecolors='none', label="Над графіком (сині)")


# Налаштування графіка
ax.set_xlim([x[0], x[-1]])
ax.set_ylim([0, max(y) + 0.1])
ax.set_xlabel('x')
ax.set_ylabel('f(x)')

# Додавання меж інтегрування та назви графіка
ax.axvline(x=a, color='gray', linestyle='--')
ax.axvline(x=b, color='gray', linestyle='--')
ax.hlines(M, a, b, colors='gray', linestyles='--')
ax.set_title('Графік інтегрування f(x) = x^3 + 2x^2 + x + 1 від ' + str(a) + ' до ' + str(b))
plt.grid()
plt.show()

# --- точний інтеграл через SciPy quad ---
from scipy.integrate import quad
area_ref, err_ref = quad(lambda t: f(t), a, b)
ref_name = "SciPy quad"

# --- Монте-Карло ---
rng = np.random.default_rng(42)
N = 100_000
xs = rng.uniform(a, b, N)
ys = rng.uniform(0, M, N)
hits = (ys <= f(xs)).sum()

p_hat = hits / N
area_rect = (b - a) * M
area_mc = area_rect * p_hat

# оцінка стандартної похибки та 95% CI
se_mc = area_rect * np.sqrt(p_hat * (1 - p_hat) / N)
ci95_low, ci95_high = area_mc - 1.96 * se_mc, area_mc + 1.96 * se_mc

print(f"M (верх рамки)          : {M:.6f}")
print(f"{ref_name}              : {area_ref:.6f} (оцінка похибки: {err_ref})")
print(f"Monte Carlo (N={N})     : {area_mc:.6f}  (95% CI: [{ci95_low:.6f}, {ci95_high:.6f}])")
print(f"Абс. різниця MC vs ref  : {abs(area_mc - area_ref):.6f}")
print(f"Відн. різниця MC vs ref : {abs(area_mc - area_ref)/area_ref:.4%}")
