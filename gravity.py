#------------------------------------------------
# name: gravity.py
# author: taster
# date: 2025-03-29 14:57:10 星期六
# id: 7651efb8b1c5eb9ec43b5dd4492811b2
# description: 引力模拟
#------------------------------------------------
import numpy as np
from animator import Animator2D
from matplotlib.widgets import Button
from matplotlib.patches import Circle
import matplotlib.pyplot as plt


class GravitySimulator(Animator2D):
    """质量点的引力交互模拟"""
    
    def __init__(self, tracing=False, N=2, damping=0.995):
        """
        初始化模拟参数
        
        参数:
            m1, m2: 两个质量点的质量
            r1_init, r2_init: 初始位置 (x,y)
            v1_init, v2_init: 初始速度 (vx,vy)
            G: 万有引力常数
            xlim, ylim: 绘图范围
            figsize: 图形大小
            title: 图形标题
        """
        super().__init__()
        
        # 物理参数
        self.G        = 1.0       # 引力常数
        self.dt       = 0.05      # 时间步长
        self.xlim     = [-10, 10]
        self.ylim     = [-10, 10] # 空间范围
        self.N        = N         # 质点数量
        self.damping  = damping   # 阻尼
        self.is_trace = tracing   # 是否跟踪路径

        # 初始化图形
        self.initialize_figure(self.xlim, self.ylim, figsize=(8, 8), title="Gravity Simulator")
        self.random_init_parameter()
        
        # 添加重置按钮
        ax_reset = plt.axes([0.465, 0.01, 0.1, 0.04])  # 按钮位置
        self.reset_button = Button(ax_reset, 'Reset')
        self.reset_button.on_clicked(lambda event: self.random_init_parameter())
        
    def random_init_parameter(self):
        """随机初始化参数"""
        # 随机初始化
        self.mass = np.random.uniform(1.0, 5.0, self.N) # 质量
        self.pos = np.column_stack([np.random.uniform(*self.xlim, size=self.N), np.random.uniform(*self.ylim, size=self.N)]) # 位置
        self.vol = np.column_stack([np.random.uniform(-1., 1., size=self.N), np.random.uniform(-1., 1., size=self.N)]) # 速度

        # 创建绘图对象
        self.points = [ self.ax.plot(*self.pos[i], 'bo', markersize=10)[0] for i in range(self.N) ] # 质点
        if self.is_trace:
            self.pos_arr = [np.array([self.pos[i]], dtype=float) for i in range(self.N)] # 位置轨迹
            self.trajectories = [ self.ax.plot(*self.pos_arr[i], 'r-', alpha=0.3)[0] for i in range(self.N) ] # 轨迹

    def handle_wall_collision(self):
        """处理与墙的碰撞"""
        self.vol[(self.pos[:, 0] >= self.xlim[1]) | (self.pos[:, 0] <= self.xlim[0]), 0] *= -1
        self.vol[(self.pos[:, 1] >= self.ylim[1]) | (self.pos[:, 1] <= self.ylim[0]), 1] *= -1
        # 边界检查
        self.pos[:, 0] = np.clip(self.pos[:, 0], self.xlim[0], self.xlim[1])
        self.pos[:, 1] = np.clip(self.pos[:, 1], self.ylim[0], self.ylim[1])

    def calculate_force(self, i, j):
        """计算一对质点间的引力"""
        r_vec = self.pos[j] - self.pos[i]
        distance = np.linalg.norm(r_vec)
        if distance < 0.1:  # 防止距离过小导致力过大
            distance = 0.1
        force_magnitude = self.G * self.mass[i] * self.mass[j] / (distance ** 2)
        force_dir = r_vec / distance
        force = force_magnitude * force_dir
        return force

    def damping_high_speed(self):
        """对高速质点设置阻尼"""
        for i in range(self.N):
            if np.linalg.vector_norm(self.vol[i]) > 2.0:
                self.vol[i] *= self.damping
    
    def update_positions(self):
        """更新位置和速度"""
        force = np.zeros((self.N, 2)) # 计算合力
        for i in range(self.N):
            for j in range(self.N):
                if j == i:
                    continue
                force[i] += self.calculate_force(i, j)

        for i in range(self.N):
            self.vol[i] += (force[i] / self.mass[i]) * self.dt # 更新速度 (F = ma → a = F/m)
            self.pos[i] += self.vol[i] * self.dt               # 更新位置
        self.handle_wall_collision() # 处理与墙的碰撞
        self.damping_high_speed() # 限制过高的速度
        
        if self.is_trace:
            # 记录轨迹
            self.pos_arr = [ np.vstack([self.pos_arr[i], self.pos[i].reshape(1, 2)]) for i in range(self.N) ]
    
    def update(self, frame):
        """动画更新函数"""
        self.update_positions()
        
        # 更新点位置
        for i in range(self.N):
            self.points[i].set_data([self.pos[i, 0]], [self.pos[i, 1]])
            if self.is_trace:
                self.trajectories[i].set_data(self.pos_arr[i][:, 0], self.pos_arr[i][:, 1])
        
        if self.is_trace:
            return *self.points, *self.trajectories
        else:
            return self.points

# 使用示例
if __name__ == "__main__":
    # 创建模拟器实例
    simulator = GravitySimulator(N=3, damping=0.99)
    
    # 运行动画
    simulator.play(interval=5)
