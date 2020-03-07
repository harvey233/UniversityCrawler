import json
import yaml
import requests
import prettytable as pt

def queryNum(target):
    f1 = open('./data/Student.info', encoding = 'utf-8')
    data = json.loads(f1.read())
    for i in range(len(data)):
        if (target == data[i]['name'] or target == data[i]['id']):
            f1.close()
            return data[i]
    f1.close()
    return -1

def querySocre(string):
    url = ''
    f1 = open("./Query/Headers.yaml", 'r', encoding = 'utf-8')
    f2 = open("./Query/FormData.yaml", 'r', encoding = 'utf-8')
    f3 = open('./Export/result.txt', 'w', encoding='utf-8')
    target = queryNum(string)
    if target == -1:
        print('未知的学生!!')
        return -1
    params = {'search$xyId.id$EQ': target['num']}
    headers = yaml.load(f1.read(), Loader=yaml.FullLoader)
    data = yaml.load(f2.read(), Loader=yaml.FullLoader)
    headers['Content-Length'] = str(headers['Content-Length'])
    try:
        response = requests.post(url, params=params, data=data, headers=headers, timeout=30)
        response.encoding = response.apparent_encoding
        print ('查询成功!!\n请在 ./Export/result.txt 查看')
        #print(reponse.text)
        f3.write('\n\t\t\t\t\t\t' + target['name'] + '(学号:'+ target['id'] + ')' + '的成绩单:\n\n')
        f1.close(); f2.close(); f3.close();
        return response.text
    except:
        print('查询出错!!')
        f1.close(); f2.close(); f3.close()
        return -1


def printSocre(data):
    f1 = open("./Export/result.txt", "a", encoding='utf-8')
    tb1 = pt.PrettyTable(); tb2 = pt.PrettyTable()
    tb1.field_names = ["学期", "课程名", "课程属性", "学分", "总评成绩", "绩点学分"]
    tb2.field_names = ["参加课程", "完成课程", "已修学分", "绩点/学分"]
    sum1 = 0.0; sum2 = 0.0; sum3 = 0
    for i in range(len(data['rows'])):
        list = [data['rows'][i]['xnxq'], data['rows'][i]['kcmc'], data['rows'][i]['kcsx'],
                data['rows'][i]['xf'], data['rows'][i]['zpcj'], data['rows'][i]['jdxf']]
        if list[2] == '01': list[2] = '必修课'
        elif list[2] == '02': list[2] = '选修课'
        else: list[2] = '实践课'
        if not (list[4] is None) and not(list[5] is None):
            sum3 += 1; sum1 += float(list[3]); sum2 += float(list[5])
        if list[4] is None: list[4] = '暂无'
        if list[5] is None: list[5] = '暂无'
        tb1.add_row(list)
    tb2.add_row([len(data['rows']),sum3, sum1, sum2/sum1])
    f1.write(str(tb1) + '\n')
    f1.write(str(tb2))
    f1.close()

def main():
    string = str(input("请输入姓名或学号："))
    opt = querySocre(string) # print one's socre

    if opt != -1:
        printSocre(json.loads(opt))

def on_click():
    string = str(x)
    tkinter.messagebox.showinfo('查询成功!!','报告文件：./Export/result.txt')


main()
