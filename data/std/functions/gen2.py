#import every function in utils.py and perlin.py
from utils import fill, setblock, visualize
import perlin
from perlin import *
import random
import math
import numpy as np


### Task2-2: Spline method
### Hint: Simulate "Continentalness"
### This is the spline table for plain biome

# valley
valley_spline_table = {
    (-1.0, 50.0),
    (0.0, 150),
    (0.1, 200),
    (1.0, 250)
}

# hills
hill_spline_table = {
    (-1.0, 60.0),
    (-0.5, 50.0),
    (0.0, 65.0),
    (0.5, 80.0),
    (1.0, 60.0)
}


def spline(noise: float, spline_table=valley_spline_table) -> float:
    noise /= 34

    # print("noise: ", noise)

    # 确保控制点按x值排序
    sorted_table = sorted(spline_table, key=lambda point: point[0])
    
    # 处理超出范围的情况
    if noise <= sorted_table[0][0]:
        return sorted_table[0][1]
    if noise >= sorted_table[-1][0]:
        return sorted_table[-1][1]
    
    # 找到噪声值所在的区间
    for i in range(len(sorted_table) - 1):
        x0, y0 = sorted_table[i]
        x1, y1 = sorted_table[i+1]
        
        if x0 <= noise <= x1:
            t = (noise - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    
    return 0.0  # 默认返回值

    
print("Starting terrain generation...")

random.seed(114514)

# clear all
print("fill {} -64 {} {} 256 {} air".format(0, 0, x_max, z_max), file=open("test.mcfunction",'w'))

height_array = np.zeros((x_max, z_max))
noise_array = np.zeros((x_max, z_max))

# This array keeps track of the top block's height (either grass or water)
top_array = np.zeros((x_max, z_max))

# Generate the perlin noise array, with max_octaves
max_octaves = 8
PerlinNoiseArray = GeneratePerlinNoiseArray(max_octaves, lattice_size=128, nmap=4)


# Task2-2 version
# for x in range(0, x_max):
#     if x % 32 == 0:
#         print("x = {}".format(x))
#     for z in range(0, z_max):
#         noise = get_perlin_octave(x, z, PerlinNoiseArray)

#         amp = 1
#         lv = -60
#         # valley
#         adjusted_noise = spline(noise, valley_spline_table)
#         # hills
#         # adjusted_noise = spline(noise, hill_spline_table)

#         height_array[x][z] = adjusted_noise * amp + lv
#         height = int(adjusted_noise * amp) + lv
#         noise_array[x][z] = adjusted_noise * amp + lv
#         water_covered = False
#         # print("noise", noise)
        
        
#         fill(x, -10, height, z, "stone")
#         fill(x, height+1, height+4, z, "dirt")
        
#         # # fill water until water_level
#         water_level = 0
#         if height + 5 <= water_level:
#             water_covered = True
#             fill(x, height+5, water_level, z, "water")
            
#         if(not water_covered):
#             setblock(x, height+5, z, "grass_block")
#             top_array[x][z] = height + 5
#         else:
#             top_array[x][z] = 0

# visualize(height_array, x_max, z_max)

# Task2-1 version
for x in range(0, x_max):
    if x % 32 == 0:
        print("x = {}".format(x))
    for z in range(0, z_max):
        noise = get_perlin_octave(x, z, PerlinNoiseArray)
        height_array[x][z] = noise + 20
        height = int(noise) + 20
        noise_array[x][z] = noise + 20
        water_covered = False
        # print("noise", noise)
        
        
        fill(x, -10, height, z, "stone")
        fill(x, height+1, height+4, z, "dirt")
        
        # # fill water until water_level
        water_level = 0
        if height + 5 <= water_level:
            water_covered = True
            fill(x, height+5, water_level, z, "water")
            
        if(not water_covered):
            setblock(x, height+5, z, "grass_block")
            top_array[x][z] = height + 5
        else:
            top_array[x][z] = 0

visualize(height_array, x_max, z_max)