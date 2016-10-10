# coding: utf8
from lxml import etree

root = etree.Element('data')
doc = etree.ElementTree(root)
tree = etree.parse("http://www.bigmir.net/", etree.HTMLParser())
links = tree.xpath('//a/@href')

counter = 20
while counter != 40:
    link = links[counter]

    if (not link.startswith("http:")):
        link = "http:" + link

    tree = etree.parse(link, etree.HTMLParser())
    images = tree.xpath("//img/@src")
    texts = tree.xpath("//*[not(self::script or self::style)]/text()[normalize-space(.)]")

    page_element = etree.SubElement(root, 'page', url=link)
    for text in texts:
        if not(text.isspace()):
            text_fragment = etree.SubElement(page_element, 'fragment', type='text')
            text_fragment.text = text
    for image in images:
        image_fragment = etree.SubElement(page_element, 'fragment', type='image')
        image_fragment.text = image
    counter += 1

doc.write('task1.xml', xml_declaration=True, encoding='utf-8')
