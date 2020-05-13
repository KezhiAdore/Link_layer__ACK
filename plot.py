from matplotlib import pyplot as plt
import pandas as pd

p=["0.01","0.05","0.1"]
plt.cla()
for i in p:
    data=pd.read_csv("p2_time"+i+".csv")
    tmp=data[0:80]
    plt.plot(tmp["precentage"],tmp["time"])
    # plt.savefig("p"+str(j+1)+"_time"+i+".png")
plt.show()
