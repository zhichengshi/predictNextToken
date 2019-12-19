import sys
import xml.etree.ElementTree as ET
import re
from xml.dom import minidom
import numpy as np
# 根据树的根节点打印该函数的源码
# 方法： 如果当前标记的尾标记有内容，则先打印标记中的内容再打印尾标记
def traverse(root):
    if root.tail != None:
        if root.text != None:
            print(root.text, end="")
        for node in root:
            traverse(node)
        print(root.tail, end="")
    else:
        if root.text != None:
            print(root.text, end="")
        for node in root:
            traverse(node)

# 解析xml
def parseXML(path):
    try:
        tree = ET.parse(path)
        # 获得根节点
        root = tree.getroot()
        return root
    except Exception as e:  # 捕获除与程序退出sys.exit()相关之外的所有 异常
        print("parse test.xmlProcess fail!")
        sys.exit()

# 翻转抽象语法树
def reverse(path1,path2):
    with open(path1) as f:
        string=f.read()
    # string=string.replace("<"," $$<").replace(">",">$$")
    # tokens=string.split("$$")
    tokens=removeAtt(string) # 移除属性
 
    tokens=np.asarray(tokens)
    tokens=tokens[::-1]

    newTokens=[]
    for i  in range(0,len(tokens)):
        token=tokens[i]
        if token.startswith('<') and token.endswith("/>"):
            continue
        if token.startswith('</') and token.endswith(">"):
            newTokens.append(token.replace("</","<"))
            continue
        if token.startswith('<') and token.endswith(">"):
            newTokens.append(token.replace('<',"</"))
            continue
        newTokens.append(token)
      
    
    string=''.join(newTokens)
    print(string)
    with open(path2,"w") as f:
        f.write(string)

# 移除xml中节点的属性
def removeAtt(string):
    string=string.replace("<"," $$<").replace(">",">$$")
    tokens=string.split("$$")
    newTokens=[]
    for i in range(0,len(tokens)):
        token=tokens[i]
        if token.startswith("<") and token.endswith(">"):
            characters=list(token)
            string=""    
            for character in characters:
                if character !=" ":
                    string +=character
                else:
                    if token.endswith("/>"):
                        string +="/>"
                    else:
                        string +=">"
                    break
            token=string
        newTokens.append(token)
    return newTokens



if __name__=="__main__":
    path1="C:\\Users\\w\\Desktop\\test.xml"
    path2="C:\\Users\\w\\Desktop\\test4.xml" 
    root=parseXML(path2)
    traverse(root)

  

   
  

 