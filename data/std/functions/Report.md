# Terrain Generation Report
蒋欣桐
## Task2 不同地形 spline 表
```python
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

```
valleys 是山和谷， hills 是丘陵（hills 的山顶有坑是有意为之）。  

valley
![alt text](Task2_spline_valley.png)

hills
![alt text](Task2_spline_hills.png)

## Task3 实现细节
我选择在 continentalness 上叠加 erosion 和 peeks & valleys。目标是产生类似黄土高原的地形。  

主要改动来自 spline 函数和 spline 表。最后用纯沙覆盖。

### spline 函数
```python
def spline(stage: int, noise: float) -> float:
    if stage == 3:
        return noise
    
    if stage == 0:
        noise /= 34  # 对初始噪声的归一化

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
```
在 spline 函数中加入了关于 stage 的条件分支，每个 stage 用相应的 spline 表。 stage0 对应从 continentalness 生成 [-1, 1] 区间的 erosion， stage1 对应从 erosion 生成 [-1, 1] 区间的 peaks_and_valleys， stage2 对应从 peaks_and_valleys 生成最终高度。


### spline 表
经过一些调参，最终生成黄土高原地形的三个 spline 表如下。

```python
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
```

示例效果
![alt text](Task3_terrain.png)