#------------------------------------------------
# name: double_pendulum.py
# author: taster
# date: 2025-03-25 23:04:40 星期二
# id: 93480b8ca54a77531cac7d95141ac23a
# description: 双摆系统
#------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, PathPatch
from matplotlib.widgets import Button
import matplotlib.animation as animation
import matplotlib.path as path
import numpy as np
from animator import Animator2D


class DoublePendulum(Animator2D):
    """双摆系统"""
    def __init__(self, 
                 L1=1.0, L2=1.0, 
                 m1=1.0, m2=1.0,
                 theta1=np.pi/2, theta2=np.pi/2,
                 damping=0.998):
        super(DoublePendulum, self).__init__()
        # 物理参数
        self.g = 9.8               # 重力加速度
        self.L1, self.L2 = L1, L2  # 摆杆长度
        self.m1, self.m2 = m1, m2  # 摆锤质量
        self.damping = damping     # 阻尼系数
        self.dt = 1e-2             # 时间步长

        # 系统变量
        self.theta1, self.theta2         = theta1, theta2  # 初始角度
        self.theta1_dot, self.theta2_dot = 0.0, 0.0        # 角速度
        self.variable_added = False # 动画部件是否已被添加过

        self.initialize_figure([-2.5, 2.5], [-2.5, 2.5], figsize=(8, 8), title="Double Pendulum Chaos Demo")  # 初始化画布
        self.plot_variable()

    def plot_variable(self):
        """依据系统变量绘制动画部件"""
        # 创建图形元素
        # 更新图形
        pos1, pos2 = self.get_positions()

        pole1 = path.Path([(0, 0), pos1], [path.Path.MOVETO, path.Path.LINETO])
        pole2 = path.Path([pos1, pos2], [path.Path.MOVETO, path.Path.LINETO])
        if not self.variable_added:
            self.ball1 = Circle(pos1, radius=0.08, color="red", zorder=3)
            self.ball2 = Circle(pos2, radius=0.08, color="blue", zorder=3)
            self.rod1 = PathPatch(pole1, lw=2, edgecolor="gray", facecolor='none')
            self.rod2 = PathPatch(pole2, lw=2, edgecolor="gray", facecolor='none')
            for patch in [self.ball1, self.ball2, self.rod1, self.rod2]:
                self.ax.add_patch(patch)
            self.variable_added = True
        else:
            self.rod1.set_path(pole1)
            self.rod2.set_path(pole2)
            self.ball1.set_center(pos1)
            self.ball2.set_center(pos2)

    def get_positions(self):
        """计算两个摆锤的坐标"""
        x1 = self.L1 * np.sin(self.theta1)
        y1 = -self.L1 * np.cos(self.theta1)
        x2 = x1 + self.L2 * np.sin(self.theta2)
        y2 = y1 - self.L2 * np.cos(self.theta2)
        return (x1, y1), (x2, y2)

    def update(self, frame):
        """更新动画帧"""
        # 更新系统变量
        delta_theta = self.theta1 - self.theta2  # 修正角度差方向

        # 公共分母计算
        denom = 2 * self.m1 + self.m2 - self.m2 * np.cos(2 * delta_theta)
        
        # 第一个摆的角加速度
        theta1_double_dot = (
            -self.g * (2 * self.m1 + self.m2) * np.sin(self.theta1)
            - self.m2 * self.g * np.sin(self.theta1 - 2 * self.theta2)
            - 2 * np.sin(delta_theta) * self.m2 * (
                self.theta2_dot**2 * self.L2 
                + self.theta1_dot**2 * self.L1 * np.cos(delta_theta)
            )
        ) / (self.L1 * denom)

        # 第二个摆的角加速度
        theta2_double_dot = (
            2 * np.sin(delta_theta) * (
                self.theta1_dot**2 * self.L1 * (self.m1 + self.m2)
                + self.g * (self.m1 + self.m2) * np.cos(self.theta1)
                + self.theta2_dot**2 * self.L2 * self.m2 * np.cos(delta_theta)
            )
        ) / (self.L2 * denom)

        # 欧拉法更新角速度
        self.theta1_dot += theta1_double_dot * self.dt
        self.theta2_dot += theta2_double_dot * self.dt
        
        # 更新角度（注意阻尼）
        self.theta1 += self.theta1_dot * self.dt
        self.theta2 += self.theta2_dot * self.dt
        self.theta1_dot *= self.damping
        self.theta2_dot *= self.damping

        # 更新图形
        self.plot_variable()
        return self.rod1, self.rod2, self.ball1, self.ball2

if __name__ == "__main__":
    # 示例：创建初始角度为 170 度的混沌双摆
    pendulum = DoublePendulum(
        L1=1.0, L2=1.0,
        theta1=170*np.pi/180,  # 转换为弧度
        theta2=150*np.pi/180,
        damping=1.0,
    )
    pendulum.play(interval=3)
    # pendulum.save_animation("./example/double_pendulum.mp4", fps=60, interval=1, frames=1000, dpi=200)
