#------------------------------------------------
# name: moving_pendulum.py
# author: taster
# date: 2025-03-25 23:31:30 星期二
# id: cfee3223db36b028f6c80c2db14b2bd3
# description: 可移动悬挂点的单摆系统 - 朗道《力学》第一章第2道习题
#------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, PathPatch
import matplotlib.animation as animation
from matplotlib.path import Path
import numpy as np
from animator import Animator2D

class MovingPendulum(Animator2D):
    def __init__(self, 
                 m1=2.0,   # 悬挂点质量
                 m2=1.0,   # 摆锤质量
                 L=1.0,    # 摆长
                 theta=np.pi/3,  # 初始角度
                 damping=0.995): # 阻尼系数
        super(MovingPendulum, self).__init__()
        # 系统参数
        self.g           = 9.8
        self.m1, self.m2 = m1, m2
        self.L           = L
        self.damping     = damping
        self.dt          = 1e-2

        # 系统变量
        self.x1             = 0.0   # 悬挂点水平位置
        self.x1_dot         = 0.0   # 悬挂点速度
        self.theta          = theta # 摆角（垂直向下为0）
        self.theta_dot      = 0.0   # 角速度
        self.variable_added = False # 动画部件是否已被添加过

        # 初始化图形
        self.initialize_figure([-5, 5], [-3, 1], figsize=(8, 6), title="Movable Pendulum System")
        self.plot_variable()

    def plot_variable(self):
        # 更新图形位置
        bob_x      = self.x1 + self.L*np.sin(self.theta)
        bob_y      = -self.L*np.cos(self.theta)
        anchor_pos = (self.x1, 0) # 悬挂点的位置
        bob_pos    = (bob_x, bob_y) # 摆锤的位置
        rod_path   = Path([anchor_pos, bob_pos], [Path.MOVETO, Path.LINETO]) # 摆杆的路径

        # 创建图形元素
        if not self.variable_added:
            self.anchor = Circle(anchor_pos, radius=0.1, color='red', zorder=3)      # 悬挂点
            self.bob = Circle(bob_pos, radius=0.1, color='blue', zorder=3)           # 摆锤
            self.rod = PathPatch(rod_path, lw=2, edgecolor="gray", facecolor='none') # 摆杆
            
            for patch in [self.anchor, self.bob, self.rod]:
                self.ax.add_patch(patch)
            self.variable_added = True
        else:
            self.anchor.set_center(anchor_pos)
            self.bob.set_center(bob_pos)
            self.rod.set_path(rod_path)

    def _calc_accelerations(self):
        """计算加速度核心算法"""
        theta = self.theta
        c, s = np.cos(theta), np.sin(theta)
        denominator = self.m1 + self.m2*s**2

        # 角加速度计算
        term1 = (self.m1 + self.m2)*self.g*s
        term2 = self.m2*self.L*self.theta_dot**2*s*c
        theta_double_dot = (-term1 - term2) / (self.L*denominator)

        # 悬挂点加速度
        x1_double_dot = (self.m2*s*(self.L*self.theta_dot**2 - self.g*c)) / denominator

        return x1_double_dot, theta_double_dot

    def update(self, frame):
        """动画更新函数"""
        # 计算加速度
        x1_dd, theta_dd = self._calc_accelerations()

        # 欧拉法更新
        self.x1_dot += x1_dd * self.dt
        self.x1 += self.x1_dot * self.dt
        
        self.theta_dot += theta_dd * self.dt
        self.theta += self.theta_dot * self.dt

        # 应用阻尼
        self.x1_dot *= self.damping
        self.theta_dot *= self.damping

        self.plot_variable()
        # if frame % 10 == 0:
        #     print(f"System Energy: {self._calc_energy():.3f} J")

        return self.rod, self.anchor, self.bob

    # 能量跟踪功能
    def _calc_energy(self):
        # 动能计算
        v_anchor = self.x1_dot
        v_bob_x = self.x1_dot + self.L*self.theta_dot*np.cos(self.theta)
        v_bob_y = self.L*self.theta_dot*np.sin(self.theta)
        K = 0.5*self.m1*v_anchor**2 + 0.5*self.m2*(v_bob_x**2 + v_bob_y**2)
        
        # 势能计算
        U = -self.m2*self.g*self.L*np.cos(self.theta)
        
        return K + U  # 总机械能


# 演示不同参数配置
if __name__ == "__main__":
    # 案例1：大质量悬挂点（近似固定悬挂点）
    # system = MovingPendulum(m1=100, m2=1, theta=np.pi/2*0.9)
    
    # 案例2：等质量混沌运动
    system = MovingPendulum(m1=1, m2=1, L=2.0, theta=100*np.pi/180, damping=1.0)
    
    # 案例3：小质量悬挂点剧烈运动
    # system = MovingPendulum(m1=0.5, m2=2, theta=np.pi/2*0.95)
    
    system.play(interval=5)
