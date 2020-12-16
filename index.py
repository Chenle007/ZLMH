# b=()  #元组类型
# print(type(b))
# c=[]  #列表类型
# print(type(c))
# d={}  #字典类型
# print(type(d))
#
# scroe = 60
# if scroe <= 60:
#     print("成绩不理想哦！")
#     pass #空语句
#
# scroe = int(input("请输入成绩："))
# if scroe >=90:
#     print("你的成绩为“优”")
# elif scroe >=60:
#     print("你的成绩及格了")
# else:
#     print("你没有及格哦")

import random #导入产生随机数模块
user = int(input("请出拳 0：石头 1：剪刀 2：布"))
com = random.randint(0,2)
if user ==0 and com ==1:
    print("厉害了，你赢了")
elif user ==1 and com ==2:
    print("厉害了呀 你居然赢了")
elif user ==2 and com ==0:
    print("牛逼 你赢了")
elif user ==com:
    print("我们平局了哦")
else:
    print("哈哈哈，你输了吧！")





