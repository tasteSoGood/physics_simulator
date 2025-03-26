#------------------------------------------------
# name: collision_2d.py
# author: taster
# date: 2025-03-17 20:03:57 星期一
# id: 6703ceb11f6e2c00964cfbfb7e1c259d
# description: 2维完全弹性碰撞
#------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.widgets import Button
import matplotlib.animation as animation
import numpy as np
import datetime
import matplotlib.gridspec as gridspec
from utils import random_color, weighted_color
from animator import Animator2D


class CollisionSimulator2D(Animator2D):
    def __init__(self, xlim=[0, 1], ylim=[0, 1], N=2):
        super(CollisionSimulator2D, self).__init__()
        # 全局参数设置
        self.xmin, self.xmax = xlim  # 边界
        self.ymin, self.ymax = ylim  # 边界
        self.g               = 98    # 重力加速度
        self.damping         = 0.995 # 阻尼
        self.N               = N     # 物体数量
        self.radius          = 0.05  # 小球的直径
        self.dt              = 1e-3  # 时间步长

        self.initialize_parameters() # 随机生成位置、质量、速度
        self.initialize_figure(
            xlim=xlim, ylim=ylim, title="Collision 2D"
        )     # 初始化matplotlib画布
        self.initialize_balls()      # 初始化小球位置

        # 添加重置按钮
        ax_reset = plt.axes([0.465, 0.01, 0.1, 0.04])  # 按钮位置
        self.reset_button = Button(ax_reset, 'Reset')
        self.reset_button.on_clicked(self.reset)

        # 添加鼠标事件绑定
        self.dragging = False
        self.selected_ball = None
        self.fig.canvas.mpl_connect("button_press_event", self.on_press)
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)
        self.fig.canvas.mpl_connect("button_release_event", self.on_release)

        # 添加文本框用于显示动量和
        self.momentum = self.cal_momentum()
        self.text_box = self.ax.text(
            0.02, 0.95, f'Momentum: {np.round(self.momentum, 2)}', 
            transform=self.ax.transAxes, fontsize=8, verticalalignment='top',
        )

        # # 记录动能
        # self.energy = [(0.5 * self.mass[:, np.newaxis] * self.vol ** 2).sum()]
        # self.energy_line, = self.curve_ax.plot(np.arange(len(self.energy)), self.energy)

    def update(self, frame):
        """每一帧更新时调用的方法"""
        if self.selected_ball is not None:
            # 如果存在被选择的球，那么在更新状态前需要保存它的原状态
            selected_pos = self.pos[self.selected_ball].copy()
            selected_vol = self.vol[self.selected_ball].copy()
        self.handle_wall_collision()  # 处理与墙的碰撞
        self.handle_block_collision() # 处理小球间的碰撞
        self.handle_gravity()         # 加入重力
        # self.handle_damping()         # 加入阻尼
        self.update_positions()       # 更新位置
        if self.selected_ball is not None:
            self.pos[self.selected_ball] = selected_pos
            self.vol[self.selected_ball] = selected_vol
        for i in range(self.N):
            self.balls[i].set_center(self.pos[i])

        # 更新动量和
        self.momentum = self.cal_momentum()
        self.text_box.set_text(f"Momentum: {np.round(self.momentum, 2)}")
        # self.energy.append((0.5 * self.mass[:, np.newaxis] * self.vol ** 2).sum())
        # self.energy_line.set_data(np.arange(len(self.energy)), self.energy)
        # self.curve_ax.set_xlim(0, len(self.energy))
        # self.curve_ax.set_ylim(np.min(self.energy), np.max(self.energy))

        # return (*self.balls, self.text_box, self.energy_line)
        return (*self.balls, self.text_box)

    def gen_non_contact_balls(self):
        """生成无接触的球，废弃"""
        ball_list = []
        for i in range(self.N):
            tmp_ball = np.array([0., 0.])
            for _ in range(100): # 最多尝试生成的次数
                tmp_ball = np.array([
                    np.random.uniform(self.xmin + self.radius, self.xmax - self.radius),
                    np.random.uniform(self.ymin + self.radius, self.ymax - self.radius),
                ])
                flag = True
                for ball in ball_list:
                    # 计算距离
                    if np.linalg.vector_norm(tmp_ball - ball) <= 2 * self.radius:
                        flag = False
                if flag:
                    break
            ball_list.append(tmp_ball)
        return np.stack(ball_list)

    """
    物理更新
    """
    def handle_wall_collision(self):
        """处理与墙的碰撞"""
        self.vol[(self.pos[:, 0] >= self.xmax - self.radius) | (self.pos[:, 0] <= self.xmin + self.radius), 0] *= -1
        self.vol[(self.pos[:, 1] >= self.ymax - self.radius) | (self.pos[:, 1] <= self.ymin + self.radius), 1] *= -1

    def handle_block_collision(self):
        """处理小球间的碰撞"""
        for i in range(self.N):
            # 逐一计算是否碰撞
            for j in range(i + 1, self.N):
                # 获取法向量
                if np.linalg.vector_norm(self.pos[i] - self.pos[j]) <= 2 * self.radius: # 发生了碰撞
                    # n_vec = self.pos[i] - self.pos[j]
                    # n_vec = n_vec / np.linalg.vector_norm(n_vec)
                    # u1, u2 = self.vol[i], self.vol[j]
                    # m1, m2 = self.mass[i], self.mass[j]
                    #
                    # # 方向
                    # u1_direction = u1 - 2 * np.dot(u1, n_vec) * n_vec
                    # u2_direction = u2 - 2 * np.dot(u2, n_vec) * n_vec
                    # self.vol[i] = u1_direction
                    # self.vol[j] = u2_direction

                    # 碰撞的切向速度分量不变，而碰撞的法向速度分量服从一维完全弹性碰撞的关系
                    m1, m2 = self.mass[i], self.mass[j]

                    n = self.pos[i] - self.pos[j]
                    n = n / np.linalg.vector_norm(n) # 单位法向量
                    t = np.array([-n[1], n[0]]) # 对应的单位切向量

                    vi, vj = self.vol[i], self.vol[j]
                    vin, vjn = np.dot(vi, n), np.dot(vj, n) # 法向分量
                    vit, vjt = np.dot(vi, t), np.dot(vj, t) # 切向分量

                    # 计算碰撞后的法向速度
                    vin_new = ((m1 - m2) * vin + 2 * m2 * vjn) / (m1 + m2)
                    vjn_new = ((m2 - m1) * vjn + 2 * m1 * vin) / (m1 + m2)
                    
                    self.vol[i] = vin_new * n + vit * t
                    self.vol[j] = vjn_new * n + vjt * t

    def handle_gravity(self):
        """引入重力"""
        self.vol[:, 1] -= self.mass * self.g * self.dt 

    def handle_damping(self):
        """引入阻尼"""
        self.vol = self.damping * self.vol

    def update_positions(self):
        """更新位置"""
        self.pos += self.vol * self.dt
        self.solve_overlaps() # 重叠检查
        # 边界检查
        self.pos[:, 0] = np.clip(self.pos[:, 0], self.xmin + self.radius, self.xmax - self.radius)
        self.pos[:, 1] = np.clip(self.pos[:, 1], self.ymin + self.radius, self.ymax - self.radius)

    """
    重叠检查
    """
    def solve_overlaps(self, max_iter=10):
        """检查并解决小球重叠的问题"""
        for _ in range(max_iter):
            pairs = self.find_overlapping_pairs() # 找到重叠的小球组
            if len(pairs) == 0:
                break # 没有则退出
            for i, j in pairs:
                self.adjust_overlapping_pair(i, j)

    def find_overlapping_pairs(self):
        """找出所有重叠的小球对"""
        delta = self.pos[:, np.newaxis, :] - self.pos[np.newaxis, :, :] # 计算所有小球的坐标差矩阵
        dist = np.sqrt(np.sum(delta**2, axis=2))                        # 计算每对小球之间的距离平方
        np.fill_diagonal(dist, np.inf)                                  # 忽略对角线元素（自身比较）
        overlap_mask = dist < 2 * self.radius - 1e-5                    # 判断是否存在重叠
        return np.argwhere(overlap_mask)

    def adjust_overlapping_pair(self, i, j):
        """调整两个重叠小球的位置"""
        delta = self.pos[i] - self.pos[j] # 方向向量
        distance = np.linalg.norm(delta)
        if distance == 0: # 如果圆心重叠，随机确定一个方向向量
            delta = np.random.rand(2) - 0.5
            distance = 1e-5

        # 计算需要移动的距离（重叠量的一半）
        overlap = (2 * self.radius - distance) / 2
        direction = delta / distance

        # 根据质量分配移动比例
        total_mass = self.mass[i] + self.mass[j]
        self.pos[i] += direction * overlap * (self.mass[j] / total_mass)
        self.pos[j] -= direction * overlap * (self.mass[i] / total_mass)

    """
    初始化函数
    """
    def initialize_parameters(self):
        """初始化物理参数"""
        self.mass = np.random.uniform(1, 10, self.N) # 质量 (N)
        # self.pos = self.gen_non_contact_balls() # 位置 (N, 2)
        self.pos = np.column_stack([
            np.random.uniform(self.xmin + self.radius, self.xmax - self.radius, self.N),
            np.random.uniform(self.ymin + self.radius, self.ymax - self.radius, self.N),
        ])
        self.vol = np.column_stack([
            np.random.uniform(0.0, 5.0, self.N),
            np.random.uniform(0.0, 5.0, self.N),
        ]) # 速度 (N, 2)

    def initialize_balls(self):
        """初始化小球图形"""
        # 移除旧的小球（如果有）
        if hasattr(self, 'balls'):
            for ball in self.balls:
                ball.remove()
        # 生成新小球
        self.balls = [
            Circle((x, y), radius=self.radius, fill=True, color=weighted_color(mass, np.max(self.mass)))
            for x, y, mass in zip(self.pos[:, 0], self.pos[:, 1], self.mass)
        ]
        for ball in self.balls:
            self.ax.add_patch(ball)

    """
    交互相关函数
    """
    def reset(self, event):
        """重置按钮的回调函数"""
        self.initialize_parameters()
        self.initialize_balls()
        # self.energy = [(0.5 * self.mass[:, np.newaxis] * self.vol ** 2).sum()]

    def on_press(self, event):
        """鼠标按下时选择小球"""
        if event.inaxes != self.ax: # 未选中
            return
        for idx, ball in enumerate(self.balls):
            center = ball.center
            dist = np.hypot(event.xdata - center[0], event.ydata - center[1]) # 求斜边
            if dist <= self.radius:
                self.dragging = True
                self.selected_ball = idx
                self.vol[idx] = [0, 0] # 拖拽的时候将速度清零
                break

    def on_motion(self, event):
        """鼠标拖动的时候更新小球的位置"""
        if not self.dragging or event.inaxes != self.ax:
            return
        self.pos[self.selected_ball] = [
            np.clip(event.xdata, self.xmin + self.radius, self.xmax - self.radius),
            np.clip(event.ydata, self.ymin + self.radius, self.ymax - self.radius)
        ]
        self.balls[self.selected_ball].set_center(self.pos[self.selected_ball])
    
    def on_release(self, event):
        """鼠标释放时的操作"""
        self.dragging = False
        self.selected_ball = None

    """
    其他函数
    """
    def cal_momentum(self):
        """计算动量和"""
        return (self.vol * self.mass[:, np.newaxis]).sum(axis=0)

if __name__ == "__main__":
    # 使用示例
    # 这里的动量和不相等不是因为碰撞过程计算有误，而是因为小球会被墙反弹，反弹之后会改变其动量
    simulator = CollisionSimulator2D(N=5)
    simulator.play()

