import math
import numpy as np
from utils import fade, lerp
from defs import *

def generate_randvec2(nlattice: int) -> np.ndarray:
    randtable = np.random.randint(NRANDVEC, size = (nlattice, nlattice))
    return RANDVEC2_TABLE[randtable]

### Task1: Naive 2D Perlin
### Hint: Gradient vectors, the fade function, and linear interpolation
class PerlinNoise:
    seed: int
    lattice_size: int
    nmap: int
    nlattice: int
    randvec2: np.ndarray
    
    def __init__(self, seed: int, lattice_size: int = 128, nmap: int = 4):
        self.seed = seed
        self.lattice_size = lattice_size
        self.nmap = nmap
        self.nlattice = nmap + 1
        self.randvec2 = generate_randvec2(self.nlattice)
        

    def get_perlin(self, x: float, z: float) -> float:
        w = 0.0
        X = None
        Z = None
        for i in range(self.nlattice):
            cur = i * self.lattice_size
            if cur <= x:
                X = cur
            if cur <= z:
                Z = cur
        # print(X, Z)
        pos_rand_x, pos_rand_z = X // self.lattice_size, Z // self.lattice_size

        vec00 = self.randvec2[pos_rand_x, pos_rand_z]
        vec01 = self.randvec2[pos_rand_x, pos_rand_z + 1]
        vec10 = self.randvec2[pos_rand_x + 1, pos_rand_z]
        vec11 = self.randvec2[pos_rand_x + 1, pos_rand_z + 1]
        # print("vecs")
        # print(vec00, vec01, vec10, vec11)

        grad00 = vec00 @ np.array([x - X, z - Z])
        grad01 = vec01 @ np.array([x - X, z - Z - self.lattice_size])
        grad10 = vec10 @ np.array([x - X - self.lattice_size, z - Z])
        grad11 = vec11 @ np.array([x - X - self.lattice_size, z - Z - self.lattice_size])
        # print("grads")
        # print(grad00, grad01, grad10, grad11)

        u = float(x - X) / self.lattice_size
        v = float(z - Z) / self.lattice_size
        u = fade(u)
        v = fade(v)

        lerpx1 = lerp(grad00, grad10, u)
        lerpx2 = lerp(grad01, grad11, u)
        w = lerp(lerpx1, lerpx2, v)

        w = max(min(w, 311), -64)

        return w
        
        

### Task2-1: Octaveal 2D Perlin
### Hint: Use multiple perlin noise generators with different lattice sizes and nmap

def GeneratePerlinNoiseArray(octaves: int, lattice_size: int = 128, nmap: int = 4) -> list:
    ret = []
    
    ### Your code begins here
    for i in range(octaves):
        current_lattice_size = lattice_size // (2 ** i)
        # 计算当前倍频所需的nmap（确保覆盖整个区域）
        current_nmap = max(nmap, math.ceil(512 / current_lattice_size))
        # 创建Perlin噪声生成器并添加到列表
        pn = PerlinNoise(i, lattice_size=current_lattice_size, nmap=current_nmap)
        ret.append(pn)
    ### Your code ends here
    
    return ret

def get_perlin_octave(x: float, z: float, perlin_array: list) -> float:
    # Generate the 2D perlin noise with octaves
    noise = 0
    total_amplitude = 0
    amplitude = 1.0
    ### Your code begins here
    for pn in perlin_array:
        noise += pn.get_perlin(x, z) * amplitude
        total_amplitude += amplitude
        amplitude *= 0.5  # 每个倍频的振幅减半
    
    # 归一化噪声值
    if total_amplitude > 0:
        noise /= total_amplitude

    ### Your code ends here
    return noise