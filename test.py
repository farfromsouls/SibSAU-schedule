import re


x = 'ывпывап  ап вп ап вапрывапыв Пятница'

try:
    print(x[:x.index('Пятница')])
except:
    print('нет подстроки')