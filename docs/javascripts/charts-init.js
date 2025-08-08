/* ECharts 初始化（适配 MkDocs Material SPA） */
(function(){
  function ensureEcharts(cb){
    if (window.echarts) return cb();
    // 若 CDN 未加载（理论上会在 mkdocs.yml 注入），则动态加载一次
    var script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/echarts/5.6.0/echarts.min.js';
    script.async = true;
    script.onload = cb;
    document.head.appendChild(script);
  }

  function initChart(id, option){
    var el = document.getElementById(id);
    if (!el) return;
    // 防止重复初始化
    if (el.dataset.echartsInited === '1') return;

    var chart = window.echarts.init(el, null, { renderer: 'canvas', useDirtyRect: false });
    chart.setOption(option);
    window.addEventListener('resize', function(){ chart.resize(); });
    el.dataset.echartsInited = '1';
  }

  function getOptions(){
    return {
      c1: {
        title: { text: '广东技术师范大学  软科中国大学排名（主榜）' },
        toolbox: { show: true, feature: { saveAsImage: {} } },
        xAxis: { type: 'category', data: ['2021','2022','2023','2024','2025'] },
        yAxis: { type: 'value', min: 250, max: 350, inverse: true },
        series: [{ data: [306,292,314,328,319], type: 'line', smooth: true, label: { show: true } }]
      },
      c2: {
        title: { text: '广东技术师范大学  武书连中国大学排名' },
        toolbox: { show: true, feature: { saveAsImage: {} } },
        xAxis: { type: 'category', data: ['2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023','2024','2025'] },
        yAxis: { type: 'value', min: 200, inverse: true },
        series: [{ data: [400,403,439,462,474,459,469,480,454,445,438,402,449,473,454,437,478,496,468,536,481,628,416,424], type: 'line', smooth: true, label: { show: true } }]
      }
    };
  }

  function run(){
    // 确保容器已在 DOM 中（Material SPA 导航会替换 .md-content）
    ensureEcharts(function(){
      var opts = getOptions();
      initChart('container-01', opts.c1);
      initChart('container-02', opts.c2);
    });
  }

  // 监听 Material 的文档更新事件
  if (window && window.document$ && typeof window.document$.subscribe === 'function') {
    window.document$.subscribe(function(){ setTimeout(run, 0); });
  } else {
    document.addEventListener('DOMContentLoaded', function(){ setTimeout(run, 0); });
    window.addEventListener('load', function(){ setTimeout(run, 0); });
  }
})();
