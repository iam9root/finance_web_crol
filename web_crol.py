import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import csv
import os
import time
import shutil

def len_name(x):

    sum=0
    a=''

    for i in x:
        if len(bytes(i, 'utf-8')) == 3:
            sum+=2
        elif len(bytes(i, 'utf-8')) == 1:
            sum+=1

    for j in range(24-sum):
        a+=' '

    return a

def write_list():
    f = open(desktop_path+'\\list.txt', 'r')
    readline=f.readlines()
    xlist = []

    for count in range(len(readline)):
        xlist.append('https://finance.naver.com/item/sise.nhn?code='+readline[count].split()[0])

    f.close()

    return xlist

def write_title():

    just_title=[]
    print('종목명\t\t\t종목 번호\t\t      시가\t      고가\t      저가\t      종가\t    거래량\t\t\t  조회 시간')
    just_title.append(['종목명', '종목코드', '시가', '고가', '저가', '종가', '거래량', '조회한 시간'])
    file = open(desktop_path+'\\original.csv', 'a', encoding='euc_kr', newline='')
    csvfile = csv.writer(file)

    for row in just_title:
        csvfile.writerow(row)

    file.close()

def web_crol2(i):

    try:
        url = i
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        csv_list = []
        my_titles = soup.select(
            'div > div > h2 > a'
            )
        my_num = soup.select(
            'div > div > div > span'
            ) 
        my_price = soup.select(
            'div > div > p > em > span'
            )
        my_low_price = soup.find(
            id="_low"
            )
        my_high_price = soup.find(
            id="_high"
            )
        my_volume = soup.find(
            id="_quant"
            )

        now = time.localtime()
        present_time = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        csv_list.append([my_titles[0].text, "'"+my_num[0].text, my_price[0].text, my_high_price.get_text(), my_low_price.get_text(), 
            my_price[0].text, my_volume.get_text(), present_time])
        print(my_titles[0].text+len_name(my_titles[0].text)+my_num[0].text.rjust(9,' ')+'\t\t'+my_price[0].text.rjust(10,' ')+'\t'+
            my_high_price.get_text().rjust(10,' ')+'\t'+my_low_price.get_text().rjust(10,' ')+'\t'+my_price[0].text.rjust(10,' ')+
            '\t'+my_volume.get_text().rjust(10,' ')+'\t\t'+present_time)
        file = open(desktop_path+'\\original.csv', 'a', encoding='euc_kr', newline='')
        csvfile = csv.writer(file)

        for row in csv_list :
            csvfile.writerow(row)

        file.close()

    except IndexError as e:
        f = open(desktop_path+'\\list.txt', 'r')
        readline=f.readlines()
        fail=[]

        for count in range(len(readline)):
            if i[-6:] in readline[count]:
                print(readline[count].split()[1] + ' 종목이 상장폐지 되었습니다.')
                fail.append([readline[count].split()[1] + ' 종목이 상장폐지 되었습니다.'])
                file = open(desktop_path+'\\original.csv', 'a', encoding='euc_kr', newline='')
                csvfile = csv.writer(file)
                for show in fail :
                    csvfile.writerow(show)
                file.close()

desktop_path=os.getenv('USERPROFILE')+"\\Desktop"
if __name__=='__main__':
    while True:

        now = time.localtime()
        present_time = '%02d%02d' % (now.tm_hour, now.tm_min)
        time_check = int(present_time)

        if 830 < time_check < 1532 :
            pass
        else:
            print('장이 마감되었습니다.')
            break

        start_time = time.time()
        file = open(desktop_path+'\\original.csv', 'a', encoding='euc_kr', newline='')
        csvfile = csv.writer(file)
        with open(desktop_path+'\\original.csv', 'a', encoding='euc_kr', newline='') as csvfile:
            csvfile.write('\n\n')

        write_title()
        pool = Pool(processes=8)
        pool.map(web_crol2, write_list())
        pool.close()
        pool.join()
        print("--- %s seconds ---" % (time.time() - start_time))

        try:
            shutil.copy(desktop_path+'\\original.csv', desktop_path+'\\copy1.csv')

        except PermissionError as a:
            shutil.copy(desktop_path+'\\original.csv', desktop_path+'\\copy2.csv')    
            
        time.sleep(900)