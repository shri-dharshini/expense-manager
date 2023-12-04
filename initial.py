import mysql.connector as sql
mycon=sql.connect(host='localhost',user='root',passwd='root',database='expense')
cursor=mycon.cursor()

import datetime as dt
x=dt.datetime.now()
curmonth=x.month
prevmonth=x.month-1
if prevmonth==0:
    prevmonth=12
    
import matplotlib.pyplot as plt

import numpy as np

cursor.execute('select * from basics;')
initial=cursor.fetchall()
sal=float(initial[0][0])
rent=float(initial[0][1])
limit=float(initial[0][2])
cursor.execute('select sum(amount), month(dateofissue) from bonus group by month(dateofissue);')
initial=cursor.fetchall()
for i in initial:
    if i[1]==curmonth:
        bonus=float(initial[0][0])
        break


def executequery(a,b):
    cursor.execute(a,b)
    mycon.commit()
    
def inputbasics(check):
    global sal
    if check==1:
        oldsal=sal
        if oldsal==0:
            sal1=float(input('Enter your salary: '))
        else:
            sal1=float(input('Enter new salary: '))
        query='update basics set sal=%s where sal=%s;'
        val=(sal1,oldsal)
        executequery(query,val)
        sal=sal1
        
    elif check==2:
        global rent
        if rent==0:
            rent1=float(input('Enter your rent: '))
        else:
            rent1=float(input('Enter new rent: '))
        query='update basics set rent=%s where sal=%s;'
        val=(rent1,sal)
        executequery(query,val)
        rent=rent1



def inputbonus():
    global bonus
    bonus1=float(input('Enter bonus amount: '))
    query='insert into bonus values(now(),%s);'
    val=(bonus1,)
    executequery(query,val)
    bonus+=bonus1

def inputdata():
    cat=input('Enter category :')
    cat.lower()
    if cat=='groceries' or cat=='essentials':
        cat='grocandess'
    val=float(input('Enter amount   :'))
    notes=input('Enter notes    :')
    print('-'*77)
    values=(val,notes)
    if cat=='food':
        q1='insert into food values(now(),%s,%s);'
    elif cat=='commute':
        q1='insert into commute values(now(),%s,%s);'
    elif cat=='shopping':
        q1='insert into shopping values(now(),%s,%s);'
    elif cat=='grocandess':
        q1='insert into grocandess values(now(),%s,%s);'
    executequery(q1,values)

def limset():
    global limit
    oldlim=limit
    limit1=float(input('Enter new limit: '))
    query='update basics set limset=%s where limset=%s;'
    val=(limit1,oldlim)
    executequery(query,val)
    limit=limit1
  
def compare():
    psum=0
    avgf=avgg=avgs=avgc=0
    netf=netg=nets=netc=0
    prevavgf=prevavgg=prevavgs=prevavgc=0
    prevnetf=prevnetg=prevnets=prevnetc=0    
    print(' '*8,'CATEGORY',' '*11, 'AVERAGE SPENDING',' '*16,'NET SPENDING')
    print(' '*23, 'THIS MONTH',' '*4,'LAST MONTH',' '*5,'THIS MONTH',' '*4,'LAST MONTH')
    
    cursor.execute('select avg(amount),sum(amount), month(datespent) from food group by datespent;')
    values=cursor.fetchall()
    for i in range(len(values)):
        if values[i][2]==curmonth:
            avgf+=values[i][0]
            netf+=values[i][1]
        elif values[i][2]==prevmonth:
            prevavgf+=values[i][0]
            prevnetf+=values[i][1]
    print(' '*10, 'FOOD',' '*9, round(avgf,2),' '*9,round(prevavgf,2), ' '*10, netf, ' '*8, prevnetf)
    cursor.execute('select sum(amount), month(datespent) from food group by datespent having day(datespent)<=day(now())')
    val=cursor.fetchall()
    for i in range(len(val)):
        if val[i][1]==prevmonth:
            psum+=val[i][0]

    cursor.execute('select avg(amount),sum(amount), month(datespent) from commute group by datespent;')
    values=cursor.fetchall()
    for i in range(len(values)):
        if values[i][2]==curmonth:
            avgc+=values[i][0]
            netc+=values[i][1]
        elif values[i][2]==prevmonth:
            prevavgc+=values[i][0]
            prevnetc+=values[i][1]
    print(' '*9, 'COMMUTE',' '*7, round(avgc,2),' '*10,round(prevavgc,2), ' '*10, netc, ' '*8, prevnetc)
    cursor.execute('select sum(amount), month(datespent) from commute group by datespent having day(datespent)<=day(now())')
    val=cursor.fetchall()
    for i in range(len(val)):
        if val[i][1]==prevmonth:
            psum+=val[i][0]
    
    cursor.execute('select avg(amount),sum(amount), month(datespent) from shopping group by datespent;')
    values=cursor.fetchall()
    for i in range(len(values)):
        if values[i][2]==curmonth:
            avgs+=values[i][0]
            nets+=values[i][1]
        elif values[i][2]==prevmonth:
            prevavgs+=values[i][0]
            prevnets+=values[i][1]
    print(' '*8, 'SHOPPING',' '*7, round(avgs,2),' '*9,round(prevavgs,2), ' '*9, nets, ' '*7, prevnets)
    cursor.execute('select sum(amount), month(datespent) from shopping group by datespent having day(datespent)<=day(now())')
    val=cursor.fetchall()
    for i in range(len(val)):
        if val[i][1]==prevmonth:
            psum+=val[i][0]
    
    cursor.execute('select avg(amount),sum(amount), month(datespent) from grocandess group by datespent;')
    values=cursor.fetchall()
    for i in range(len(values)):
        if values[i][2]==curmonth:
            avgg+=values[i][0]
            netg+=values[i][1]
        elif values[i][2]==prevmonth:
            prevavgg+=values[i][0]
            prevnetg+=values[i][1]
    print(' '*8, 'GROCERIES',' '*6, round(avgg,2),' '*9,round(prevavgg,2), ' '*10, netg, ' '*8, prevnetg)
    cursor.execute('select sum(amount), month(datespent) from grocandess group by datespent having day(datespent)<=day(now())')
    val=cursor.fetchall()
    for i in range(len(val)):
        if val[i][1]==prevmonth:
            psum+=val[i][0]
    print()
    
    print('*'*30,'PERCENTAGAGE DISTRIBUTION','*'*30)
    sum=netg+netf+netc+nets
    f=(round((netf/sum)*100,2))
    g=(round((netg/sum)*100,2))
    c=(round((netc/sum)*100,2))
    s=(round((nets/sum)*100,2))
    print('GRAPHS SHOWN ABOVE')
    print()
    piechart(f,c,s,g)
    
    presavg=[avgf,avgc,avgs,avgg]
    presnet=[netf,netc,nets,netg]
    prevavg=[prevavgf,prevavgc,prevavgs,prevavgg]
    prevnet=[prevnetf,prevnetc,prevnets,prevnetg]
    barchart(prevavg,presavg,'avg')
    barchart(prevnet,presnet,'net')
   
    print()
    print('Amount spent this month till date is Rs.',sum)
    print('Amount spent last month till today\'s date is',psum)
    left=sal-rent+bonus-sum
    if limit!=0:
        limited=limit-sum
        if limited<=0:
            print('YOU HAVE CROSSED YOUR MONTHLY LIMIT!',)
            print('You have spent Rs.',-limited,'more than the set limit (Rs.',limit,')')
        else:
            print('Amount left that can be spend this month to stay within the limit is Rs.', limited)
    else:
        print('Amount left that can be spent this month is Rs.', left)    

def piechart(a=0,b=0,c=0,d=0):
    val=[a,b,c,d]
    l=['food','commute','shopping','groceries']
    maxv=max(val)
    exp=[0,0,0,0]
    for i in range(len(val)):
        if val[i]==maxv:
            exp[i]=0.2
    print('Maximum spending this month was in',l[val.index(maxv)],'category.')
    plt.pie(val,labels=l, explode=exp, shadow=True, autopct='%1.2f%%')
    plt.show()
    
def barchart(prev,pres,check):
    x=np.arange(len(prev))
    plt.bar(x, prev,width=0.35, label='previous month')
    plt.bar(x+0.35,pres, width=0.35, label='present month')
    plt.xticks(x,['food','commute','shopping','grocery'])
    plt.xlabel('CATEGORY')
    plt.legend(loc='upper right')
    if check=='avg':
        plt.title('Comparison of average expenditure')
        plt.ylabel('AVERAGE EXPENDITURE PER MONTH')
    else:
        plt.title('Comparison of net expenditure')
        plt.ylabel('NET EXPENDITURE PER MONTH')
    plt.show()
    
       
print('-'*77)
print(' '*30,'EXPENSE MANAGER')  
print('-'*77)
print()
print(' '*34,'WELCOME!')


if sal==0:
    print('*'*30,'SALARY INSERTION','*'*30)
    inputbasics(1)
    check=input('Would you like to enter your rent?(y/n): ')
    if check.lower()=='y':
        inputbasics(2)
else:
    print('Current salary is Rs.', sal)
    print('Current rent is Rs.', rent)
    check=input('Would you like to update your salary/ rent?(y/n): ')
    if check.lower()=='y':
        print('1.SALARY UPDATION\n2.RENT UPDATION')
        check=int(input('Enter your choice: '))
        inputbasics(check)
        if check==1:
            check=input('Would you like to update rent?(y/n): ')
            if check.lower()=='y':
                inputbasics(2)
        else:
            check=input('Would you like to update salary?(y/n): ')
            if check.lower()=='y':
                inputbasics(1)
print()
    
print('Net bonus recieved this month is Rs.',bonus)
check=input('Is there an occational bonus you would like to enter?(y/n):')
while check.lower()=='y':
    inputbonus()
    check=input('Enter another bonus?(y/n): ')
print()    


print('*'*30, 'ENTRY OF EXPENDITURE','*'*30)
print('CATEGORIES AVAILABLE:')
print('Food','Shopping','Commute','Groceries/Essentials')
check=input("Would you like to enter today's expenses?(y/n): ")
while True:
    if check.lower()=='n':
        break
    inputdata()
    check=input('Enter another value?(y/n): ')
print()

print('*'*33, 'SPENDING LIMIT','*'*33)
if limit==0:
    check=input('Would you like to set a monthly spending limit?(y/n): ')
else:
    print('Current spending limit is Rs.',limit)
    check=input('Would you like to update the monthly limit?(y/n):')
if check.lower()=='y':
    limset()
print()

print('*'*30,'STATISTICS OF EXPENDITURE','*'*30)
compare()
