import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
import csv


Raw_Data=open('sphere_1.csv', 'r')#these 3 lines in take the data file
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
    time.append(float(x[el])) #floats all the times and voltages  saves them in time and voltage arrays
    volt.append(float(y[el]))



plt.plot(time,volt,'-')  # PLOTS THE entire data run
plt.xlabel('time')
plt.ylabel('voltage')
plt.title('Full Data Run')
plt.axis()
plt.show()
def Range (duration_of_fit,time,voltage,fit_deg):   #input either 1 or 1/2 for fit degree  data cutting function.
    sample_time=[]
    sample_volt=[]
    noise=[]

    for el in range(len(time)):  #This loop loops through full data run and takes out all of the voltage data in specified time chunk before data run.
        if time[el] >= -.05 and time[el] < -.04:
            noise.append(voltage[el])
    avg_noise=np.mean(noise)   #This averages the voltages before the data run so that we can have an average noice level of voltage before the run.
    std=np.std(noise)  #finds the std dev. of that run.
    begin=avg_noise+(6*std)   #the begin variable corresponds to the voltage threshold that is 6 standard deviations above the average noise level.


    for el in range (len(time)-2):
        if voltage[el] >= begin and voltage[el+1]>= begin and voltage [el+2]>= begin:  #this loops through full data and checks for three consecutive voltage readings that are greater than begin.
            start=time[el]  #once this condition is met, then the corresponding time element is our starting time for the data run.
            stop=time[el]+duration_of_fit #this once the starting time is specified, then the stop time is found by adding the user specified duration of the fit parameter.
            break

    for el in range (len(time)):
        if time[el]>= start and time[el]< stop:
            sample_time.append(time[el])    # the sample times and sample voltaged from the above time chunck are saved in arrays.
            sample_volt.append(voltage[el])

    if sample_time[0] < 0:  #if the first x value is negitive, this loop shifts all the x values by the amount that makes the first value zero.  This is so that square root fits can be preformed.
        for el in range(len(sample_time)):
            sample_time[el]= sample_time[el]+abs(sample_time[0])
    print sample_time[0]  #prints the begining and ending time element being used.  these should both be positive.
    print sample_time[len(sample_time)-1]


    negitive_sample_volts = [ -y for y in sample_volt]  #this flips all the voltages so that a decrease in voltage corresponds to a decrease in temp. (more intuititive)

    if fit_deg == 1:
        linear_fit_values=[(np.polyfit(sample_time,negitive_sample_volts,1)[0])*x +(np.polyfit(sample_time,negitive_sample_volts,1)[1]) for x in sample_time]
        slope, intercept, r_value, p_value, std_err = stats.linregress(sample_time,negitive_sample_volts)  #calculates slope, int, and r value using sci pi stats, consider using this instead of np polyfit.
        #Linear fit values uses poly fit to change all the voltage values to linear_fit_values= m*x+b.  To be plotted in fit.
        r_squared= r_value*r_value


        plt.plot(sample_time,negitive_sample_volts,'-',sample_time,linear_fit_values,'-')  # plots the sampled portion of data witht the fit.
        plt.xlabel('time')
        plt.ylabel('voltage')
        plt.title('Sample of Data Run')
        plt.axis()
        plt.show()
        print "The linear Regression has the form y=", (np.polyfit(sample_time,negitive_sample_volts,1)[0]) , "x +" ,(np.polyfit(sample_time,negitive_sample_volts,1)[1]) , " With an r^2 value of " , r_squared


    if fit_deg == .5:   #wont work becasue there is still negitive values in sample_time
        def func (x,a,b):
            return a*np.power(x,1)+b


        for el in range(len(sample_time)):
            if sample_time[el]<0:
                print sample_time[el]
    popt, pcov= curve_fit(func, sample_time, negitive_sample_volts)

    print popt

    return sample_time
    return sample_volt

Range(.02,time,volt,.5)


