import time
import random
import threading

#本程序是对地月之间的通信进行模拟仿真，分为发送端，通道和接收端，三个组成部分三线程运行
framelen=64*8
tr=384403.9/300000
message_len=3840*1920*24*3
send_go_flag=0      #发送端写，通道端读的状态位
send_back_flag=0    #通道端写，接收端读的状态位
receive_go_flag=0   #ack信息到达通道
receive_back_flag=0 #ack信息到达发送端
send_ack=0          #发送端接收到的ack
receive_ack=0       #接收端发送的ack
is_end=0
p1=0.3    #数据帧出错概率
p2=0.3    #数据帧丢失概率
p3=0.3    #确认帧丢失概率

def send():
    global message_len,framelen,is_end,send_go_flag,send_back_flag
    total=message_len//framelen+1
    cnt=0
    ack=0
    while(1):
        resend=0   #重发计数器
        if (cnt>=total):
            is_end=1
            break
        lock.acquire()
        send_go_flag=1
        lock.release()
        print("发送第"+str(cnt+1)+"帧")
        start=time.time()
        while(1):
            now=time.time()
            if (now-start)>2*tr+1:
                resend=resend+1
                print("对第"+str(cnt+1)+"帧进行第"+str(resend)+"次重发......")
                start=now
                lock.acquire()
                send_go_flag=1
                lock.release()
            if (send_back_flag):
                lock.acquire()
                send_back_flag=0
                lock.release()
                if (send_ack==ack^1):
                    break
        print("第"+str(cnt+1)+"帧确认发送成功\n")
        ack=ack^1
        cnt=cnt+1


def path():
    print("path")
    global is_end,send_go_flag,receive_go_flag,send_back_flag,send_ack,receive_ack
    while(1):
        if (is_end):
            break
        if(send_go_flag):   #传输数据
            time.sleep(tr)
            lock.acquire()
            send_go_flag=0
            lock.release()
            if(random.random()>p2):
                lock.acquire()
                receive_go_flag=1
                lock.release()
            else:
                print("数据传输丢失......")
        if(receive_back_flag):  #传输确认帧
            time.sleep(tr)
            receive_go_flag=0
            if(random.random()>p3):
                lock.acquire()
                send_back_flag=1
                send_ack=receive_ack
                lock.release()
            else:
                print("ACK传送丢失......")


def receive():
    global is_end,receive_go_flag,receive_go_flag,receive_back_flag,receive_ack
    print("receive")
    ack=1
    while(1):
        if (is_end):
            break
        if (receive_go_flag):
            lock.acquire()
            receive_go_flag=0
            lock.release()
            if(random.random()>p1):
                lock.acquire()
                receive_back_flag=1
                receive_ack=ack
                lock.release()
                ack=ack^1
                print("数据正确，接收成功......")
            else:
                lock.acquire()
                receive_back_flag=1
                receive_ack=-1
                lock.release()
                print("数据出错......")


path_tread=threading.Thread(target=path)
receive_tread=threading.Thread(target=receive)
lock=threading.Lock()
start_time=time.time()
path_tread.start()
receive_tread.start()
send()
end_time=time.time()
print("传输总耗时："+str(end_time-start_time)+"秒")
