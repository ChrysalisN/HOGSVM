# HogSvm

## 目标
 实现对人头的检查并尝试标出来。

## 使用方法
  1. 解压后，rawdata是要放置的数据。`_0`表示负样本，`_1`表示正样本。无需resize。datamake.py文件会进行resize操作
  2. 运行datamake.py文件后，文件会将rawdata中的数据图片放置到data文件夹下。（如data不存在会自动新建data文件夹)
  3. 运行data/datamk.py，会将data文件夹下的图片分类放置到/data/images/neg\_position或/data/images/pos\_position下。之后的特征提取与保存时从这两个文件下读文件。
  4. 运行object\_detector/extract\_features.py提取HOG并保存。
  5. 运行object\_detector/train\_svm.py进行支持向量机的训练并保存模型。
  6. 运行detect\_detector/detect.py进行对`test_image_mine`文件夹的测试图片的检测，并展示效果。
##.其他说明:
- inforce.py用于增强，简单修改代码中的字符串匹配可以改为是复制正样本还是复制负样本。
- mname.py（manage name）用于管理rawdata的图片名称。虽然图片名称毫无影响。只要\_1还是\+0正确标注就行。
- getsize.py 用于获取rawdata中图片的分辨率。最初是用于辨认测试图片中应设置的窗口大小。生成了img\_shape.txt
- __datamk.py与inforce.py因为调用的是linux中的`cp`命令进行的复制文件，所以需要在WSL下运行（windows subsystem for linux)可以在Microsoft Store中安装。或者在Linux下或其他terminal下运行。（斜眼笑）当然，最简单的还是自己改下代码，替换复制操作就好了。__
