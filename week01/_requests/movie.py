import requests
import pandas as pd
from bs4 import BeautifulSoup as bs


user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

cookie = '__mta=214915368.1595729169975.1595729511253.1595729516796.8; uuid_n_v=v1; uuid=91DF7E70CEE411EAACA59DB4EC64C4A81A3350F864DB496E86E9FCE0789E74F9; _csrf=63953af58cf6aa2ee1b6ad67e77409408f9e6ab5ec2252265ea508648878a9bb; _lxsdk_cuid=17388decdd1c8-093c63ffd10222-31617403-1fa400-17388decdd1c8; _lxsdk=91DF7E70CEE411EAACA59DB4EC64C4A81A3350F864DB496E86E9FCE0789E74F9; mojo-uuid=a477c029bcb1c2a6c573360ed1967228; mojo-session-id={"id":"4e5b4698113396e405d9f7799c8186e3","time":1595729169957}; lt=iOSIt4nYa3hIX_tXf7yfTd5QEdMAAAAAHAsAACnGueM3MFYb5V34skxuW555cjYPLsLRWZg1hpHY_nuKtxpmiJI9i6tFC---bSPVaQ; lt.sig=cInxeSjAWXs40JSo9cMx-7Ga7EY; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1595729170,1595729215,1595729264,1595729297; __mta=214915368.1595729169975.1595729499367.1595729511253.7; mojo-trace-id=13; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1595729517; _lxsdk_s=17388decdd2-04c-28a-d13%7C%7C20'

headers = {
    'User-Agent': user_agent,
    'Cookie': cookie
}

url = 'https://maoyan.com/films?showType=3&sortId=3'

response = requests.get(url, headers=headers)

bs_info = bs(response.text, 'html.parser')

# with open('1.html', 'r', encoding='utf-8') as f:
#      html = f.read()

# bs_info = bs(html, 'html.parser')

data = [
    [ 'name', 'type', 'date' ]
]

top = 10
for tags in bs_info.findAll('div', attrs={'class': 'movie-hover-info'}):
    if top > 0:
        temp = []
        for aTags in tags.findAll('div', attrs={'class': 'movie-hover-title'}):
            # print('---------------------')
            # print(aTags.text.split('\n'))
            temp.append(aTags.text)
        name = temp[0].split('\n')[1].strip()
        type = temp[1].split('\n')[2].strip()
        date = temp[3].split('\n')[2].strip()
        temp.clear()
        temp.append(name)
        temp.append(type)
        temp.append(date)
        print(temp)
        data.append(temp)
        top -= 1


# print(data)
movie1 = pd.DataFrame(data = data)
movie1.to_csv('./movie1.csv', encoding='utf8', index=False, header=False)


'''
    name = 'movies'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3&sortId=3']
    cookies = {
        '__mta': '214915368.1595729169975.1595729511253.1595729516796.8',
        'uuid_n_v': 'v1',
        'uuid': '91DF7E70CEE411EAACA59DB4EC64C4A81A3350F864DB496E86E9FCE0789E74F9', 
        '_csrf': '63953af58cf6aa2ee1b6ad67e77409408f9e6ab5ec2252265ea508648878a9bb',
        '_lxsdk_cuid': '17388decdd1c8-093c63ffd10222-31617403-1fa400-17388decdd1c8',
        '_lxsdk': '91DF7E70CEE411EAACA59DB4EC64C4A81A3350F864DB496E86E9FCE0789E74F9', 
        'mojo-uuid': 'a477c029bcb1c2a6c573360ed1967228',
        'mojo-session-id': '{"id":"4e5b4698113396e405d9f7799c8186e3","time":1595729169957}',
        'lt': 'iOSIt4nYa3hIX_tXf7yfTd5QEdMAAAAAHAsAACnGueM3MFYb5V34skxuW555cjYPLsLRWZg1hpHY_nuKtxpmiJI9i6tFC---bSPVaQ',
        'lt.sig': 'cInxeSjAWXs40JSo9cMx-7Ga7EY',
        'Hm_lvt_703e94591e87be68cc8da0da7cbd0be2': '1595729170,1595729215,1595729264,1595729297',
        '__mta': '214915368.1595729169975.1595729499367.1595729511253.7',
        'mojo-trace-id': '13',
        'Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2': '1595729517',
        '_lxsdk_s': '17388decdd2-04c-28a-d13%7C%7C20'
    }

'''
    



