# -*- coding: utf-8 -*-
"""
Created on Fri May 20 22:21:12 2016

@author: ldl
"""

from lxml import etree
html='''
<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title>测试-常规用法</title>
</head>
<body>
<div id="content">
    <ul id="useful">
        <li>这是第一条信息</li>
        <li>这是第二条信息</li>
        <li>这是第三条信息</li>
    </ul>
    <ul id=“useless”>
        <li>1不需要的信息</li>
        <li>2不需要的信息</li>
        <li>3不需要的信息</li>
    </ul>

    <div id="url">
        <a href="属性1">这个不属于属性值</a>
        <a href="属性2" href2="属性3">这个也不是属性值</a>
        <a href3="attribute">3也不是属性值</a>
   </div>
</div>

</body>
</html>
'''
selector=etree.HTML(html)

#提取文本信息
# content=selector.xpath('//ul[@id="useful"]/li/text()')
# for each in content:
    # print each

#此语句打印出了标签a下的内容
content2=selector.xpath('//a/text()')
for each in content2:
    print each

#提取属性
content3=selector.xpath('//a/@href')
for each in content3:
    print each

content4=selector.xpath('//a/@href2')
print content4[0]

content5=selector.xpath('//a[@href3="attribute"]/text()')
print content5[0]
