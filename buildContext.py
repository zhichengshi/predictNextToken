from xml.dom import minidom



specialCharachter=set(["\r","\t","\n",""])
# 深度优先遍历获得所有叶子节点
def dfsLeaves(root,leaves):
    if root.nodeType == 3 and root.nodeValue.strip() not in specialCharachter : # 若当前节点是叶子节点
        leaves.append(root)
    for child in root.childNodes:
        dfsLeaves(child,leaves)
    return leaves



# 输入文件路径,根据该文件路径后再情景对
def buildContext(path):
    # 深度优先遍历获得所有叶子节点
    def dfs(root,leaves):
        if root.nodeType is "TEXT_NODE": # 若当前节点是叶子节点
            leaves.append(root)
        for child in root.childNodes:
            dfs(child,leaves)

def removeComment(root):
    if root.nodeType==1:
        if root.tagName=="comment" or root.tagName=="literal":
            root.parentNode.removeChild(root)
    for child in root.childNodes:
        removeComment(child)
    return root
        
    
if __name__=="__main__":
    path="/Users/shizhicheng/Desktop/test3.xml"
    # 获取DOM对象
    with open(path,"r") as f:
        dom=minidom.parse(f)
    # 获取根节点
    root=dom.documentElement
    root=removeComment(root)
    leaves=dfsLeaves(root,[])
    print(leaves)