#import every function in utils.py and perlin.py
from sklearn import base
from utils import fill, setblock, visualize
import perlin
from perlin import *
import random
import math
import numpy as np

#import every function in utils.py and perlin.py
from utils import fill, setblock, visualize, lerp
import perlin
from perlin import *
import random
import math
import numpy as np

DEBUG = False

spline_table_continental = {
    (-1.0, -1.0),
    (1.0, 1.0)
}

spline_table_erosion = {
    (-1.0, -1.0),
    (1.0, 1.0)
}

spline_table_pandv = {
    (-1.0, 50.0),
    (0.0, 150.0),
    (0.1, 200.0),
    (1.0, 250.0)
}

def spline(stage: int, noise: float) -> float:
    if stage == 3:
        return noise
    
    if stage == 0:
        noise /= 34

    if DEBUG:
        print("noise in spline: ", noise, "stage: ", stage)
        
    if stage == 0:
        spline_table = spline_table_continental
    elif stage == 1:
        spline_table = spline_table_erosion
    else:
        spline_table = spline_table_pandv

    sorted_table = sorted(spline_table, key=lambda point: point[0])
    
    # 处理超出范围的情况
    if noise <= sorted_table[0][0]:
        return spline(stage + 1, sorted_table[0][1])
    if noise >= sorted_table[-1][0]:
        return spline(stage + 1, sorted_table[-1][1])
    
    # 找到噪声值所在的区间
    for i in range(len(sorted_table) - 1):
        x0, y0 = sorted_table[i]
        x1, y1 = sorted_table[i+1]
        
        if x0 <= noise <= x1:
            t = (noise - x0) / (x1 - x0)
            t = fade(t)
            last_noise = lerp(y0, y1, t)
            return spline(stage + 1, last_noise)
    
    return 0.0  # 默认返回值


print("Starting advanced terrain generation...")

print("fill {} -64 {} {} 256 {} air".format(0, 0, x_max, z_max), file=open("test.mcfunction",'w'))

# 高度图和噪声图
height_array = np.zeros((x_max, z_max))
continentalness_array = np.zeros((x_max, z_max))

continentalness_gen = GeneratePerlinNoiseArray(3, lattice_size=128, nmap=4)

# 地形生成主循环
print("Generating terrain...")
for x in range(0, x_max):
    if x % 32 == 0:
        print("x = {}".format(x))
    
    for z in range(0, z_max):
        continentalness_noise = get_perlin_octave(x, z, continentalness_gen)
        
        # 保存噪声值用于可视化
        if DEBUG:
            print("nosie1: ", continentalness_noise)

        continentalness_array[x][z] = continentalness_noise
        
        height = spline(0, continentalness_noise)
        if DEBUG:
            print("height: ", height)
        
        # 保存高度值
        height_array[x][z] = height
        int_height = int(height)

        ################################### in minecraft
        
        fill(x, -59, int_height - 1, z, "sand")

# 可视化结果
print("Visualizing results...")
visualize(height_array, x_max, z_max)
