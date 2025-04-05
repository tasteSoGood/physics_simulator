#------------------------------------------------
# name: animator.py
# author: taster
# date: 2025-03-26 15:58:50 星期三
# id: 8ff8deb1975d79c08f46de8ec13f09b7
# description: 动画基类
#------------------------------------------------
from abc import abstractmethod
from typing import Tuple
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Animator2D:
    """二维动画基类"""
    def __init__(self):
        pass

    def initialize_figure(self, xlim: tuple | list, ylim: tuple | list, figsize=None, title=None, grid=True):
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
            self.ax.set_title(title)
        self.ax.grid(grid)
        self.fig.tight_layout()

    @abstractmethod
    def update(self, frame) -> Tuple[Line2D]:
        """更新函数，需重载"""
        pass

    def play(self, frames=1000, interval=10, blit=True):
        """运行动画"""
        assert hasattr(self, 'fig'), "画布未初始化，请在 __init__ 中调用 self.initialize_figure 方法"
        self.ani = animation.FuncAnimation(self.fig, self.update, frames=frames, interval=interval, blit=blit)
        plt.show()

    def save_animation(self, filename, fps=30, dpi=100, writer="ffmpeg", extra_args=None, 
                      frames=None, interval=None, **kwargs):
        """
        将动画保存为视频文件
        
        参数:
            filename: 保存的文件名(包括扩展名，如 'animation.mp4')
            fps: 帧率(每秒帧数)
            dpi: 输出视频的分辨率
            writer: 指定视频写入器(如 'ffmpeg', 'imagemagick'等)
            extra_args: 传递给视频写入器的额外参数
            frames: 覆盖play()方法中设置的帧数
            interval: 覆盖play()方法中设置的间隔(毫秒)
            **kwargs: 其他传递给animation.FuncAnimation.save()的参数
            
        支持格式:
            .mp4, .gif, .mov等(取决于系统安装的视频编码器)
            
        注意:
            1. 需要先调用play()方法或手动创建self.ani
            2. 保存MP4需要安装ffmpeg
            3. 保存GIF需要安装imagemagick
        """
        if not hasattr(self, 'ani'):
            # 如果没有创建动画，先创建一个
            frames = frames if frames is not None else 500
            interval = interval if interval is not None else 10
            self.ani = animation.FuncAnimation(
                self.fig, 
                self.update, 
                frames=frames, 
                interval=interval, 
                blit=True
            )
        
        # 设置保存参数
        save_kwargs = {
            'fps': fps,
            'dpi': dpi,
            'writer': writer
        }
        if extra_args is not None:
            save_kwargs['extra_args'] = extra_args
        save_kwargs.update(kwargs)
        
        # 保存动画
        self.ani.save(filename, **save_kwargs)
        print(f"动画已保存为 {filename}")

