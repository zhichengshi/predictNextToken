import sys
import xml.etree.ElementTree as ET
import copy
# 带双亲节点的树节点
class treeNode:
    def __init__(self, parent=None, current=None,tag=None):
        self.parent=parent
        self.parentTag=tag
        self.current=current #该变量的数据结构和原AST中的结构一样
        self.tag=tag

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

# 构造情景向量数据集
def generateContextDataset(nodes,upSize,downSize,siblingUsing):
    
    # 获得当前节点的所有情景节点
    def generateContext(node,upSize,downSize,siblingUsing):
        contextNodes=set()
        contextNodes=findDescendants(contextNodes,node.current,downSize,0) #加入子孙节点
        n=0
        parent=node.parent
        while n < upSize and parent !=None:  #加入祖先节点
            contextNodes.add(parent.current.tag)
            parent=parent.parent
            n+=1
        
        if siblingUsing == True and node.parent != None: #判断是否使用兄弟节点，如果使用则在情景向量中加入兄弟节点
            for child in node.parent.current:
                contextNodes.add(child.tag)
        
        return contextNodes
    
    # 根据窗口大小，获得当前节点所有的子孙节点
    def findDescendants(result,node,maxdepth,depth):
        if depth >= maxdepth:
            return set()

        # 将当前节点的孩子节点放入result
        for child in node.getchildren():
            result.add(child.tag)

        # 将孩子节点的孩子节点放入result
        for child in node.getchildren():
            descendantNodes=findDescendants(result,child,maxdepth,depth+1)
            result=result | descendantNodes
        
        return result


    contextDataset=[]
    for node in nodes:  #遍历树上的所有节点，构造出所有节点的情景向量对
        contextNodes=generateContext(node,upSize,downSize,siblingUsing)
        for contextNode in contextNodes:
            if node.tag != contextNode:
                contextDataset.append((node.tag,contextNode))
    
    return contextDataset

# 预处理抽象语法树
#（1）删除注释
#（2）将叶子节点加入到双亲节点的孩子列表中
# (3) 重新构建ast,给节点添加双亲节点
# 返回整个抽象语法树的节点
def preprocessAst(root):
    
    # 将叶子节点添加到其双亲节点的孩子节点列表中 
    def transform(root):
        if root.text!=None:
            root.append(ET.Element(root.text.strip()))
        for child in root:
            transform(child)
        return root  

    # 移除注释节点
    def removeComment(root,parent):
        for child in root.getchildren():
            if child.tag=="comment":
                root.remove(child)
                continue
            removeComment(child,root)
        return root
    
    # 给所有节点加上双亲节点
    def reconstructTree(parent,current,nodes):
        nodes.append(treeNode(parent,current,current.tag))
        for child in current.getchildren():
            parent=treeNode(parent,current,current.tag)
            reconstructTree(parent,child,nodes)
        return nodes

    
    root=removeComment(root,None)
    root=transform(root)
    nodes=reconstructTree(None,root,[])
    return nodes



if __name__=="__main__":
    path="/Users/shizhicheng/Desktop/test.xml"
    root=parseXML(path)
    nodes=preprocessAst(root)
    contextDataset=generateContextDataset(nodes,1,1,True)
    for ele in contextDataset:
        print(ele)