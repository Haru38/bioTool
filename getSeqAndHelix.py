import pandas as pd
from urllib.request import urlopen
import numpy as np
from lxml import etree
import re
import pickle

resultDatas = []
cantGetData = []
uniIds = ["Q8NGS9","Q9GZM6","Q8NGI2"]
for i,uniId in enumerate(uniIds):
    print(i,"/",len(uniIds))
    url = "https://www.uniprot.org/uniprot/" + uniId + ".xml"
    f = urlopen(url)
    xml = f.read()
    root = etree.fromstring(xml)

    sequence = root.find('./entry/sequence', root.nsmap)#sequenceの取得
    datas = xml.decode().split("\n")
    getData = []
    count = 0
    for index,data in enumerate(datas):
        if "transmembrane region" in data:
            count += 1
            namePattern = r'.*?(Name=\d)'
            nameResult = re.match(namePattern,data)
            try:
                resultDatas.append([uniId,sequence.text ,nameResult.group(1),datas[index+2],datas[index+3]])
            except:
                cantGetData.append(uniId)

output_file = "sample"
with open(output_file+".dump","wb") as f:
    pickle.dump({
        "success" : resultDatas,
        "false" : cantGetData
    },f)