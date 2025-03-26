#------------------------------------------------
# name: utils.py
# author: taster
# date: 2025-03-26 15:45:58 星期三
# id: 7d342f820c6a394bf7cdcb58a63bb5a1
# description: 辅助函数
#------------------------------------------------
import numpy as np

def random_color(seed=None):
    if seed:
        np.random.seed(seed)
    return "#%02x%02x%02x" % (
        np.random.randint(0, 256),
        np.random.randint(0, 256),
        np.random.randint(0, 256)
    )

def weighted_color(mass, max_mass):
    """根据质量来区别颜色"""
    return "#%02x%02x%02x" % (
        255 - int(255 * mass / max_mass),
        0, # 255 - int(255 * mass / max_mass),
        0, # 255 - int(255 * mass / max_mass),
    )

