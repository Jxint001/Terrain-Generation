# Mini Project: Terrain Generation

## Deadline: 2025.07.18 (Fri.)

> TA: MasterFHC

如果你想制作一款游戏，想要生成一些随机，却又平滑的变化，那么绕不开的一样东西就是柏林噪声，今天让我们来用柏林噪声来实现Minecraft中的地形生成！

## Intro

> Refer to Terrain-Generation.pptx on Canvas

> 如果你想对 Minecraft 的地形/群系生成机制做进一步了解，可以参照 [这个视频](https://www.youtube.com/watch?v=CSa5O6knuwI)

## Your Tasks

### Task1: Naive 2D Perlin

使用朴素的柏林噪声生成一片地图，chunk大小至少为16，至少生成4 * 4个chunk

![Naive Perlin](https://pic1.imgdb.cn/item/685f65ff58cb8da5c879bf62.png)

评分标准: 注意关注生成的地形在晶格边缘附近有没有突变（明显不自然的“人工”痕迹）
Hint: 如果怎么都调不出来，看看是不是没有用fade函数进行平滑

$$ fade(x) = 6 x^5 - 15 x^4 + 10 x^3 $$

### Task2: Octaveal 2D Perlin and spline method

由于一层柏林噪声看起来过于平滑，因此请使用课上讲的多层噪声叠加的方法生成一片更加“层峦叠嶂”的地形，此外，需要使用样条方法提供各种地形的预设，附在Report中

![Octave Perlin](https://pic1.imgdb.cn/item/685f65ae58cb8da5c879bd16.png)

评分标准：Octaveal部分关注实现效果是否比起Task1有明显提升，要求在报告中附上你的几个Spline表，并且要求提供几种特定地形的预设，如高原、山脉、平原等

### Task3: Decoration

> 2025.06.30 综合考虑到工作量与给分，修改了Task3的任务要求

对于Task3部分的评分，主要是希望大家对地形实现一些个性化的装饰。你可以选择实现一个大型的装饰，或者两个小型的装饰，以下给出一些例子：

**大型装饰：**

- Option1: 通过额外叠加"Erosion"和"Peaks and Valleys"层来实现更复杂的地形，比如"尖峰"，"峡谷"等，要求效果明显

- Option2: 通过3D Perlin，结合不同高度层来实现更复杂的地形变化，比如"浮空岛"，"地下洞穴"，"悬崖"等，要求仿照视频中的效果，有空腔和长条两种形态，彼此连接

**小型装饰：**

- Option3: 对于平原地形的生成，请使用"Plant Tree"函数，在平缓的地方种植树苗，长成树(你需要修改Tickspeed)

- Option4: 用噪声的方式或其他方式来装饰湖泊/河流，你可以使用 `minecraft:gravel`， `minecraft:sand` 以及一些植被来作为装饰物。如果你希望使用其他方块，在游戏中按下 `F3+H` 来展示“高级提示框”，在创造模式的背包中你可以看见各种方块的 `minecraft:xxx` 的名称

以上只是给出一些基本的例子，如果你感兴趣的话（不需要使用光影），你可以尝试新建一个正常的Minecraft世界，看看里面都有什么样的元素，当你实现完毕之后，你应该会天然地了解这是一个小型的装饰还是一个大型的装饰。

在这一部分，你也可以使用噪声来创造性地实现一些装饰，最终效果好看即可

## Tutorials

由于本次项目比较特殊，所以在此提供一些你可能用得到的教程!

### Installing Minecraft

为了 ~~节省我的工作量~~ 提供更好的可视化效果，本项目决定使用 Minecraft（我的世界）作为3D模拟器，在教程中，我将使用 [HMCL启动器](https://https://github.com/HMCL-dev/HMCL) 作为例子，如果你以前从未游玩过 Minecraft，或从未使用过 HMCL 的启动器的话， ~~请参照仓库中的 `Minecraft_Guide.md`~~ ，请参照小作业发布的录屏，也可以问问有经验的同学。



### Setting up your respository

找到你的 `.minecraft` 文件夹，如果你开启了版本隔离，那么进入 `/versions/1.20.1/saves/<World Name>/datapacks/` 下面，在这里建立你的仓库，等克隆完之后，你的目录应该长这个样子：

```
datapacks
|- Terrain-Generation
|  |- /data
|  |  |- /minecraft
|  |  |- /std
|  |
|  |- pack.mcmeta
|  |- README.md
```

其中，在 `/std/functions` 中，大致有如下文件：

- ##### `defs.py`: 
  定义了若干常量，比如生成范围的界限，随机梯度表
- ##### `utils.py`:
  一些工具函数，其中 `setblock()` 和 `fill()` 用于生成指令，和 Minecraft 的接口进行交互
- ##### `perlin.py`: 
  一个柏林噪声类，其中的若干函数需要你来实现（Task 1 + Task 2）
- ##### `gen.py`:
  主函数，生成最终的高度，并生成 Minecraft 指令写入文件，需要你在其中补充实现一下 `spline`（Task 2）
- ##### `load.mcfunction` 和 `tick.mcfunction`:
  没用，但别删
- ##### `test.mcfunction`:
  之前在 `gen.py` 中所生成的指令
  
  
### Testing before you start coding

在你开始做 **Task1** 之前，你可以先进入游戏，然后手动试试你的datapack有没有正确地载入：
1. 手动向test.mcfunction中写入一行指令，比如 `fill 0 -5 0 10 5 10 minecraft:dirt`
2. 进入你刚刚创建的世界，在命令行中输入
> /reload
3. 稍等几秒后，你应该会看到蓝色的"Datapack has been loaded!"，也就是load.mcfunction中写的内容，如果没有看到这行字，说明载入失败，要么你不小心动了其他文件，要么你test.mcfunction中存在不合法的指令，如果遇到这个问题且自己无法解决，请咨询TA
4. 在命令行中输入
> /function std:test
5. 由于这里只有一条指令，所以执行的应该很快，你应该立刻就能看到"已加载std::test中的1条指令"，并且在世界中生成了一坨泥土

如果以上步骤都没有问题，那么你就可以开始尝试实现你的Perlin Noise类了，你可以尝试分步地调试，每做一点就测试一下，我在 `utils.py` 中为你提供了一个可视化的函数，只需在python中测试，而不用打开Minecraft

### Generating the Terrain

当你实现完地形生成的部分后，你可以用如下方法在MC中生成一块区域
1. 在wsl中进入 /functions 文件夹
> cd ./data/std/functions
2. 运行 gen.py
> python gen.py
3. 此时test.mcfunction中应该已经被写入了很多东西，现在重复先前已经说过的步骤即可，注意，运行 `/function std:test` 后的等待时间取决于你的指令数，如果你的指令数非常多（接近1M行），那么大概需要等待1-2分钟的样子。实际上对于这类问题，有一种基于贪心的优化方案来大幅减少指令数，不过我并没有在本次项目中实现（能用就行

为了在截图时保证图片的完整性，请把游戏中的云关掉（esc-选项-视频设置-云:关）


## Grading Policy

> 该项目本着给大家玩玩的初衷，所以给分基准相对较高，不过由于是以最终效果为主，因此在评分标准上会主要关注你成果的 **美丽程度** 以及 **可复现性**，而不是你代码的美丽程度（此外，使用好看的光影并不能提高你的得分，请大家截图/录屏的时候使用Minecraft默认渲染方式），不过如果你尝试了某些优化，但是失败了，也可以写在报告里，会酌情根据有道理程度补分。

给分比例是拍脑袋想出来的，如果有异议希望各位提意见：

> 2025.06.30 修改了评分细则，使其变为了5分制给分，要求期望得分为4.0分

* Task1: 1%
  - 美观度 **0.5%**
  - 可复现性 **0.5%**

* Task2: 1.5%
  - 美观度 **1%**
  - 可复现性 **0.5%**
  - （Task2的期望得分为 **1.3分** ）

* Task3: 1.5%
  - 美观度 **0.5%**
  - 可复现性 **0.5%**
  - 选题的有趣程度 **0.5%**

* Report + (Video / CR): 1%
  - 为了让我记得你的实现效果大概如何，请你提交一份report讲一讲你Task3的实现细节，pdf格式，一些基础的东西就不用讲了，抓住最关键的部分即可，适当加入一些用于解释的图片
  - 另外，为了查看你的实现效果具体怎样，请你另外提交一份演示视频，展示你的Task2和Task3的运行过程，需要从运行python文件开始录制屏幕（不要用手机录屏），主要不是为了看视频的美观程度，而是验证一下真实性。不过如果你不想录视频的话，可以找我线下演示运行一遍。


## Outro

如果在“配环境”方面遇到任何问题，请立即联系TA

Good Luck, Have Fun!
