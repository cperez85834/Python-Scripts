#The purpose of this script is to provide a proof of concept for plotting two different
#sets of data with asynchronous sampling time on the same graph. This would be useful
#if you want to compare data from two different sensors on the same graph, each with
#unique axes. The actual result looks a little bit weird simply because plotting two changing graphs
#in the same axes can be confusing


import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

data = [0, 0]
ln2Wait = time.time()
Samples1 = 0
Samples2 = 0

xLimMax = 6
xLimMin = 0

yLimMax = 5
yLimMin = 0

#Setup information for the first graph
#Line 1 information
xData, yData = [], []
fig, ax = plt.subplots()
color = 'tab:blue'
ax.set_xlabel('Samples (x100 samples)', color = color)
ax.grid(True)
ax.set_ylabel('Force (N)', color = color)
ax.tick_params(axis='x', labelcolor=color)
ax.tick_params(axis='y', labelcolor=color)
ax.tick_params(which='minor', length=4)

ln, = plt.plot(xData, yData)
plt.grid()
ln.set_color(color)

xLimMax2 = 10
xLimMin2 = 0

yLimMax2 = 7
yLimMin2 = 0

#Setup information for the second graph             
#Line 2 information
color = 'tab:red'
xData2, yData2 = [], []
ax2 = fig.add_subplot()

ax2.set_xlabel('Samples (x100 samples)', color = color)
ax2.xaxis.tick_top()
ax2.xaxis.set_label_position('top')
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position('right')
ax2.set_ylabel('Extension (mm)', color = color)
ax2.tick_params(axis='x', labelcolor=color)
ax2.tick_params(axis='y', labelcolor=color)

ln2, = plt.plot(xData2, yData2)
ln2.set_color(color)

def getData():
    data[0] = data[0] + .01

def getData2():
    data[1] = data[1] + .05

#The following function simulates data input for the first graph
def inputFunc(x):
    return np.exp(x/10)

#The following function simulates data input for the second graph
#and includes a built in delay to simulate a different sampling rate
def inputFunc2(x): #Data to simulate
    global ln2Wait
    ln2Elapsed = time.time()

    if(ln2Elapsed - ln2Wait) >= .07:
        ln2Wait = time.time()
        return np.exp(x/12)

    else:
        return None

#initialization function
def init():
    global xLimMax, xLimMin
    global yLimMax, yLimMin
    global xLimMax2, xLimMin2
    global yLimMax2, yLimMin2
    ax.set_xlim(xLimMin, xLimMax)
    ax.set_ylim(yLimMin, yLimMax)
    ax2.set_xlim(xLimMin2, xLimMax2)
    ax2.set_ylim(yLimMin2, yLimMax2)
    return ln, ln2,

#One function updates both graphs each frame
def update1(i, frame, frame2):
    getData()
    global xLimMax, xLimMin, end, Samples1, Samples2
    global yLimMax, yLimMin
    global xLimMax2, xLimMin2
    global yLimMax2, yLimMin2
    
    xNew = frame
    yNew = inputFunc(frame)
    
    xData.append(xNew)
    yData.append(yNew)

    if xNew > xLimMax:
        xLimMax *= 1.15
        ax.set_xlim(1, xLimMax)
        plt.draw()

    if yNew > yLimMax:
        yLimMax *= 1.15
        ax.set_ylim(0, yLimMax)
        plt.draw()

    xNew2 = frame2
    yNew2 = inputFunc2(frame2)

    if yNew2 is not None:
        getData2()
        xData2.append(xNew2)
        yData2.append(yNew2)

        if xNew2 > xLimMax2:
            xLimMax2 *= 1.15
            ax2.set_xlim(1, xLimMax2)
            plt.draw()

        if yNew2 > yLimMax2:
            yLimMax2 *= 1.15
            ax2.set_ylim(0, yLimMax2)
            plt.draw()

        ln2.set_data(xData2, yData2)
        Samples2 += 1
        
    ln.set_data(xData, yData)
    Samples1 += 1
    end = time.time()
    return ln, ln2,

def update2(frame):
    global xLimMax2, xLimMin2, end
    global yLimMax2, yLimMin2
    
    xNew = frame + 0.5
    yNew = inputFunc2(frame)
    
    xData2.append(xNew)
    yData2.append(yNew)

    if xNew > xLimMax2:
        xLimMax2 *= 1.15
        ax2.set_xlim(1, xLimMax2)
        plt.draw()

    if yNew > yLimMax2:
        yLimMax2 *= 1.15
        ax2.set_ylim(0, yLimMax2)
        plt.draw()

    ln2.set_data(xData2, yData2)
    return ln2,


init()

start = time.time()
end = time.time()


ani = FuncAnimation(fig, update1,
                    init_func=init, fargs=data, interval=0, blit=True, repeat=False)

plt.show()

while True:
    print('time taken: ' + str(end - start))
    print('Line 1 samples/sec: ' + str(Samples1 / (end - start)))
    print('Line 2 samples/sec: ' + str(Samples2 / (end - start)))
    time.sleep(1)
