from pyquery import PyQuery as pq

html_doc = """
<html>
<head>
    <title>The Dormouse's story</title>
</head>
<body>
    <p class="title">
        <b>The Dormouse's story</b>
    </p>

    <p class="story one">
        Once upon a time there were three little sisters; and their names were
        <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
        <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
        <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
        and they lived at the bottom of a well.
    </p>
    <p class="story two">...</p>
</body>
</html>
"""

doc = pq(html_doc)
# 输出：标签
# print(doc('title'))
# 结果：<title>The Dormouse's story</title>

# 输出：文本
# print(doc('title').text())
# 结果：The Dormouse's story

# 通过class进行定位
# print(doc('p.title'))

# 获取所有满足条件的标签
# items = doc('a.sister').items()
# for a in items:
#     print(a)
#     # 获取属性
#     print(a.attr('href'))


# items = doc('.story')
# print(items)
# print(type(items))

# afind = items.find('#link3').text()
# print(afind)

# 查看子元素
# children()查找所有直接子元素
# a_more = items.children()
# print(a_more)
# print(type(a_more))


# 查看父元素
# link1 = doc('#link1')
# print(link1)
# link_parent = link1.parent()
# print(link_parent)
# 祖先节点
# parents = link1.parents()
# print(parents)
# print(type(parents))


# 查看兄弟标签
# p = doc('.story.one')
# print(p)
# brother = p.siblings()
# print(brother)

# sister = doc('.sister').items()
# for a in sister:
#     print(a)


# DOM操作
# addClass、removeClass
# p = doc('.story.one')
# print(p)
# p.remove_class('one')
# print(p)
# p.add_class('one')
# print(p)

# attr css
# 添加属性
p = doc('.title')
p.attr('name', 'title')
print(p)
