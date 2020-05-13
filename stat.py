import random
import csv
import time
from matplotlib import pyplot as plt

#本程序为根据出错概率计算传输时间
p1=0.1 #数据帧出错概率
p2=0.1 #数据帧丢失概率
p3=0.1 #确认帧丢失概率
framelen=64*8
tr=384403.9/300000
message_len=3840*1920*24*3
total_frame=message_len//framelen+1
p1_time=[]
p2_time=[]
p3_time=[]
for precent in range(100):
    p1_tmp=precent/100
    sum_time=0
    i=0
    while(i<total_frame):
        sum_time+=2*tr
        if (random.random()<p2):
            sum_time+=2*tr
            i=i-1
        else:
            if (random.random()<p1_tmp):
                sum_time+=2*tr
                i=i-1
            elif(random.random()<p3):
                sum_time+=2*tr
                i=i-1
        i=i+1
    p1_time.append(sum_time)
    print(sum_time)
for precent in range(100):
    p2_tmp=precent/100
    sum_time=0
    i=0
    while(i<total_frame):
        sum_time+=2*tr
        if (random.random()<p2_tmp):
            sum_time+=2*tr
            i=i-1
        else:
            if (random.random()<p1):
                sum_time+=2*tr
                i=i-1
            elif(random.random()<p3):
                sum_time+=2*tr
                i=i-1
        i=i+1
    p2_time.append(sum_time)
    print(sum_time)
for precent in range(100):
    p3_tmp=precent/100
    sum_time=0
    i=0
    while(i<total_frame):
        sum_time+=2*tr
        if (random.random()<p2):
            sum_time+=2*tr
            i=i-1
        else:
            if (random.random()<p1):
                sum_time+=2*tr
                i=i-1
            elif(random.random()<p3_tmp):
                sum_time+=2*tr
                i=i-1
        i=i+1
    p3_time.append(sum_time)
    print(sum_time)
result=[p1_time,p2_time,p3_time]
for i in range(3):
    File=open("p"+str(i+1)+"_time"+str(p1)+".csv","w")
    writer=csv.writer(File)
    writer.writerow(["time","precentage"])
    for j in range(100):
        writer.writerow([result[i][j],j/100])
    File.close()
# send.sendmail()