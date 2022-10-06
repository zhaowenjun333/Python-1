#
from lxml import etree
import csv

wb_data = """
<div>
    <ul>
        <li class="item.txt-0"><a href="link1.html">first item.txt</a></li>
        <li class="item.txt-1"><a href="link2.html">second item.txt</a></li>
        <li class="item.txt-inactive"><a href="link3.html">third item.txt</a></li>
        <li class="item.txt-1"><a href="link4.html">four item.txt</a></li>
        <li class="item.txt-0"><a href="link5.html">fifth item.txt</a></li>
    </ul>
</div>
"""

# 1.
html_element = etree.HTML(wb_data)
# print(html_element)

# 2.
links = html_element.xpath('//li/a/@href')
# print(links)
results = html_element.xpath('//li/a/text()')
# print(results)

# 3.
# lis = html_element.xpath('//li')   # []
# for i in lis:
#     a = i.xpath('.//a')
#     print(a)

lst = []
for i in range(len(links)):
    dic = {}
    dic['href'] = links[i]
    dic['title'] = results[i]
    # print(dic)
    lst.append(dic)
print(lst)
