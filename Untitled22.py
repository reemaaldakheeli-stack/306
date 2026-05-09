

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# عنوان الموقع
st.title("Distillation Column Simulation")
st.write("Interactive McCabe-Thiele Tool")

# سلايدرز جانبية
alpha = st.sidebar.slider("Volatility (α)", 1.1, 5.0, 2.5)
R = st.sidebar.slider("Reflux Ratio (R)", 0.5, 10.0, 2.0)

# الحسابات
x = np.linspace(0, 1, 100)
y = (alpha * x) / (1 + (alpha - 1) * x)

# الرسم البياني
fig, ax = plt.subplots()
ax.plot(x, y, label='Equilibrium Line')
ax.plot([0, 1], [0, 1], 'r--', label='45-degree Line')
ax.set_xlabel('x (Liquid)')
ax.set_ylabel('y (Vapor)')
ax.legend()
ax.grid(True)

# عرض الرسمة في الموقع
st.pyplot(fig)
st.success("Simulation is Running!")
