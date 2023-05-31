from lxml import etree

words = '王届0专博78中4杨女6高B校以经大陈吴1士9刘M应张无本验李男技5硕E黄3下2周赵生科A'
words = list(words)
with open('./zitiku1.xml', 'rb') as f:
    xml = f.read()
    xml_element = etree.XML(xml)
    TTGlyph_lst = xml_element.xpath('//TTGlyph')[1:-1]
    TTGlyphs = []
    for TTGlyph in TTGlyph_lst:
        xMin = TTGlyph.xpath('.//@xMin')[0]
        yMin = TTGlyph.xpath('.//@yMin')[0]
        xMax = TTGlyph.xpath('.//@xMax')[0]
        yMax = TTGlyph.xpath('.//@yMax')[0]
        TTGlyphs.append((xMin, yMin, xMax, yMax))
words_dict = {}
for k, v in zip(words, TTGlyphs):
    words_dict[v] = k
print(words_dict)
