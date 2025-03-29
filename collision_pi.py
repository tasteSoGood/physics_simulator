#------------------------------------------------
# name: collision_pi.py
# author: taster
# date: 2025-03-16 16:26:31 星期日
# id: 073097cc12359febcdc6f9146abd41c7
# description: 用刚体块的一维完全弹性碰撞计算圆周率
#------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.animation as animation
from animator import Animator2D

class CollisionSimulator(Animator2D):
    def __init__(self, m1=1.0, m2=1.0, w=0.5, dt=0.1, x1=0.0, v1=0.0, x2=5.0, v2=-2.0):
        super(CollisionSimulator, self).__init__()
        # 参数初始化
        self.m1 = m1
        self.m2 = m2
        self.w = w  # 方块宽度
        self.dt = dt  # 时间步长
        self.x1 = x1  # 方块A的位置
        self.v1 = v1  # 方块A的速度
        self.x2 = x2  # 方块B的位置
        self.v2 = v2  # 方块B的速度
        self.collision_count = 0  # 碰撞计数
        
        # 创建图形和坐标轴
        self.initialize_figure([-1, 6], [-1, 1], title="Collision", figsize=(8, 3))
        
        # 初始化方块
        self.rect1 = Rectangle((self.x1 - self.w/2, -0.25), self.w, 0.5, fill=True, color='blue')
        self.rect2 = Rectangle((self.x2 - self.w/2, -0.25), self.w, 0.5, fill=True, color='red')
        self.wall = Rectangle((-1, -1), 1, 2, fill=True, color="#aaaaaa")
        self.ax.add_patch(self.rect1)
        self.ax.add_patch(self.rect2)
        self.ax.add_patch(self.wall)

        # 添加文本框用于显示碰撞次数
        self.text_box = self.ax.text(0.02, 0.95, f'Collisions: {self.collision_count}', 
                                     transform=self.ax.transAxes, fontsize=12, verticalalignment='top')
        
    def update_positions(self):
        """更新位置"""
        self.x1 += self.v1 * self.dt
        self.x2 += self.v2 * self.dt
        
        self.rect1.set_x(self.x1 - self.w/2)
        self.rect2.set_x(self.x2 - self.w/2)
    
    def handle_wall_collision(self):
        """处理与墙的碰撞"""
        if self.x1 <= 0 + self.w / 2:
            self.v1 = -self.v1
            self.x1 = 0 + self.w / 2  # 确保方块不会穿过墙
            self.collision_count += 1
            
        if self.x2 <= 0 + self.w / 2:
            self.v2 = -self.v2
            self.x2 = 0 + self.w / 2  # 确保方块不会穿过墙
            self.collision_count += 1
    
    def handle_block_collision(self):
        """处理方块间的碰撞"""
        if abs(self.x1 - self.x2) < self.w:  # 如果发生碰撞
            u1, u2 = self.v1, self.v2
            self.v1 = ((self.m1 - self.m2)*u1 + 2*self.m2*u2) / (self.m1 + self.m2)
            self.v2 = ((self.m2 - self.m1)*u2 + 2*self.m1*u1) / (self.m1 + self.m2)
            self.collision_count += 1  # 增加碰撞计数
    
    def update(self, frame):
        """每一帧更新时调用的方法"""
        # 更新位置
        self.update_positions()
        
        # 处理与墙的碰撞
        self.handle_wall_collision()
        
        # 处理方块间的碰撞
        self.handle_block_collision()

        # 更新文本框中的碰撞次数
        self.text_box.set_text(f'Collisions: {self.collision_count}')
        
        return self.rect1, self.rect2, self.text_box

if __name__ == "__main__":
    # 使用示例
    simulator = CollisionSimulator(x1=2, x2=5, m1=1.0, m2=100.0, dt=1e-3)
    simulator.play(interval=1)
    # simulator.save_animation("./example/collision_pi.mp4", fps=30, interval=1, frames=500, dpi=200)

