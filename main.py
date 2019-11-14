def usil(xx,k):
    '''Усилитель входного сигнала
    xx-входной сигнал на усилитель
    k-коэф.усиления
    ResUs-выход усилителя-усиленный сигнал'''
    ResUs=xx*k
    return Resus
def usil(vhod,k):
    '''Усилитель входного сигнала
    vhod-входной сигнал на усилитель
    k-коэф.усиления
    ResUs-выход усилителя-усиленный сигнал'''
    ResUs=vhod*k
    return ResUs
def inerz(x1,y1,t):
    '''Инерционное звено
    x1-входной сигнал в звено
    y1-выходной сигнал в предыдущий момент времени
    t-постоянная времени'''
    ResInerz=(x1+y1*t)/(1+t)
    return ResInerz
def integr(xi,yi):
    '''Интегратор
    xi-входной сигнал
    yi-выходной сигнал в предыдущий момент времени'''
    ResInt=0.001*xi+yi
    return ResInt
def sumator(xs1,xs2):
    '''Сумматор
    xs1-первый входной сигнал на сумматоре
    xs2-второй входной сигнал на сумматоре'''
    return xs1+xs2
def model(x,k1,k2,tt1,tt2,prev):
    '''Функция, реализующая моделирование САР
    x-входной сигнал всей САР
    k1,k2-коэф-ы усиления усилителей
    tt1,tt2-постоянные времени инерционных звеньев
    prev-список со значениями сигналов в предыдущий момент времени'''
    for i in range(len(x)):
        sumout=sumator(x[i],prev[0])
        usout1=usil(sumout,k1)
        inrout1=inerz(usout1,prev[1],tt1)
        prev[1]=inrout1
        inrout2=inerz(inrout1,prev[2],tt2)
        prev[2]=inrout2
        intout=integr(inrout2,prev[3])
        Y.append(intout)
        usout2=usil(intout,k2)
        prev[0]=usout2
# -*- coding: utf-8 -*-
import os
os.chdir('C:\\RashetPython')
X=3*[0]+1000*[1]
k1,k2=6,-1
t1,t2=0.25,0.625
delta=1.1
Y=[]
prev=[0,0,0,0]
model(X,k1,k2,t1,t2,prev)
fp=open('y.txt','w')
fp.write(' i         X[i]             Y[i]\n')
for i in range(len(X)):
    fp.write(' '+str(i)+'         '+str(X[i])+'    '+str(Y[i])+'\n')
fp.close()
print(Y)
import pylab
def graph(graphy,dlt,k1,k2):
    '''Функция построения графика выходного сигнала САР
    graphy-выходной сигнал САР
    dlt-продолжительность такта'''
    r=0
    t0=[]
    for i in range(len(graphy)):
	    t0.append(r)
	    r+=dlt
    pylab.plot(t0,Y)
    pylab.title('Выходной сигнал САР\nКоэффициент К1='+str(k1)+' Коэффициент K2='+str(k2))
    pylab.xlabel('Время')
    pylab.ylabel('Значение сигнала')
graph(Y,delta,k1,k2)
pylab.show()
