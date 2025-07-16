#import every function in utils.py and perlin.py
from utils import fill, setblock, visualize
import perlin
from perlin import *
import random
import numpy as np

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

# Task1 version
p = perlin.PerlinNoise(random.seed(9823478635))
for x in range(0, x_max):
    if x % 32 == 0:
        print("x = {}".format(x))
    for z in range(0, z_max):
        noise = p.get_perlin(x, z)
        height_array[x][z] = noise
        height = int(noise)
        noise_array[x][z] = noise
        water_covered = False
        # print("noise", noise)
        
        
        fill(x, -10, height, z, "stone")
        fill(x, height+1, height+4, z, "dirt")
        
        # fill water until y=0
        if height + 5 <= 0:
            water_covered = True
            fill(x, height+5, 0, z, "water")
            
        if(not water_covered):
            setblock(x, height+5, z, "grass_block")
            top_array[x][z] = height + 5
        else:
            top_array[x][z] = 0

# plant_tree(top_array, x_max, z_max)
visualize(height_array, x_max, z_max)