#------------------------------------------------
# name: rigid_rod.py
# author: taster
# date: 2025-04-05 01:29:18 星期六
# id: 225f6d4aa8c6988283173426a6e8516f
# description: 刚体杆的运动
#------------------------------------------------
import numpy as np
from animator import Animator2D
from matplotlib.patches import PathPatch
import matplotlib.path as path

class RigidRodSimulator(Animator2D):
    """均匀刚体杆自由下落碰撞模拟"""
    def __init__(self, restitution=0.8):
        """
        可通过修改 restitution 调整弹性（0为完全非弹性，1为完全弹性）。
        """
        super().__init__()
        # 物理参数
        self.L       = 1.0             # 杆长
        self.m       = 1.0             # 质量
        self.g       = 9.8             # 重力加速度
        self.e       = restitution     # 碰撞恢复系数
        self.floor_y = 0.0             # 地面高度
        
        # 初始状态 (质心坐标x,y; 速度vx,vy; 角度theta; 角速度omega)
        self.x_cm  = 0.0        # 质心x初始在原点
        self.y_cm  = self.L     # 初始高度为杆长（避免初始碰撞）
        self.vx_cm = 0.0
        self.vy_cm = 0.0
        self.theta = np.random.uniform(0, 2 * np.pi) # 初始角度
        self.omega = 0.0        # 初始无旋转
        
        # 物理常量
        self.I_cm = (1/12) * self.m * self.L**2  # 转动惯量
        
        # 初始化动画
        self.variable_added = False # 动画部件是否已被添加过
        self.initialize_figure(xlim=(-1.5, 1.5), ylim=(0, 3.0), title="Rigid Rod Simulator")
        self.plot_variable(0, 0, 0, 0)

    def plot_variable(self, x1, y1, x2, y2):
        """依据系统变量绘制动画部件"""
        rod_path = path.Path([(x1, y1), (x2, y2)], [path.Path.MOVETO, path.Path.LINETO])
        if self.variable_added:
            self.rod_line.set_path(rod_path)
        else:
            self.rod_line = PathPatch(rod_path, lw=2, edgecolor="blue", facecolor='none')
            self.ax.add_patch(self.rod_line)

    def _update_physics(self, dt):
        """物理状态更新（无碰撞时）"""
        self.vy_cm -= self.g * dt        # 重力加速度
        self.y_cm  += self.vy_cm * dt    # 更新质心y坐标
        self.x_cm  += self.vx_cm * dt    # 更新质心x坐标
        self.theta += self.omega * dt    # 更新角度
        
    def _check_collision(self):
        """检测与地面碰撞"""
        # 计算杆两端坐标
        half_L     = self.L / 2
        theta      = self.theta
        y1         = self.y_cm + half_L * np.sin(theta)
        y2         = self.y_cm - half_L * np.sin(theta)
        self.min_y = min(y1, y2)  # 保存为实例变量
        
        # 碰撞条件：杆的任一端接触地面
        if self.min_y <= self.floor_y:
            return True
        return False

    def _handle_collision(self):
        """处理碰撞后的速度和角速度（修正能量异常）"""
        half_L = self.L / 2
        theta = self.theta
        
        # 确定碰撞端点（下端或上端）
        if (self.y_cm - half_L * np.sin(theta)) <= self.floor_y:
            collision_point = -1  # 下端碰撞
        else:
            collision_point = 1   # 上端碰撞
        
        # 碰撞点相对于质心的位置矢量 (x方向为沿杆，y方向为垂直杆)
        r = collision_point * half_L
        r_x = r * np.cos(theta)   # 碰撞点在质心坐标系中的x分量
        r_y = r * np.sin(theta)   # 碰撞点在质心坐标系中的y分量
        
        # 碰撞点的线速度（法向和切向）
        v_tip_x = self.vx_cm - r_y * self.omega  # 切向速度（水平方向）
        v_tip_y = self.vy_cm + r_x * self.omega  # 法向速度（垂直方向）
        
        # 计算法向冲量（考虑转动惯量）
        numerator = -(1 + self.e) * v_tip_y
        denominator = 1/self.m + (r_x**2) / self.I_cm  # 有效惯性
        J = numerator / denominator
        
        # 更新质心速度和角速度
        self.vy_cm += J / self.m
        self.omega += (r_x * J) / self.I_cm
        
        # 修正位置防止穿透
        penetration = self.floor_y - self.min_y
        self.y_cm += penetration + 1e-3

    def update(self, frame):
        """动画更新函数"""
        dt = 0.01  # 时间步长
        
        # 更新物理状态
        self._update_physics(dt)
        
        # 检测并处理碰撞
        if self._check_collision():
            self._handle_collision()
        
        # 更新杆的图形
        half_L = self.L / 2
        x1 = self.x_cm + half_L * np.cos(self.theta)
        y1 = self.y_cm + half_L * np.sin(self.theta)
        x2 = self.x_cm - half_L * np.cos(self.theta)
        y2 = self.y_cm - half_L * np.sin(self.theta)
        self.plot_variable(x1, y1, x2, y2)
        
        return self.rod_line,

if __name__ == "__main__":
    sim = RigidRodSimulator(restitution=1.0)
    sim.play(frames=1000, interval=10)
    # sim.save_animation("rigid_rod_collision.mp4", fps=30)
