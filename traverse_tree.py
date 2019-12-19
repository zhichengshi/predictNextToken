import sys
import xml.etree.ElementTree as ET

class treeNode:
    def __init__(self,parent,node,children):
        self.parent=parent
        self.node=node
        self.children=children
# 解析xml
def parseXML(path):
    try:
        tree = ET.parse(path)
        # 获得根节点
        root = tree.getroot()
        return root
    except Exception as e:  # 捕获除与程序退出sys.exit()相关之外的所有 异常
        print("parse tbcnn.xmlProcess fail!")
        sys.exit()

def transform(root):
    if root.text!=None:
        root.append(ET.Element(root.text))
    for child in root:
        transform(child)
    
    return root

def traverse(root):
    print(root.tag)
    for child in root:
        traverse(child)
    
if __name__ =="__main__":
    path="/Users/shizhicheng/Desktop/test.xml"
    root=parseXML(path)
    root=transform(root)
    traverse(root)
