#------------------------------------------------
# name: moving_pendulum.py
# author: taster
# date: 2025-03-25 23:31:30 星期二
# id: cfee3223db36b028f6c80c2db14b2bd3
# description: 可移动悬挂点的单摆系统 - 朗道《力学》第一章第2道习题
#------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.animation as animation
import numpy as np

class MovingPendulum:
    def __init__(self, 
                 m1=2.0,   # 悬挂点质量
                 m2=1.0,   # 摆锤质量
                 L=1.0,    # 摆长
                 theta=np.pi/3,  # 初始角度
                 damping=0.995): # 阻尼系数
        # 系统参数
        self.g = 9.8
        self.m1, self.m2 = m1, m2
        self.L = L
        self.damping = damping
        self.dt = 1e-2

        # 初始状态
        self.x1 = 0.0         # 悬挂点水平位置
        self.x1_dot = 0.0     # 悬挂点速度
        self.theta = theta    # 摆角（垂直向下为0）
        self.theta_dot = 0.0  # 角速度

        # 初始化图形
        self.fig, self.ax = plt.subplots(figsize=(8,6))
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-3, 1)
        self.ax.set_aspect('equal')
        self.ax.grid(True)
        self.ax.set_title("Movable Pendulum System")

        # 创建图形元素
        self.anchor = Circle((0,0), 0.1, color='red', zorder=3)  # 悬挂点
        self.bob = Circle((0,0), 0.1, color='blue', zorder=3)    # 摆锤
        self.rod, = self.ax.plot([0,0], [0,0], lw=2, color='black')
        
        self.ax.add_patch(self.anchor)
        self.ax.add_patch(self.bob)

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

        # 更新图形位置
        bob_x = self.x1 + self.L*np.sin(self.theta)
        bob_y = -self.L*np.cos(self.theta)
        
        self.anchor.set_center((self.x1, 0))
        self.bob.set_center((bob_x, bob_y))
        self.rod.set_data([self.x1, bob_x], [0, bob_y])

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

    def play(self):
        """运行动画"""
        ani = animation.FuncAnimation(
            self.fig, self.update,
            frames=200, interval=20, blit=True
        )
        plt.show()

# 演示不同参数配置
if __name__ == "__main__":
    # 案例1：大质量悬挂点（近似固定悬挂点）
    # system = MovingPendulum(m1=100, m2=1, theta=np.pi/2*0.9)
    
    # 案例2：等质量混沌运动
    system = MovingPendulum(m1=1, m2=1, L=2.0, theta=100*np.pi/180, damping=1.0)
    
    # 案例3：小质量悬挂点剧烈运动
    # system = MovingPendulum(m1=0.5, m2=2, theta=np.pi/2*0.95)
    
    system.play()
