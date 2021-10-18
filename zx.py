import sys
import requests
import random
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#你需要num.txt来存储学号信息(每行一个学号)

#以下两个是要填写的信息
#你的身份
snc_token=''
#社团ID
assId=''

session = requests.session()
headers = {
    'Host': 'studentclub.gzhu.edu.cn',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                  'Mobile/15E148 MicroMessenger/8.0.2(0x18000233) NetType/WIFI Language/en',
    'Referer': 'https://servicewechat.com/wxb78a5743a9eed5bf/15/page-frame.html',
    'Accept-Language': 'en-us',
    'snc-token':snc_token
}
session.headers = headers

inf_url = 'https://studentclub.gzhu.edu.cn/studentclub/number/studentInfoById'
join_url = 'https://studentclub.gzhu.edu.cn/studentclub/number/addNewNumber'
page_url='https://studentclub.gzhu.edu.cn/studentclub/number/selectMumberByAssId'
update_url='https://studentclub.gzhu.edu.cn/studentclub/number/updateNumber'

def get_inf(num):
    signin_data = {'params':{'numbers':num}}
    inf = session.post(inf_url, json=signin_data,verify=False).json()
    return inf

def join_dx(num,fail_find_num,join_num,fail_find_phone,upper_limit):
    inf=get_inf(num)
    if inf['data']==None:
        print('未查询到学号:'+num)
        fail_find_num.write(num+'\n')
        return 1
    elif not inf['data'].__contains__('mobilePhone'):
        print(inf['data']['studentName']+'未查询到电话,学号:' + num)
        inf['data'].update({'mobilePhone': ''})
        fail_find_phone.write(num+'\n')
    join_data ={'params':{'assId':assId,
                          'studentNumber':inf['data']['studentId'],
                          'phone':inf['data']['mobilePhone'],
                          'dutyCode':'4'}
                }
    res=session.post(join_url, json=join_data,verify=False).json()
    if res['msgCode']==501:
        if res['message'] == "该学生已加入的社团数已到上限":
            print(inf['data']['studentName'] + '已加入两个社团，学号:' + num)
            upper_limit.write(num+'\n')
            return 3
        join_num.write(num + '\n')  # 此同学已加入
        return 2
    return 0

#获取一页的信息，并没什么用
def get_page(page):
    page_data = {
	'params': {
		'pagination': {
			'pagenum': page,
			'pagesize': 10
		},
		'searchValue': '',
		"assId": assId
	}
    }
    res = session.post(page_url, json=page_data, verify=False).json()
    return res

#更新手机号码，用不到
def update_phone(number,phone):
    phone_data={
	"params": {
		"number": number,
		"key": "tel",
		"value": phone,
		"assId": assId
	}
    }
    res = session.post(update_url, json=phone_data, verify=False).json()

    return res

#批量更新手机号码，这并没什么用
def set_phone():
    inf=get_page(1)
    print('共有成员:',inf['data']['rowCount'])
    print('共有页数:', inf['data']['totalPage'])
    if inf['data']['records']==[]:
        print('无该页面:',1)
        return 0
    else:
        for i in inf['data']['records']:
            phone = get_inf(i['studentId'])
            if phone['data'] == None:
                print('未查询到学号:' + i['studentId'])
                continue
            elif not phone['data'].__contains__('mobilePhone'):
                print(phone['data']['studentName'] + '未查询到电话,学号:' + i['studentId'])
                continue
            update_phone(i['memberId'], phone['data']['mobilePhone'])
            time.sleep(random.random())
        print('已完成第', 1, '页')
    for k in range(2,inf['data']['totalPage']+1):
        inf = get_page(k)
        if inf['data']['records'] == []:
            print('无该页面:',k)
            return 0
        else:
            for i in inf['data']['records']:
                phone = get_inf(i['studentId'])
                if phone['data'] == None:
                    print('未查询到学号:' + i['studentId'])
                    continue
                elif not phone['data'].__contains__('mobilePhone'):
                    print(phone['data']['studentName'] + '未查询到电话,学号:' + i['studentId'])
                    continue
                update_phone(i['memberId'], phone['data']['mobilePhone'])
                time.sleep(random.random())
            print('已完成第', k, '页')
    return 1

#输出所有协会成员的学号到文件mem.txt
def out_mem_num():
    fd=open('mem.txt','a')
    inf = get_page(1)
    print('共有成员:', inf['data']['rowCount'])
    print('共有页数:', inf['data']['totalPage'])
    if inf['data']['records'] == []:
        print('无该页面:', 1)
        return 0
    else:
        for i in inf['data']['records']:
            fd.write(i['studentId']+'\n')
        print('已完成第', 1, '页')
    for k in range(2, inf['data']['totalPage'] + 1):
        inf = get_page(k)
        if inf['data']['records'] == []:
            print('无该页面:', k)
            return 0
        else:
            for i in inf['data']['records']:
                fd.write(i['studentId']+'\n')
            print('已完成第', k, '页')
    print('已完成输出会员信息')
    fd.close()
    return 1

#一个不知名的进度条
def progress_bar(num):
    print("\r", end="")
    print("已尝试录入{}人: ".format(num), "▋" * (num // 5), end="")
    sys.stdout.flush()

if __name__ == '__main__':
    #out_mem_num()#输出全部人
    #set_phone()#批量设置电话号码
    try:
        su = 0
        ha = 0
        fa = 0
        up = 0

        num = open('dx.txt', 'r')
        fail_find_num = open('fail_find_num.txt', 'a')
        fail_find_phone = open('fail_find_phone.txt', 'a')
        join_num = open('join_num.txt', 'a')
        upper_limit = open('upper_limit.txt', 'a')

        for n in num:
            res = join_dx(n.strip(), fail_find_num, join_num, fail_find_phone,upper_limit)
            if res == 0:
                su = su + 1
            elif res == 1:
                fa = fa + 1
            elif res == 2:
                ha = ha + 1
            else:
                up = up + 1
            progress_bar(su+fa+ha+up)
            time.sleep(random.random())

        print('\n新加入', su, '人')
        print('已加入', ha, '人')
        print('加入失败', fa+up, '人')
        print('超出2个社团',up,'人')
        num.close()
        fail_find_num.close()
        join_num.close()
        fail_find_phone.close()
        upper_limit.close()
    except Exception as e:
        print(e)