<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/echarts/5.6.0/echarts.min.js"></script>
<script type="text/javascript">
    var dom = document.getElementById('container-01');
    var myChart = echarts.init(dom, null, {
        renderer: 'canvas',
        useDirtyRect: false
    });
    var app = {};

    var option;

    option = {
    title: {
        text: '广东技术师范大学  软科中国大学排名（主榜）'
    },
    toolbox: {
        show: true,
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
    type: 'category',
    data: ['2021', '2022', '2023', '2024', '2025']
    },
    yAxis: {
    type: 'value',
    min: 250,
    max: 350,
    inverse: true,
    },
    series: [
    {
        data: [306, 292, 314, 328, 319],
        type: 'line',
        smooth: true,
        label:{
            show: true
        }
    }
    ]
    };

    if (option && typeof option === 'object') {
        myChart.setOption(option);
    }

    window.addEventListener('resize', myChart.resize);
</script>
<script type="text/javascript">
    var dom = document.getElementById('container-02');
    var myChart = echarts.init(dom, null, {
        renderer: 'canvas',
        useDirtyRect: false
    });
    var app = {};

    var option;

    option = {
    title: {
        text: '广东技术师范大学  武书连中国大学排名'
    },
    toolbox: {
        show: true,
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
    type: 'category',
    data: ['2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']
    },
    yAxis: {
    type: 'value',
    min: 200,
    inverse: true,
    },
    series: [
    {
        data: [400, 403, 439, 462, 474, 459, 469, 480, 454, 445, 438, 402, 449, 473, 454, 437, 478, 496, 468, 536, 481, 628, 416, 424],
        type: 'line',
        smooth: true,
        label:{
            show: true
        }
    }
    ]
    };

    if (option && typeof option === 'object') {
        myChart.setOption(option);
    }

    window.addEventListener('resize', myChart.resize);
</script>

## 学校排名

!!! ISSUE
    待修复错误：此处图表第一次不会加载，需要一次手动刷新才可见

[软科中国大学排名-直达链接](https://www.shanghairanking.cn/institution/guangdong-polytechnic-normal-university)
<div id="container-01" style="height: 250px"></div>
[武书连中国大学排名-直达链接](https://www.wurank.net/university/detail/24300,25,360)
<div id="container-02" style="height: 250px"></div>

## 高考招生
**志愿代码：10588**
[广东技术师范大学2025招生指南](https://mp.weixin.qq.com/s/Ppvia214q0oKWw5OLIthgA)
[广东技术师范大学2025年夏季高考招生计划](https://mp.weixin.qq.com/s?__biz=MzIwMzA3NzIyNg==&mid=2649987370&idx=1&sn=e7fa1b0532e8d7a6bd8de72ea6de4da3&chksm=8f9ec7091e67aa47345e6de49e1695389ddf93af745b587a9c61cd0ae01a0d0e4549c38d25b2&scene=0&xtrack=1&subscene=90#rd)

## 排名线
[早安广师大 | 划重点！多少分可以上广师大](https://mp.weixin.qq.com/s?__biz=MzIwMzA3NzIyNg==&mid=2649988203&idx=1&sn=196cd6af1ee2bac457b2c390f9f669d7&chksm=8f8f37f595b8c88db8c8f0c80bc1e97ce6c3ad9c2ff013c700223b1ef13880bbb2354d308d21&mpshare=1&scene=23&srcid=0627R4BoK3DNtlmgPodtufhw&sharer_shareinfo=e6bf194cf2e7fa15f970984e4b44931a&sharer_shareinfo_first=3abbad667b56b33dac8c535e0944d469#rd)

### QA


## 民族专项

!!! 注意
    在某些志愿辅助软件中，**少数民族专项**的分数会成为该专业录取最低分，请注意甄别。

仅身份证上的少数民族信息不足以报考少数民族专项，必须在高考报名时填写申请表认证公示。  
[广东省民族宗教委广东省招生委员会关于做好普通高校招收广东省少数民族聚居区少数民族考生工作的通知](https://www.gd.gov.cn/zwgk/gongbao/2020/17/content/post_3366829.html)  
!!! warning
    此处的消息未经验证，请仔细分辨


## 加分资格
[《官宣！最高20分！今年高考有2807人可加分上大学！》--广东考学妹](https://mp.weixin.qq.com/s/tmBaQLomi6sFuqwLTCzX9g)  
!!! warning
    此处的消息未经验证，请仔细分辨

## 专升本

[广东省2025年普通高等学校专升本招生工作规定](https://mp.weixin.qq.com/s?__biz=MzI4NjYzMTM4MA==&mid=2247559843&idx=1&sn=94f42b8883d63b94cc162ed0e17e5937&chksm=ea9501be5af47255603d47d0b6e00f45a27d04b9dcc162b48c700ed2cf94716aa998ef87a1b8&mpshare=1&scene=23&srcid=06241ANrxBOHboRARHOh9lLn&sharer_shareinfo=6bfc745c2f68b1c50055aa0d92da4018&sharer_shareinfo_first=6bfc745c2f68b1c50055aa0d92da4018#rd)
[2025年普通专升本招生录取情况](https://bkzs.gpnu.edu.cn/listInfo?menuId=7&parentId=2&id=4623)

## 国际班
[广东技术师范大学2025年国际班招生简章](https://mp.weixin.qq.com/s/0BlayJsTstNvzbAS23iDMA)

## 转专业
[关于做好我校2025年学生转专业工作通知](https://www.gpnu.edu.cn/info/1039/61509.htm)

有下列情况之一者，一般**不予**以转专业：  
1. 入学未满一学年的学生。  
2. 由专科升入本科，或由外校转学进入我校就读者且高考成绩低于拟转入专业同一生源地相应年份录取成绩的学生。  
3. 已转专业一次的学生。  
4. 在校期间有违纪等行为受到行政或党团组织警告及以上处分的学生。  
5. 招生时确定为定向、委托培养或联合培养的学生。  
6. 应作为退学处理或被开除学籍的学生。  
7. 艺术类与非艺术类专业之间互转的学生。  
8. 不符合当年招生专业对文、理科生源限制规定的学生。  
9. 无正当理由的学生。  

## 辅修专业/第二专业
TODO

## 专业信息

### 电子与信息学院
[电子与信息学院官网](https://dxxy.gpnu.edu.cn/)  
校区：白云校区 4年

#### 本科专业
| 专业                   | 资料                                                                                                                                                                                                                  |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 电子信息工程           | [2023版电子信息工程专业课程教学大纲](https://dxxy.gpnu.edu.cn/content.jsp?urltype=news.NewsContentUrl&wbtreeid=1288&wbnewsid=6206)<br>[电子信息工程专业人才培养方案](https://dxxy.gpnu.edu.cn/info/1114/2652.htm)     |
| 智能科学与技术         | [2023版智能科学与技术专业课程教学大纲](https://dxxy.gpnu.edu.cn/content.jsp?urltype=news.NewsContentUrl&wbtreeid=1288&wbnewsid=6204)<br>[智能科学与技术专业人才培养方案](https://dxxy.gpnu.edu.cn/info/1114/4731.htm) |
| 集成电路设计与集成系统 | [集成电路设计与集成系统-专业人才培养方案](https://dxxy.gpnu.edu.cn/info/1114/6273.htm)                                                                                                                                |
| 网络工程               | [2023版网络工程专业课程教学大纲](https://dxxy.gpnu.edu.cn/content.jsp?urltype=news.NewsContentUrl&wbtreeid=1288&wbnewsid=6202)<br>[网络工程-专业人才培养方案](https://dxxy.gpnu.edu.cn/info/1114/2560.htm)            |
| 应用电子技术教育       | [应用电子技术教育专业人才培养方案](https://dxxy.gpnu.edu.cn/info/1114/2557.htm)                                                                                                                                       |
| 通信工程               | [通信工程专业人才培养方案](https://dxxy.gpnu.edu.cn/info/1114/6261.htm)                                                                                                                                               |

#### 同学分享 
[blog/三年来的一些感悟](blog/posts/tieba-9790547930.md)

---

### 机电学院
[机电学院官网](https://jdxy.gpnu.edu.cn/)
校区：河源校区 1年 + 白云校区 3年

#### 本科专业

| 专业                   | 资料                                                                                                                                                                                                                                                                     |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 机械设计制造及其自动化 | [机械设计制造及其自动化专业课程教学大纲](https://jdxy.gpnu.edu.cn/nry.jsp?urltype=news.NewsContentUrl&wbtreeid=1283&wbnewsid=4122)                                                                                                                                       |
| 机械电子工程           |                                                                                                                                                                                                                                                                          |
| 材料成型及控制工程     | [材料成型及控制工程专业课程教学大纲](https://jdxy.gpnu.edu.cn/nry.jsp?urltype=news.NewsContentUrl&wbtreeid=1283&wbnewsid=4130)<br>[材料成型及控制工程（师范）专业课程教学大纲](https://jdxy.gpnu.edu.cn/nry.jsp?urltype=news.NewsContentUrl&wbtreeid=1283&wbnewsid=4131) |
| 机器人工程             |                                                                                                                                                                                                                                                                          |

---

### 计算机科学学院
[计算机科学学院官网](https://jkxy.gpnu.edu.cn/)
校区：河源校区 1年 + 东校区 3年

#### 本科专业

| 专业                 | 培养方案                                                                                                                                                                                                                                                                                                | 教学大纲                                                                                                                                                                                                                                                                                                           |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 计算机科学与技术     | [【2023版】计算机科学与技术（师范）专业人才培养方案](https://jkxy.gpnu.edu.cn/info/1259/6175.htm)<br>[【2023版】计算机科学与技术专业人才培养方案](https://jkxy.gpnu.edu.cn/info/1259/6174.htm)<br>[【2023版】计算机科学与技术（职教师资）专业人才培养方案](https://jkxy.gpnu.edu.cn/info/1259/6173.htm) | [2023版课程教学大纲-计算机科学与技术(20240313)](https://jkxy.gpnu.edu.cn/info/1345/5812.htm)<br>[2023版课程教学大纲-计算机科学与技术（职教师资）(20240313)](https://jkxy.gpnu.edu.cn/info/1345/5811.htm)<br>[2023版课程教学大纲-计算机科学与技术（师范）（20240313）](https://jkxy.gpnu.edu.cn/info/1345/5810.htm) |
| 电子商务             |                                                                                                                                                                                                                                                                                                         | [电子商务（师范）专业课程教学大纲](https://jkxy.gpnu.edu.cn/info/1345/6247.htm)                                                                                                                                                                                                                                    |
| 物联网工程           | [【2023版】物联网工程（师范）专业人才培养方案](https://jkxy.gpnu.edu.cn/info/1259/6171.htm)<br>[【2023版】物联网工程专业人才培养方案](https://jkxy.gpnu.edu.cn/info/1259/6170.htm)<br>[【2023版】物联网工程（三二分段）专业人才培养方案](https://jkxy.gpnu.edu.cn/info/1259/6169.htm)                   | [2023版课程教学大纲（物联网师范）](https://jkxy.gpnu.edu.cn/info/1345/5700.htm)<br>[2023版课程教学大纲（物联网三二分段）](https://jkxy.gpnu.edu.cn/info/1345/5699.htm)<br>[2023版课程教学大纲（物联网非师范）](https://jkxy.gpnu.edu.cn/info/1345/5697.htm)                                                        |
| ​人工智能            | [【2023版】人工智能（创新实验班）专业人才培养方案](https://jkxy.gpnu.edu.cn/info/1259/6168.htm)<br>[【2023版】人工智能专业人才培养方案](https://jkxy.gpnu.edu.cn/info/1259/6165.htm)                                                                                                                    | [2023年人工智能课程教学大纲](https://jkxy.gpnu.edu.cn/info/1345/5696.htm)<br>[2023年人工智能课程教学大纲（创新实验班）](https://jkxy.gpnu.edu.cn/info/1345/5695.htm)                                                                                                                                               |
| 数据科学与大数据技术 | [【2023版】数据科学与大数据技术专业人才培养方案](https://jkxy.gpnu.edu.cn/info/1259/6160.htm)                                                                                                                                                                                                           | [2023版大数据系课程教学大纲](https://jkxy.gpnu.edu.cn/info/1345/5714.htm)                                                                                                                                                                                                                                          |
| 软件工程             | [【2023版】软件工程专业人才培养方案](https://jkxy.gpnu.edu.cn/info/1259/6172.htm)                                                                                                                                                                                                                       | [2023年软件工程课程教学大纲](https://jkxy.gpnu.edu.cn/info/1345/5691.htm)                                                                                                                                                                                                                                          |
| 计算机学院国际班     |                                                                                                                                                                                                                                                                                                         | [软工-国际班-2023版课程教学大纲240322](https://jkxy.gpnu.edu.cn/info/1345/5865.htm)<br>[计科-国际班-2023版课程教学大纲240322](https://jkxy.gpnu.edu.cn/info/1345/5864.htm)                                                                                                                                         |

### 汽车与交通工程学院
[汽车与交通工程学院官网](https://qcxy.gpnu.edu.cn/)
校区：河源校区 1年 + 白云校区 3年

#### 本科专业

### 自动化学院
[自动化学院官网](https://zdhxy.gpnu.edu.cn/)
校区：河源校区 1年 + 白云校区 3年

#### 本科专业

### 光电工程学院
[光电工程学院官网](https://gdxy.gpnu.edu.cn/)
校区：河源校区 1年 + 白云校区 3年

#### 本科专业

### 体育与健康学院
[体育与健康学院官网](https://tyb.gpnu.edu.cn/)
校区：河源校区 4年

#### 本科专业

### 数学与系统科学学院
[数学与系统科学学院官网](https://sxxy.gpnu.edu.cn/)
校区：河源校区 1年 + 白云校区 3年

#### 本科专业

### 数据科学与工程学院
[数据科学与工程学院官网](https://dase.gpnu.edu.cn/)
校区：河源校区 4年

#### 本科专业

### 教育科学学院
[教育科学学院官网](https://jky.gpnu.edu.cn/)
校区：河源校区 1年 + 白云校区 3年

#### 本科专业

### 网络空间安全学院
[网络空间安全学院官网](https://scs.gpnu.edu.cn/)
校区：西校区 4年

#### 本科专业

### 财经学院
[财经学院官网](https://cjxy.gpnu.edu.cn/)
校区：河源校区 1年 + 白云校区 3年

#### 本科专业

### 法学与知识产权学院
[法学与知识产权学院官网](https://fzxy.gpnu.edu.cn/)
校区：河源校区 1年 + 白云校区 3年

#### 本科专业

#### 知名校友

### 管理学院
[管理学院官网](https://glxy.gpnu.edu.cn/)
校区：河源校区 1年 + 白云校区 3年

#### 本科专业

### 外国语学院
[外国语学院官网](https://wgyxy.gpnu.edu.cn/)
校区：河源校区 1年 + 白云校区 3年

#### 本科专业

### 文学与传媒学院
[文学与传媒学院官网](https://wxycb.gpnu.edu.cn/)
校区：河源校区 1年 + 白云校区 3年

#### 本科专业

### 美术学院
[美术学院官网](https://msxy.gpnu.edu.cn/)
校区：河源校区 1年 + 东校区 3年

#### 本科专业

### 音乐学院
[音乐学院官网](https://yyxy.gpnu.edu.cn/)
校区：河源校区 1年 + 东校区 3年

#### 本科专业

### 民族学院
[民族学院官网](https://mzxy.gpnu.edu.cn/)
校区：河源校区 1年 + 白云校区 3年

#### 本科专业

### 马克思主义学院
[马克思主义学院官网](https://mksxy.gpnu.edu.cn/)
校区：河源校区 1年 + 白云校区 3年

#### 本科专业

### 国际教育学院
[国际教育学院官网](https://gjxy.gpnu.edu.cn/)
校区：河源校区 1年 + 白云校区 3年

#### 本科专业

### 基础教育学院
[基础教育学院官网](https://jcjy.gpnu.edu.cn/)
校区：河源校区 4年

#### 本科专业

| 专业     | 人才培养方案                                                                  | 课程教学大纲                                                                  |
| -------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| 小学教育 | [小学教育人才培养方案（2023版）](https://jcjy.gpnu.edu.cn/info/1274/1105.htm) | [小学教育课程教学大纲（2023版）](https://jcjy.gpnu.edu.cn/info/1273/1104.htm) |

#### 硕士专业

| 专业     | 资料                                                                                                                          |
| -------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 小学教育 | [2024年广东技术师范大学基础教育学院小学教育专业硕士研究生招生复试与录取工作方案](https://jcjy.gpnu.edu.cn/info/1275/1102.htm) |

### 数字创意学院
[数字创意学院官网](https://szcy.gpnu.edu.cn/)
校区：河源校区 4年

#### 本科专业

| 专业         | 专业介绍                                                    |
| ------------ | ----------------------------------------------------------- |
| 环境设计     | [环境设计](https://szcy.gpnu.edu.cn/info/1094/1220.htm)     |
| 数字媒体艺术 | [数字媒体艺术](https://szcy.gpnu.edu.cn/info/1094/1219.htm) |

### 继续教育学院
[继续教育学院官网](https://jxjy.gpnu.edu.cn//)
校区：

#### 成人教育
#### 自学考试
#### 特色招生

### 广东工业实训中心
[广东工业实训中心官网](https://gyzx.gpnu.edu.cn/)
校区：东校区

### 创新创业学院
[创新创业学院官网](https://cxxy.gpnu.edu.cn/)
校区：东校区 白云校区