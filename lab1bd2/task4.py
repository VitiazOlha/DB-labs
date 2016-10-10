# coding: utf8
from lxml import etree

tree = etree.parse("task3.xml")
xslt_root = etree.XML('''\
<?xml version="1.0" encoding="WINDOWS-1251"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<html xmlns="http://www.w3.org/1999/xhtml">
<table border="1">
<xsl:for-each select="page/tr">
<tr bgcolor="#CCCCCC">
<td align="center">
<strong>
<xsl:value-of select="text()"/>
</strong>
</td>
</tr>
<xsl:for-each select="tr">
<tr bgcolor="#F5F5F5">
<td>
<img>
<xsl:attribute name="src">
<xsl:value-of select="image"/>
</xsl:attribute>
</img>
</td>
<td align="left">
<strong>
<xsl:value-of select="name"/>
</strong>
<br />
<xsl:value-of select="description"/>
</td>
<td>
<xsl:value-of select="price"/>
</td>
</tr>
</xsl:for-each>
</xsl:for-each>
</table>
</html>
</xsl:template>
</xsl:stylesheet>''')

transform = etree.XSLT(xslt_root)

my_file = open("task4.xhtml", 'w')
my_file.write(etree.tostring(transform(tree)))
my_file.close()
