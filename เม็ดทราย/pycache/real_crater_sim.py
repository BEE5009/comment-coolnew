import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap

# ===== ค่าจากการทดลองจริง =====
water_depth = 0.10        # m
crater_diameter = 0.06545 # m
t0 = 0.334                # s
g = 9.81                  # gravity

# สร้าง domain จริง (เมตร)
x = np.linspace(-0.1, 0.1, 500)
y = np.linspace(0, water_depth, 400)
X, Y = np.meshgrid(x, y)

fig, ax = plt.subplots(figsize=(6,8))
paused = False
time = 0

# colormap น้ำ + ทราย
cmap = ListedColormap(["#1f77b4", "#ffdc50"])

def update(frame):
    global time
    if not paused:
        time += 0.02

    ax.clear()

    # รัศมีหลุมจริง
    radius = crater_diameter / 2

    # เริ่มเกิดหลุมหลัง t0
    if time >= t0:
        depth_growth = 0.02 * (time - t0)  # การลึกลง (ปรับได้)
    else:
        depth_growth = 0

    # สร้างรูปทรงหลุมแบบ Gaussian
    crater = depth_growth * np.exp(-(X**2)/(radius**2))

    # พื้นผิวน้ำเดิม
    surface = water_depth - crater

    # กำหนด phase: 0 = น้ำ, 1 = ทราย
    phase = np.zeros_like(X)

    # ทรายอยู่ด้านบนกำลังตก
    sand_front = water_depth - g*(time**2)/50
    phase[Y > sand_front] = 1

    # แสดงผล
    ax.contourf(X, Y, phase, levels=[-0.1,0.5,1.1], cmap=cmap)

    # วาดเส้นผิวหลุม
    ax.plot(x, water_depth - depth_growth*np.exp(-(x**2)/(radius**2)), 'k')

    ax.set_xlim(-0.1,0.1)
    ax.set_ylim(0,water_depth)
    ax.set_xlabel("Width (m)")
    ax.set_ylabel("Depth (m)")
    ax.set_title(f"Sand Impact Simulation | Time = {time:.2f} s")

def on_key(event):
    global paused
    if event.key == ' ':
        paused = not paused

fig.canvas.mpl_connect('key_press_event', on_key)

ani = FuncAnimation(fig, update, frames=500, interval=30)

plt.show()
