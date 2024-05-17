import cx_Oracle
import requests
from bs4 import BeautifulSoup

conn = cx_Oracle.connect('sys/Daneshkar/db19c', mode=cx_Oracle.SYSDBA)
cur = conn.cursor()
cur.execute('''create table Car_Infos (Names varchar(10), Prices float, Miles float,
Colors varchar(50) ,Conditions varchar(50))''')

for i in range (1, 6) :
    url = f'https://www.truecar.com/used-cars-for-sale/listings/?page={i}'
    used_cars_page = requests.get(url)

soup1 = BeautifulSoup(used_cars_page.text, 'html.parser')

used_cars_prices =  soup1.find_all('span', attrs = {'data-test' : 'vehicleListingPriceAmount'})
for i in range (len(used_cars_prices)) :
    sql1 = '''insert into Car_Info (Prices) values (:price)'''
    cur.execute(sql1, price=used_cars_prices[i])
used_cars_names =  soup1.find_all('span', attrs = {'class' : 'truncate'})
for i in range (len(used_cars_names)) :
    sql1 = '''insert into Car_Info (Names) values (:name)'''
    cur.execute(sql1, name=used_cars_names[i])
used_cars_miles =  soup1.find_all('div', attrs = {'class' : 'truncate text-xs', 'data-test' : 'vehicleMileage'})
for i in range (len(used_cars_miles)) :
    sql1 = '''insert into Car_Info (Miles) values (:mile)'''
    cur.execute(sql1, mile=used_cars_miles[i])
used_cars_conditions1 =  soup1.find_all('div', attrs = {'class' : "vehicle-card-location mt-1 truncate text-xs", 'data-test' : "vehicleCardColors"})
for i in range (len(used_cars_conditions1)) :
    sql1 = '''insert into Car_Info (Colors) values (:color)'''
    cur.execute(sql1, color=used_cars_conditions1[i])
used_cars_conditions2 =  soup1.find_all('div', attrs = {'class' : "vehicle-card-location mt-1 text-xs", 'data-test' :"vehicleCardCondition"})
for i in range (len(used_cars_conditions2)) :
    sql1 = '''insert into Car_Info (Conditions) values (:condition)'''
    cur.execute(sql1, condition=used_cars_conditions2[i])

rows = cur.fetchall()

cur.close()
conn.close()

print("Welcome Car Shopping!!!\n")
kindofcar = input("New or Used_Car? ")
if kindofcar == 'Used_Car' :
    name = input('Name of your desired car : ')
    price_low, price_high = map(int, input('Price range(low-high) : ').split('-'))
    i = 1
    for n, p in zip(used_cars_names, used_cars_prices) :
        if (n.text == name) and (int(p[1:]) > price_low and int(p[1:]) < price_high) :
            print('Information on Car ', i, ' : ')
            print('Price : ', used_cars_prices[i-1])
            print('Miles : ', used_cars_miles[i-1].text)
            print('Color and Conditions : ', used_cars_conditions1[i-1].text, used_cars_conditions2[i-1].text)
    i += 1

