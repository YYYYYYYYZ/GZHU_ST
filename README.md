# 社团入会——本程序仅是学习记录，仅用于学习作用
## 依赖库
import sys  
import requests  
import random  
import time  
import urllib3  
## 以下两个是要填写的信息，需要抓取
### 你的身份
snc_token=''
### 社团ID
assId=''
## 输入文件num.txt格式:
学号一  
学号二  
.  
.  
.  
## 输出文件作用
join_num.txt 已加入的学号  
fail_find_num.txt 未找到的学号  
fail_find_phone.txt 无手机号码的学号——可以加入社团，但是手机号栏为空  
upper_limit.txt 加入社团超出上限的学号
