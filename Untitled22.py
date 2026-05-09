

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Distillation Column Simulation")
st.write("Full Interactive McCabe-Thiele Tool")

# القائمة الجانبية للمدخلات
st.sidebar.header("Design Parameters")
alpha = st.sidebar.slider("Volatility (α)", 1.1, 5.0, 2.5)
R = st.sidebar.slider("Reflux Ratio (R)", 0.5, 10.0, 2.0)
xf = st.sidebar.slider("Feed (xf)", 0.1, 0.9, 0.5)
xd = st.sidebar.slider("Distillate (xd)", 0.8, 0.99, 0.9)
xb = st.sidebar.slider("Bottoms (xb)", 0.01, 0.2, 0.05)

# 1. حساب منحنى الاتزان
x = np.linspace(0, 1, 100)
y_eq = (alpha * x) / (1 + (alpha - 1) * x)

# 2. معادلة خط التشغيل (Rectifying Line)
def rect_line(val):
    return (R / (R + 1)) * val + (xd / (R + 1))

# 3. حساب الدرجات (Stages)
sx, sy = [xd], [xd]
cx, cy = xd, xd
steps = 0
while cx > xb and steps < 50:
    # تحرك أفقي لمنحنى الاتزان
    nx = cy / (alpha - cy * (alpha - 1))
    sx.extend([nx, nx])
    
    # تحرك عمودي لخطوط التشغيل
    if nx > xf:
        ny = rect_line(nx)
    else:
        # تبسيط لخط الاستخلاص (Stripping Line)
        slope_s = (rect_line(xf) - xb) / (xf - xb)
        ny = slope_s * (nx - xb) + xb
    
    sy.extend([cy, ny])
    cx, cy = nx, ny
    steps += 1

# 4. الرسم البياني
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x, y_eq, 'b', label='Equilibrium Curve')
ax.plot([0, 1], [0, 1], 'k--', alpha=0.5)
ax.step(sx, sy, 'r', where='pre', label=f'Stages: {steps}') # رسم الدرجات

# رسم نقاط التغذية والمنتجات
ax.plot(xf, xf, 'go', label='Feed (xf)')
ax.plot(xd, xd, 'ro', label='Distillate (xd)')
ax.plot(xb, xb, 'bo', label='Bottoms (xb)')

ax.set_xlabel('x (Liquid Phase)')
ax.set_ylabel('y (Vapor Phase)')
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)
st.success(f"Calculated Theoretical Stages: {steps}")
