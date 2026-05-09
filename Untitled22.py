#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt

def simulate_distillation(alpha, xf, xd, xb, R):
    # 1. معادلة خط الاتزان
    x = np.linspace(0, 1, 100)
    y_eq = (alpha * x) / (1 + (alpha - 1) * x)

    # 2. معادلات خطوط التشغيل (Operating Lines)
    # خط التقطير (Rectifying Line): y = (R/(R+1))x + xd/(R+1)
    def rectifying_line(x_val):
        return (R / (R + 1)) * x_val + (xd / (R + 1))

    # 3. حساب عدد الصواني (Stepping)
    stages_x = [xd]
    stages_y = [xd]
    
    curr_x = xd
    curr_y = xd
    num_stages = 0
    
    while curr_x > xb and num_stages < 50: # حد أقصى 50 صينية لمنع التعليق
        # تحرك أفقياً لخط الاتزان (Vapor Composition)
        # x = y / (alpha - y(alpha-1))
        next_x = curr_y / (alpha - curr_y * (alpha - 1))
        
        stages_x.append(next_x)
        stages_y.append(curr_y)
        
        # تحرك عمودياً لخط التشغيل (Liquid Composition)
        if next_x > xf:
            next_y = rectifying_line(next_x)
        else:
            # خط الاستخلاص (Stripping Line) - تبسيط للتمثيل
            slope_s = (rectifying_line(xf) - xb) / (xf - xb)
            next_y = slope_s * (next_x - xb) + xb
            
        stages_x.append(next_x)
        stages_y.append(next_y)
        
        curr_x = next_x
        curr_y = next_y
        num_stages += 1

    # 4. الرسم البياني
    plt.figure(figsize=(10, 8))
    plt.plot(x, y_eq, 'b-', lw=2, label='Equilibrium Curve')
    plt.plot([0, 1], [0, 1], 'k--', alpha=0.5) # خط 45
    
    # رسم الصواني (الدرجات)
    plt.step(stages_x, stages_y, 'r-', where='post', label=f'Stages: {num_stages}')
    
    # نقاط البيانات
    plt.plot(xf, xf, 'go', label='Feed (xf)')
    plt.plot(xd, xd, 'ro', label='Distillate (xd)')
    plt.plot(xb, xb, 'bo', label='Bottoms (xb)')

    plt.title(f'McCabe-Thiele Simulation\nStages calculated: {num_stages}', fontsize=14)
    plt.xlabel('x (Liquid Mole Fraction)')
    plt.ylabel('y (Vapor Mole Fraction)')
    plt.legend()
    plt.grid(True)
    plt.show()

# تشغيل المحاكاة بقيم تجريبية
# alpha=2.5, xf=0.5, xd=0.9, xb=0.1, R=2.0
simulate_distillation(alpha=2.5, xf=0.5, xd=0.9, xb=0.1, R=1.5)


# In[2]:


import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, widgets

def plot_interactive_mccabe(alpha=2.5, R=2.0, xf=0.5, xd=0.9, xb=0.1):
    x = np.linspace(0, 1, 100)
    y_eq = (alpha * x) / (1 + (alpha - 1) * x)
    
    # معادلة خط التشغيل
    def rect_line(x_val):
        return (R / (R + 1)) * x_val + (xd / (R + 1))

    # حساب الصواني
    sx, sy = [xd], [xd]
    cx, cy = xd, xd
    steps = 0
    while cx > xb and steps < 40:
        # خط أفقـي للاتزان
        nx = cy / (alpha - cy * (alpha - 1))
        sx.extend([nx, nx])
        sy.extend([cy, rect_line(nx) if nx > xf else ((rect_line(xf)-xb)/(xf-xb))*(nx-xb)+xb])
        cx, cy = nx, sy[-1]
        steps += 1

    # الرسم
    plt.figure(figsize=(9, 7))
    plt.plot(x, y_eq, 'b', label='Equilibrium Curve')
    plt.plot([0,1], [0,1], 'k--', alpha=0.3)
    plt.step(sx, sy, 'r', where='pre', label=f'Stages: {steps}')
    plt.axvline(xf, color='g', ls=':', label='Feed Line')
    
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title(f"Live Simulation: R={R}, Alpha={alpha}")
    plt.show()

# إنشاء الواجهة التفاعلية
interact(plot_interactive_mccabe, 
         alpha=widgets.FloatSlider(value=2.5, min=1.1, max=5.0, step=0.1, description='Alpha (α)'),
         R=widgets.FloatSlider(value=1.5, min=0.5, max=10.0, step=0.1, description='Reflux (R)'),
         xf=(0.1, 0.9, 0.05), xd=(0.8, 0.99, 0.01), xb=(0.01, 0.2, 0.01))


# In[ ]:





# In[ ]:




