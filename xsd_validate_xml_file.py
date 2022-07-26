import lxml
from lxml import etree

xml_file = lxml.etree.parse("D:/2021_8_16_oborot/ish_unziped/VO_OTKRDAN5_9965_9965_20210729_000f7269-b452-4bb0-85ea-3fa614ec3342.xml")
xml_validator = lxml.etree.XMLSchema(file="D:/2021_8_16_oborot/structure-20180110.xsd")

is_valid = xml_validator.validate(xml_file)

print(is_valid)
