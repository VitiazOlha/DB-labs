## About
Lab #1 project for databases 5th semester course: basic XML documents processing. Variant #3
## Goals
* Fetch 20 HTML pages starting from `https://www.bigmir.net/` recursively, parse, extract text and image urls using XPATH. Parsing results save as XM
L file of the following structure:
```xml
<data>
<page url=”wwww.example.com/index.hml”>
<fragment type=”text”>
.... text data
</fragment>
<fragment type=”image”>
.... image url
</fragment>
</page>
<page url=”wwww.example.com/page.hml”>
<fragment type=”text”>
.... text data
</fragment>
<fragment type=”image”>
.... image url
</fragment>
</page>
...
</data>
```

* Using XPATH get minimal text fragments count in dataset
* Fetch name, price and image for 20 products from online store `http://www.sokol.ua/` using XPATH, save as XML file.
* Transform product list XML into HTML table using XSLT
