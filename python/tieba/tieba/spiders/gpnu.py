from pathlib import Path
import random

import scrapy

class GPNUSpider(scrapy.Spider):
    name = "gpnu"
    
    def start_requests(self):
        base_url = "https://tieba.baidu.com/f?kw=%E5%B9%BF%E4%B8%9C%E6%8A%80%E6%9C%AF%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6&ie=utf-8"
        min_pn = 0
        max_pn = 12400 # 12400
        step = 50
        
        urls = []
        # 添加基础URL（没有pn参数，相当于pn=0）
        if min_pn == 0:
            urls.append(base_url)
            
        # 生成带有pn参数的URL
        for pn in range(min_pn, max_pn + step, step):
            if pn > 0:  # pn=0的情况已经处理过了
                urls.append(f"{base_url}&pn={pn}")
            
        for url in urls:
            yield scrapy.Request(url=url,
                                callback=self.parse,
                                 )

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = f"quotes-{page}.html"
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")

        for quote1 in response.css('div.main'):
            for quote2 in quote1.css('li.j_thread_list'):
                yield {"title": quote2.css('a').get()}