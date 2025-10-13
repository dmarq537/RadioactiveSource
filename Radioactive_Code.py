import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import csv


with open('Data_t=550.csv', mode='r') as file:
    reader = csv.DictReader(file)

    # Empty lists to store column values
    time = np.array([])
    output_1 = np.array([])
    output_2 = np.array([])
    output_3 = np.array([])
    output_4 = np.array([])

    # Iterating over each row
    for row in reader:
        time = np.append(time, int(row['Entry']))
        
        output_1  = np.append(output_1, int(row['Col2'])) #stores the data from each source in individual arrays
        output_2  = np.append(output_2, int(row['Col3']))
        output_3  = np.append(output_3, int(row['Col4']))
        output_4  = np.append(output_4, int(row['Col5']))
        
    outputs = np.array([output_1, output_2,
                        output_3, output_4]) #stores them all in one large array, makes repeating the fit process easier in the future
    
#The general form of the function
def func(x,n,t,c):
    return n*np.e**(-t*x) + c # t = 1/tau, n = N_0, c = lower level

p0_guesses = np.array([[1,1],[1,1],
                       [1,1],[1,1]]) #the array of guesses we use for our curve fit function, adjust to get 

plt.close('all')
fig, axes = plt.subplots(2, 2, figsize=(12, 12))

for i,output in enumerate(outputs):
    popt = [0.3, 0.3, 0.3] 
    for k in range(1):
        popt, pcov = curve_fit(func, time, output, p0=[popt[0], popt[1], popt[2]]) # the first gives us the values for our two variables, the second is the error
    print("Source {}: \n N_o = {} \u00B1 {} \n \u03c4 = {} \u00B1 {} \n c = {} \u00B1 {}".format(i+1,
                                                                round(popt[0],3),round(np.sqrt(pcov[0,0]),3), 
                                                                round(1/popt[1],3), round(np.sqrt(pcov[1,1]),3), 
                                                                round(popt[2],3), round(pcov[2,2],3)))
    RMSE = 0
    for n in range(len(time)): #goes through v
        RMSE += (output[n] - func(time[n], *popt))**2

    RMSE = np.sqrt(RMSE/len(time))
    print("RMSE = {}". format(RMSE))
    
    first_term = 0 if i in (1, 2) else 1 #this if for indexing the graphs
    axes[first_term, (i + 1) % 2].plot(time, output, "b-",label='Recorded Data')
    axes[first_term, (i + 1) % 2].plot(time, func(time, *popt), 'r-', label = 'Fit curve' )
    axes[first_term, (i + 1) % 2].set_title("Source {}".format(i))
    plt.legend()
    plt.show()
