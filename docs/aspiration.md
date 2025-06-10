# 广师大高考志愿填报指南

## 学校排名

[软科中国大学排名-直达链接](https://www.shanghairanking.cn/institution/guangdong-polytechnic-normal-university)
<div id="container-01" style="height: 200px"></div>
[武书连中国大学排名-直达链接](https://www.wurank.net/university/detail/24300,25,360)
<div id="container-02" style="height: 200px"></div>

<script type="text/javascript" src="https://fastly.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
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

## 宣传视频 2025

<video src="/assets/welcome2025.mp4"></video>

!!! 注意
    在某些志愿辅助软件中，少数民族专项的分数会成为该专业录取最低分，请注意甄别。

## 专业信息

### 电子与信息学院 [[官网链接](https://dxxy.gpnu.edu.cn/)]

| 专业                   | 往届分数线 | 校区    | 培养计划                                               | 相同专业同学分享 |
| ---------------------- | ---------- | ------- | ------------------------------------------------------ | ---------------- |
| 电子信息工程(师范)     |            |         | [[官网链接](https://dxxy.gpnu.edu.cn/info/1114/2562.htm)] |                  |
| 电子信息工程           |            |         | [[官网链接](https://dxxy.gpnu.edu.cn/info/1114/2652.htm)] |                  |
| 智能科学与技术         |            |         | [[官网链接](https://dxxy.gpnu.edu.cn/info/1114/4731.htm)] |                  |
| 集成电路设计与集成系统 |            |         | [[官网链接](https://dxxy.gpnu.edu.cn/info/1114/6273.htm)] |                  |
| 网络工程               |            | 白云4年 | [[官网链接](https://dxxy.gpnu.edu.cn/info/1114/2560.htm)] |                  |
| 应用电子技术教育       |            |         | [[官网链接](https://dxxy.gpnu.edu.cn/info/1114/2557.htm)] |                  |
| 通信工程               |            |         | [[官网链接](https://dxxy.gpnu.edu.cn/info/1114/6261.htm)] |                  |
