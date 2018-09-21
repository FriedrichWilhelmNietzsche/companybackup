#! /usr/bin/env python
# -*- coding: utf-8 -*-


# 深度遍历 广度遍历(仅取出来的方式不一样)
# 导入模块
import os, collections

def copyDir(sourcePath,targetPath):
    # 传入原目录,和需要复制后的目标目录
    # 判断需要复制的目录是否存在,如果不存在就返回
    if not os.path.isdir(sourcePath):
        return ( '源目录不存在' )
    # 创建两个栈,一个用来存放原目录路径,另一个用来存放需要复制的目标目录
    sourceStack = collections.deque()
    sourceStack.append(sourcePath)

    targetStack = collections.deque()
    targetStack.append(targetPath)
    # 创建一个循环当栈里面位空时结束循环
    while True:
        if len(sourceStack) == 0:
            break
        # 将路径从栈的上部取出
        sourcePath = sourceStack.pop()  #sourcePath = sourceStack.popleft()
        # 遍历出该目录下的所有文件和目录
        listName = os.listdir(sourcePath)

        # 将目录路径取出来
        targetPath = targetStack.pop()  #targetPath = targetStack.popleft()
        # 判断该目标目录是否存在,如果不存在就创建
        if not os.path.isdir(targetPath):
            os.makedirs(targetPath)
        # 遍历目录下所有文件组成的列表,判断是文件,还是目录
        for name in listName:
            # 拼接新的路径
            sourceAbs = os.path.join(sourcePath, name)
            targetAbs = os.path.join(targetPath, name)
            # 判断是否时目录
            if os.path.isdir(sourceAbs):
                # 判断目标路径是否存在,如果不存在就创建一个
                if not os.path.exists(targetAbs):
                    os.makedirs(targetAbs)
                # 将新的目录添加到栈的顶部
                sourceStack.append(sourceAbs)
                targetStack.append(targetAbs)
            # 判断是否是文件
            if os.path.isfile(sourceAbs):
                # 1.如果目标子级文件不存在 或者目标子级文件存在但是该文件与原子级文件大小不一致 则需要复制
                if (not os.path.exists(targetAbs)) or (os.path.exists(targetAbs) and os.path.getsize(targetAbs) != os.path.getsize(targetAbs)):
                    rf = open(sourceAbs, mode='rb')
                    wf = open(targetAbs, mode='wb')
                    while True:
                        # 一点一点读取,防止当文件较大时候内存吃不消
                        content = rf.read(1024*1024*10)
                        if len(content) == 0:
                            break
                        wf.write(content)
                        # 写入缓冲区时候手动刷新一下,可能会加快写入
                        wf.flush()
                    # 读写完成关闭文件
                    rf.close()
                    wf.close()
# 传入需要复制的目录和需要复制到的目标目录
sPath = r'C:\Users\Administrator\Desktop\20180920'
tPath = r'C:\Users\Administrator\Desktop\新建文件夹'
copyDir(sPath,tPath)



"""

复制目录: 包含多层子目录
递归, 深度遍历,广度遍历

# 递归思路
1.定义一个函数来复制目录,需要传入原目录和目标目录
2.判断源目录是否是一个目录--不是就终止
3.判断目标目录是否存在--不存在,新建
4.遍历源目录,

1.获得源目录子级目录,并设置目标目录的子级路径 
1.1在此就创建两个栈(或者队列),将原目录和目标目录分别添加到栈(或者队列)里面,一般用append添加,加在栈的顶部,队列的后部 
1.2深度遍历 从栈的顶部取出一个原路径去判断,同时用同样的方式取出目标路径(栈和队列都类似于list,都可以用list实现) 广度遍历 从队列的前面取出一个原路径去判断,同时用同样的方式取出目标路径 
2.判断原子级路径是否是文件 
2.1.如果目标子级文件不存在 或者目标子级文件存在,但是子级大小不一致,则复制 
3.判断原子级目录是否是目录 
3.1.递归 调用自己,把自己的子级目录当作源文件,复制到目标子级目录 
3.2.深度遍历 广度遍历 都将原目录和目标目录添加(append)到栈(队列)的后面


"""