from pyecharts.charts import Line
from pyecharts import options as opts
from html_compress import compress_html_file

# 软科中国大学排名（主榜）- 越小越好

bar = Line(
    init_opts=opts.InitOpts(
        width="100%",
        height="250px",
        bg_color="rgba(0, 0, 0, 0)"
    )
)
bar.add_xaxis(["2021", "2022", "2023", "2024", "2025"])
bar.add_yaxis("软科中国大学排名（主榜）- 越小越好", [306, 292, 314, 328, 319])
bar.set_global_opts(
    yaxis_opts=opts.AxisOpts(
        min_="dataMin",
        max_="dataMax"
    )
)
bar.render("shanghairanking.html")

compress_html_file("shanghairanking.html", "shanghairanking_escape.html")

# 武书连中国大学排名 - 越小越好

bar = Line(
    init_opts=opts.InitOpts(
        width="100%",
        height="250px",
        bg_color="rgba(0, 0, 0, 0)"
    )
)
bar.add_xaxis(["2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"])
bar.add_yaxis("武书连中国大学排名 - 越小越好",
              [449, 473, 454, 437, 478, 496, 468, 536, 481, 628, 416, 424])
bar.set_global_opts(
    yaxis_opts=opts.AxisOpts(
        min_="dataMin",
        max_="dataMax"
    )
)
bar.render("wurank.html")

# 使用封装的函数压缩HTML
compress_html_file("wurank.html", "wurank_escape.html")

