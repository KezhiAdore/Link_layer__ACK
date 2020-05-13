# Link_layer__ACK

## 地月模拟通信

![地月模拟通信](http://download.kezhi.tech/img/20200417132254.png)

编写三个函数分别模拟发送端，通道，和接收端：

- 发送端：发送帧时写send_go_flag，计时器打开，读取send_back_flag判断是否有接收端发的反馈信息，如果有，则读取send_ack获取反馈信息。当send_ack中的信息正确，则可以确认接收成功，发送下一帧，否则当计时器的时间大于规定时间时，重新发送本帧，重置计时器
- 通道：读send_go_flag判断是否有数据待发送，如果有，将send_go_flag重置，经过地月延迟时间之后receive_go_flag。读receive_back_flag判断是否有反馈信息待发送，如果有，将receive_back_flag重置，经过地月延迟之后，写send_back_flag，将receive_ack中的数据写入send_ack
- 接收端：读取receive_go_flag判断是否有数据到达，之后进行数据验证，如果数据重复则无动作，数据正确则发送当前ack之后ack=ack^1，数据错误则发送-1，发送ack即对receive_back_flag进行改写，ack信息写入receive_ack。

本次模拟中无实际信息发送，传输中出现的错误均为随机数模拟，其中的数据出错在接收端进行数据验证时概率出错。数据帧丢失和确认帧丢失在传输通道中概率出现。

运行截图：

![image-20200417141743542](http://download.kezhi.tech/img/20200417141745.png)

## 通信时长统计

![传输失败](http://download.kezhi.tech/img/20200417133722.png)

由上图可以看出，通信失败一共有三种情形。使用循环对于发送信息进行模拟，如果三种情况均为出现则循环变量+1，总时长+一次通信时常；否则循环变量不变，总时长+一次通信时常。

选取几种情况下的通信时常，在其中两个概率不变时，改变一个事件出现的概率得到的结果如下：

> 其余两个因素产生概率均为0.01 0.05 0.1，变量变化区域为0:0.01:0.99

<table>
    <tr>
        <td><center><img src="http://download.kezhi.tech/img/20200417140611.png">p1</center></td>
        <td><center><img src="http://download.kezhi.tech/img/20200417140433.png">p2</center></td>
        <td><center><img src="http://download.kezhi.tech/img/20200417140637.png">p3</center></td>
    </tr>
</table>

可以看出在0.8之后的变化几乎为直线上升，因此将变量范围改为0:0.01:0.8

> 其余两个因素产生概率为0.01,0.05,0.1，变量变化区域为0:0.01:0.8

<table>
    <tr>
        <td><center><img src="http://download.kezhi.tech/img/20200417140757.png">p1</center></td>
        <td><center><img src="http://download.kezhi.tech/img/20200417140731.png">p2</center></td>
        <td><center><img src="http://download.kezhi.tech/img/20200417140827.png">p3</center></td>
    </tr>
</table>
