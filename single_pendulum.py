#------------------------------------------------
# name: single_pendulum.py
# author: taster
# date: 2025-03-25 22:17:42 星期二
# id: 08de7fa19730f9f757396ee2acdee663
# description: 单摆
#------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, PathPatch
import matplotlib.path as path
from matplotlib.widgets import Button
import matplotlib.animation as animation
import numpy as np
import datetime
import matplotlib.gridspec as gridspec
from animator import Animator2D

"""
此系统中，广义坐标仅有theta与其一阶导，即L(theta, theta_dot)
即在动画更新过程中本质上只是这一个变量的变化，其后的所有绘制均基于此变化
"""

class SinglePendulum(Animator2D):
    """单摆系统"""
    def __init__(self, length=1.0, mass=1.0, theta=np.pi / 3, damping=False):
        super(SinglePendulum, self).__init__()
        # 全局参数设置
        self.g          = 9.8     # 重力加速度
        self.damping    = 0.998   # 阻尼
        self.is_damping = damping 
        self.length     = length  # 杆长
        self.mass       = mass    # 摆锤的质量
        self.dt         = 1e-2    # 时间步长

        # 变量
        self.theta          = theta # 初始角度
        self.theta_dot      = 0.0   # 角速度
        self.variable_added = False # 动画部件是否已被添加过

        self.initialize_figure([-1.5, 1.5], [-1.5, 1.5], title="Single Pendulum", figsize=(6, 6)) # 初始化matplotlib画布
        self.plot_variable()

    def plot_variable(self):
        """依据系统变量绘制动画部件"""
        # 绘制摆锤、杆
        ball_pos = (self.length * np.sin(self.theta), -self.length * np.cos(self.theta))
        # self.pole, = self.ax.plot([0, ball_position[0]], [0, ball_position[1]], lw="2", c="blue")
        # 创建杆的PathPatch
        pole_vertices = [(0, 0), ball_pos]
        pole_codes = [path.Path.MOVETO, path.Path.LINETO]
        pole_path = path.Path(pole_vertices, pole_codes)

        if not self.variable_added: # 动画部件的初始添加
            self.ball = Circle(ball_pos, radius=0.1, fill=True, color="blue")
            self.pole = PathPatch(pole_path, lw=2, edgecolor="gray", facecolor='none')
            self.ax.add_patch(self.pole)
            self.ax.add_patch(self.ball)
            self.variable_added = True
        else:
            self.pole.set_path(pole_path)
            self.ball.set_center(ball_pos)

    def update(self, frame):
        """每一帧更新时调用的方法"""
        # 更新系统变量
        theta_double_dot = - (self.g / self.length) * np.sin(self.theta) # 计算角加速度
        # 欧拉法更新速度和角度
        self.theta_dot += theta_double_dot * self.dt
        self.theta += self.theta_dot * self.dt
        if self.is_damping:
            self.theta_dot *= self.damping # 应用阻尼

        self.plot_variable()
        return self.ball, self.pole


if __name__ == "__main__":
    # 使用示例
    simulator = SinglePendulum(length=1.0)
    simulator.play(interval=3)
    # simulator.save_animation("./example/single_pendulum.mp4", fps=60, interval=1, frames=1000, dpi=200)

