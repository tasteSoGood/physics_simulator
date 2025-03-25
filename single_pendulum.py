#------------------------------------------------
# name: single_pendulum.py
# author: taster
# date: 2025-03-25 22:17:42 星期二
# id: 08de7fa19730f9f757396ee2acdee663
# description: 单摆
#------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.widgets import Button
import matplotlib.animation as animation
import numpy as np
import datetime
import matplotlib.gridspec as gridspec

class SinglePendulum:
    """单摆系统"""
    def __init__(self, length=1.0, mass=1.0, theta=np.pi / 3, damping=False):
        # 全局参数设置
        self.g          = 9.8     # 重力加速度
        self.damping    = 0.998   # 阻尼
        self.is_damping = damping 
        self.length     = length  # 杆长
        self.mass       = mass    # 摆锤的质量
        self.theta      = theta   # 初始角度
        self.theta_dot  = 0.0     # 角速度
        self.dt         = 1e-2    # 时间步长

        self.initialize_figure() # 初始化matplotlib画布

        # 绘制摆锤、杆
        ball_position = self.ball_pos()
        self.ball = Circle(ball_position, radius=0.1, fill=True, color="blue")
        self.ax.add_patch(self.ball)
        self.pole, = self.ax.plot([0, ball_position[0]], [0, ball_position[1]], lw="2", c="blue")

    def ball_pos(self):
        """计算当前小球的笛卡尔坐标"""
        return (self.length * np.sin(self.theta), -self.length * np.cos(self.theta))

    def update(self, frame):
        """每一帧更新时调用的方法"""
        # 计算角加速度
        theta_double_dot = - (self.g / self.length) * np.sin(self.theta)
        # 欧拉法更新速度和角度
        self.theta_dot += theta_double_dot * self.dt
        self.theta += self.theta_dot * self.dt
        if self.is_damping:
            # 应用阻尼
            self.theta_dot *= self.damping
        ball_position = self.ball_pos()
        self.pole.set_data([0, ball_position[0]], [0, ball_position[1]])
        self.ball.set_center(ball_position)
        self.ax.add_patch(self.ball)
        return self.ball, self.pole

    def initialize_figure(self):
        """创建图形和坐标轴"""
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-1.5, 1.5) # 设置x轴范围
        self.ax.set_ylim(-1.5, 1.5)     # 设置y轴范围
        self.ax.set_aspect('equal', adjustable='box')  # 确保比例为1:1
        self.ax.set_title("Single Pendulum")
        self.ax.grid(True)

    def play(self, frames=1000, interval=3):
        """运行动画"""
        ani = animation.FuncAnimation(self.fig, self.update, frames=frames, interval=interval, blit=True)
        plt.show()

if __name__ == "__main__":
    # 使用示例
    simulator = SinglePendulum(length=1.0)
    simulator.play()

