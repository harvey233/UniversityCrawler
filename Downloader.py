import json
import yaml
import requests
import prettytable as pt

def printInfo(data):
    f1 = open('./data/Student.info', 'w', encoding = 'utf-8')
    f1.write('[')
    for i in range(len(data['rows'])):
        f1.write('{' '"name":"'+ data['rows'][i]['xm'] + '",' + '"id":"' +\
        data['rows'][i]['xh'] + '","' + 'num":"'+ data['rows'][i]['xyxjxxid'] +'"}')
        if i < len(data['rows']) - 1:
            f1.write(',')
    f1.write(']')
    f1.close()

def getSource():
    url = ''
    f1 = open('./Headers.yaml', 'r', encoding = 'utf-8')
    f2 = open('./FromData.yaml', 'r', encoding = 'utf-8')
    headers = yaml.load(f1.read(), Loader=yaml.FullLoader)
    data = yaml.load(f2.read(), Loader=yaml.FullLoader)
    headers['Content-Length'] = str(headers['Content-Length'])
    try:
        response = requests.post(url, data=data, headers=headers, timeout=30)
        response.encoding = response.apparent_encoding
        print ('扫描成功!!')
        return response.text
    except:
        print('扫描出错!!')
    f1.close(); f2.close()

def printList(data):

    f1 = open('./Export/Student.list', 'w', encoding = 'utf-8')
    f1.write('\n\t\t\t\t\t\t\t\t\t\t\t\tXXXXX大学 16-19级 学员名单\n\n')
    tb = pt.PrettyTable();
    tb.field_names = ["姓名", "专业", "教学班", "学号", "系统ID"]
    for i in range(len(data['rows'])):
        data['rows'][i]['xh'] = int(data['rows'][i]['xh'])
    data['rows'] = sorted(data['rows'], key=lambda x:x['xh'])
    for i in range(len(data['rows'])):
        tb.add_row([data['rows'][i]['xm'],data['rows'][i]['xyzymc'],
            data['rows'][i]['jxb'],data['rows'][i]['xh'],data['rows'][i]['xyxjxxid']])
    f1.write(str(tb))
    f1.close()

def main():
    opt = getSource() # scan students' information
    if opt != -1:
        printList(json.loads(opt))
        # printInfo(json.loads(opt))

main()