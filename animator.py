#------------------------------------------------
# name: animator.py
# author: taster
# date: 2025-03-26 15:58:50 星期三
# id: 8ff8deb1975d79c08f46de8ec13f09b7
# description: 动画基类
#------------------------------------------------
from abc import abstractmethod
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Animator2D:
    """二维动画基类"""
    def __init__(self):
        pass

    def initialize_figure(self, xlim: tuple | list, ylim: tuple | list, figsize=None, title=None):
        """初始化画布"""
        plt.rcParams["font.sans-serif"]=["Source Code Pro", "SimHei"]  # 正常显示中文
        plt.rcParams["axes.unicode_minus"] = False # 该语句解决图像中的负号乱码问题
        if not figsize:
            self.fig, self.ax = plt.subplots()
        else:
            self.fig, self.ax = plt.subplots(figsize=figsize)
        self.ax.set_xlim(*xlim)  # 设置x轴范围
        self.ax.set_ylim(*ylim)  # 设置y轴范围
        self.ax.set_aspect('equal', adjustable='box')  # 确保比例为1:1
        if title and isinstance(title, str):
            self.ax.set_title("Collision 2D")
        self.ax.grid(True)

    @abstractmethod
    def update(self, frame):
        """更新函数，需重载"""
        pass

    def play(self, frames=1000, interval=10, blit=True):
        """运行动画"""
        assert hasattr(self, 'fig'), "画布未初始化，请在 __init__ 中调用 self.initialize_figure 方法"
        ani = animation.FuncAnimation(self.fig, self.update, frames=frames, interval=interval, blit=blit)
        plt.show()

