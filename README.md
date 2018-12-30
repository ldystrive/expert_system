## 基于规则的专家系统 - 宠物猫推荐



### 概述

用户选择喜欢的猫的特征来推荐比较适合的猫的种类，并给出该种类猫的一张照片，该系统中现有十种比较受欢迎的宠物猫，可以添加更多的规则来添加更多的猫。系统中现有的猫种类有：

+ 苏格兰折耳猫
+ 波斯猫
+ 布偶猫
+ 美国短毛猫
+ 暹罗猫
+ 狸花猫
+ 英国短毛猫
+ 金吉拉猫
+ 安哥拉猫
+ 挪威森林猫

用户可选的特征有：

+ 体型大小及是否易胖体质
+ 头的形状及大小
+ 腿的长短
+ 猫毛的长短
+ 尾巴长短
+ 眼睛形状
+ 耳朵形状及大小
+ 性格

demo:

使用 python3+eel

```
// 先安装eel
// pip3 install eel 
// 如果安装失败，请先升级pip和setuptools
// python3 -m pip install --upgrade pip
// pip3 install --upgrade setuptools
// 打开系统
python3 ui.py
```

示例：

![demo1](D:\lessons\人工智能A\expert_system\readmeImg\demo1.png)



### 系统结构

包括规则(rules)、事实(facts)、推理引擎(engine)、ui和用户

规则为一些特征与猫匹配的条件，如：

```
IF head_shape is round
AND body_size_mid
AND fat is true
AND legs_short
AND hair_length_short
AND tail_length_short
AND eyes_shape is round
AND ears_size_mid
AND ears_shape is round
AND temperament is docile
THEN ScottishFold
```

事实由最初用户选择的条件和推理引擎产生的一些中间结果

推理引擎为该系统的核心，利用规则和用户选择的特征来产生一些事实

ui提供用户和专家系统的交互

用户可以选择一些猫的特征



### 规则构建

详细的规则写在```src/rule.txt``` 中，程序运行时，先申请一个实例，然后初始化规则，通过专家系统中的```readRule()```来解析规则，放入```self.rules``` 中 

```python
es = ExpertSystem()
es.readRule('src/rule.txt')
```

首先，猫的大小、腿的长度、毛的长度等等可能不是一个明确的大、中、小分类，可能是小or中、中or大。将这些条件组合起来，直接写每个猫的特征会及其复杂，会写很多冗余的内容。所以我们可以先提取一下这些特征，如下：

```shell
IF legs_short
OR legs_mid
THEN legs_short_mid

IF legs_mid
OR legs_long
THEN legs_mid_long
```

```legs_short``` 表示短腿，```legs_short_mid``` 表示中等或短腿，把这些规则放到规则的最前面，优先级最高，减少冗余规则的编写

然后由于本系统现在只有十个品种的猫，相对来说可选的特征较多，如果直接匹配每个规则，推理引擎极有可能找不出符合条件的猫，所以本系统使用带优先级的规则专家系统。使用几个优先级：

* 完整条件优先级较高，设为第一优先级

+ 放宽一些条件限制，例如将长腿放宽条件为中长腿，设置为第二优先级
+ 删掉一些相对来说不重要的特征，例如耳朵的形状可能就不是很重要，放到第三优先级

可以区分出每个特征的重要性，添加更多的优先级，使系统的推荐效果更好。也可以给系统添加更多种类的猫，推荐的效果会更好。



### 事实数据库

本系统中事实数据库主要用来存放初始用户选择的条件和推理引擎工作是产生的中间结果，例如```legs_short_mid``` 中或短腿就存放在facts中，推理引擎工作时，规则的条件也需要从数据库在数据库中查找，判断规则是否成立





### 推理引擎

```ExpertSystem.engineWork()``` 

本系统使用前向链接，根据用户输入的特征根据规则去寻找符合条件的猫

+ step1: 将用户的输入特征放入到facts中
+ step2: 按优先度遍历每一个rule
+ step3: 对于每个rule，判断then后面的结果是否在facts中，若出现过则跳过这个rule
+ step4: 判断rule的条件是否成立，条件分为两种：1. 用```AND``` 连接的，2.用```OR``` 连接的，需要判断这个rule是哪种连接
+ step5: 若产生一个新的facts，则跳到step2重新遍历每个rule。若遍历完所有rule都没有新的fact产生便结束推导

由于是按照优先级遍历rules，所以引擎推导出的第一个品种的猫就是推荐的猫



### 界面

界面使用```eel```和web应用进行交互，用户点击```submit```按钮后，将选择的特征发送给推理引擎，推理引擎进行推导，返回最符合条件的猫的种类的照片

初始时，用户没有进行选择，所以展示一张默认的动画片中的猫。并且由于现在本系统中猫的种类有限，若出现对于用户选择的特征没有匹配的猫，也将展示这张默认图片

![demo_default](D:\lessons\人工智能A\expert_system\readmeImg\demo_default.png)



一些实例展示：

金吉拉猫:

![demo2](D:\lessons\人工智能A\expert_system\readmeImg\demo2.png)





布偶猫:

![demo3](D:\lessons\人工智能A\expert_system\readmeImg\demo3.png)



暹罗猫:

![demo4](D:\lessons\人工智能A\expert_system\readmeImg\demo4.png)



### 总结

1. 本系统中猫的种类太少，以至于只能通过放宽条件来让这个系统能够正常使用，可以通过添加更多的种类给用户提供更加精准的建议
2. 对于用户来说，猫的颜色应该是一个比较重要的特征，但由于每种猫的颜色较多，部分猫的颜色种类多达80+种，再添加颜色特征会增加大量的规则，所以现阶段没有使用颜色特征