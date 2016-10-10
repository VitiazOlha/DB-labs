# coding: utf8
from lxml import etree

root = etree.Element('page')
doc = etree.ElementTree(root)
site_url = "http://www.sokol.ua"
tree = etree.parse(site_url, etree.HTMLParser())
category_links = tree.xpath('//h2/a/@href')[1:2]
find_category_query = "//div[@class='white-block']/descendant::a[not(@class='sprite')]/@href"

for category in category_links:
    sub_links = etree.parse(category, etree.HTMLParser()).xpath(find_category_query)

    for sub in sub_links:
        next = sub
        product_links = []
        category_name = etree.SubElement(root, 'tr')
        text = etree.parse(next, etree.HTMLParser()).xpath('//h1[@class="inlineStyle"]/span/text()')
        if len(text) > 0:
            category_name.text = etree.parse(next, etree.HTMLParser()).xpath('//h1[@class="inlineStyle"]/span/text()')[0]

        while next != []:
            tree = etree.parse(next, etree.HTMLParser())
            product_links = product_links + tree.xpath('//section[@class="item"]')
            next = tree.xpath('//a[@name="next"][@class="next"]/@href')
            if next != []:
                next = site_url + next[0]

        for product in product_links:
            this_product = etree.fromstring(etree.tostring(product))

            image = this_product.xpath('//figure/descendant::img[@src]/@data_src')
            name = this_product.xpath('//header/div[@class="title"]/a/text()[normalize-space(.)]')
            description = this_product.xpath('//section/descendant::div[@class="description"]/text()[normalize-space(.)]')
            price = this_product.xpath('//div[@class="price price-style-2"]/span[@class="uah"]/text()|'
                                    '//div[@class="price price-red"]/span[@class="uah"]/text()')
            tr = etree.SubElement(category_name, 'tr')
            page_element = etree.SubElement(tr, 'image')
            if len(image) > 0:
                page_element.text = image[0]
            text_fragment = etree.SubElement(tr, 'name')
            if len(name) > 0:
                text_fragment.text = name[0].strip('\n').strip('\t').strip('\n')
            description_fragment = etree.SubElement(tr, 'description')
            if len(description) > 0:
                description_fragment.text = description[0]
            price_fragment = etree.SubElement(tr, 'price')
            if len(price) > 0:
                price_fragment.text = price[0]

doc.write('task3.xml', xml_declaration=True, encoding='utf-8', pretty_print=True)
