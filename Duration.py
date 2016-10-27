import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import csv


Raw_Data=open('Side1.csv', 'r')#these 3 lines in take the data file
content = Raw_Data.readlines()
Data=[]

for line in content[1:]:
    line = line.strip(',')  # this parses out the data, and gets rid of the commas
    line=line.strip('\r\n')
    data = line.split(',')
    Data.append(data)  # stores all the raw data in the Data variable

def column (matrix,i):
    return [row[i] for row in matrix]  #This function parses out columns

x=column(Data,0)
y=column(Data,1)  # parses out the time, the x, and the y column (voltage into separate arrays)
time=[]
volt=[]


for el in range (len(x)):
    time.append(float(x[el])) #floats all the times and voltages
    volt.append(float(y[el]))



plt.plot(time,volt,'-')  # PLOTS THE entire data run
plt.xlabel('time')
plt.ylabel('voltage')
plt.title('Full Data Run')
plt.axis()
plt.show()
def Range (duration_of_fit,time,voltage,fit_deg):   #input either 1 or 1/2 for fit degree
    sample_time=[]
    sample_volt=[]
    noise=[]

    for el in range(len(time)):
        if time[el] >= -.05 and time[el] < -.04:
            noise.append(voltage[el])
    avg_noise=np.mean(noise)
    std=np.std(noise)
    begin=avg_noise+(6*std)


    for el in range (len(time)-2):
        if voltage[el] >= begin and voltage[el+1]>= begin and voltage [el+2]>= begin:
            start=time[el]
            stop=time[el]+duration_of_fit
            break

    for el in range (len(time)):
        if time[el]>= start and time[el]< stop:
            sample_time.append(time[el])
            sample_volt.append(voltage[el])

    print (sample_time)[0]
    print (sample_time[len(sample_time)-1])
    return sample_time
    return sample_volt

Range(.02,time,volt,1)





