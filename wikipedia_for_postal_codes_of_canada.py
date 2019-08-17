import requests
import pandas as pd
from lxml import etree

wikiData = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M')
html = etree.HTML(wikiData.text)

#postal codes starting with letter M
postalCodeTable = html.xpath('//table[@class="wikitable sortable"]/tbody/tr')

tableHeaders = [col.text.strip() for col in postalCodeTable[0].xpath('th')]
postalCodes = pd.DataFrame(columns=tableHeaders[0:3])

for row in postalCodeTable[3:]:
    rowElements = row.xpath("td")
    rowData = [column.text.strip() if column.text is not None else column.xpath('a')[0].text.strip() for column in rowElements]
    postalCodes = postalCodes.append(pd.DataFrame([rowData],columns=tableHeaders[0:3]), ignore_index = True)

postalCodes.to_csv('postal_code_data.csv')


