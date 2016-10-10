from lxml import etree

print min(map(lambda item: int(item.xpath('count(fragment[@type = "image"])')), etree.parse("task1.xml").xpath('//page')))
# tree = etree.parse("task1.xml")
# links = tree.xpath('//page')
# y = map(lambda item: int(item.xpath('count(fragment[@type = "image"])')), links)
# print y
# print min(y)
