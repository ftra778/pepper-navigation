import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation
import pandas as pd
import csv
import os
import argparse

def update(t):
    ax.cla()

    x1, y1, z1 = [LeftShoulder[0][t], -LeftShoulder[1][t], LeftShoulder[2][t]]
    x2, y2, z2 = [RightShoulder[0][t], -RightShoulder[1][t], RightShoulder[2][t]]
    x3, y3, z3 = [LeftElbow[0][t], -LeftElbow[1][t], LeftElbow[2][t]]
    x4, y4, z4 = [RightElbow[0][t], -RightElbow[1][t], RightElbow[2][t]]
    x5, y5, z5 = [LeftWrist[0][t], -LeftWrist[1][t], LeftWrist[2][t]]
    x6, y6, z6 = [RightWrist[0][t], -RightWrist[1][t], RightWrist[2][t]]
    x7, y7, z7 = [LeftHip[0][t], -LeftHip[1][t], LeftHip[2][t]]
    x8, y8, z8 = [RightHip[0][t], -RightHip[1][t], RightHip[2][t]]
    x9, y9, z9 = [LeftKnee[0][t], -LeftKnee[1][t], LeftKnee[2][t]]
    x10, y10, z10 = [RightKnee[0][t], -RightKnee[1][t], RightKnee[2][t]]
    x11, y11, z11 = [LeftAnkle[0][t], -LeftAnkle[1][t], LeftAnkle[2][t]]
    x12, y12, z12 = [RightAnkle[0][t], -RightAnkle[1][t], RightAnkle[2][t]]

    ax.scatter(x1, z1, y1, s = 100, marker = 'o')
    ax.scatter(x2, z2, y2, s = 100, marker = 'o')
    ax.scatter(x3, z3, y3, s = 100, marker = 'o')
    ax.scatter(x4, z4, y4, s = 100, marker = 'o')
    ax.scatter(x5, z5, y5, s = 100, marker = 'o')
    ax.scatter(x6, z6, y6, s = 100, marker = 'o')
    ax.scatter(x7, z7, y7, s = 100, marker = 'o')
    ax.scatter(x8, z8, y8, s = 100, marker = 'o')
    ax.scatter(x9, z9, y9, s = 100, marker = 'o')
    ax.scatter(x10, z10, y10, s = 100, marker = 'o')
    ax.scatter(x11, z11, y11, s = 100, marker = 'o')
    ax.scatter(x12, z12, y12, s = 100, marker = 'o')
    ax.plot([x1, x2], [z1, z2], [y1, y2], linestyle = '-', color='black')
    ax.plot([x1, x3], [z1, z3], [y1, y3], linestyle = '-', color='black')
    ax.plot([x1, x7], [z1, z7], [y1, y7], linestyle = '-', color='black')
    ax.plot([x3, x5], [z3, z5], [y3, y5], linestyle = '-', color='black')
    ax.plot([x7, x8], [z7, z8], [y7, y8], linestyle = '-', color='black')
    ax.plot([x2, x8], [z2, z8], [y2, y8], linestyle = '-', color='black')
    ax.plot([x2, x4], [z2, z4], [y2, y4], linestyle = '-', color='black')
    ax.plot([x4, x6], [z4, z6], [y4, y6], linestyle = '-', color='black')
    ax.plot([x7, x9], [z7, z9], [y7, y9], linestyle = '-', color='black')
    ax.plot([x8, x10], [z8, z10], [y8, y10], linestyle = '-', color='black')
    ax.plot([x9, x11], [z9, z11], [y9, y11], linestyle = '-', color='black')
    ax.plot([x10, x12], [z10, z12], [y10, y12], linestyle = '-', color='black')

    ax.set_xlim(0.8*min(x), 1.2*max(x))
    ax.set_ylim(-1.2*max(z), 1.2*max(z))
    ax.set_zlim(1.2*min(y), 0.8*max(y))

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, default=r"beckon",
                        help="Name of gesture")

    args = parser.parse_args()
    data = []
    x = []
    y = []
    z = []
    i = 0
    with open(os.path.expanduser("~") + r"/pepper-motion-mimicking/csv/scatter/" + args.name + r"_coordinates.csv", 'r', newline='') as f:
        w = csv.reader(f, delimiter=',', quotechar='|')
        for row in w:
            if(i % 4 != 0):
                data.append([float(x) for x in row[1:]])
                
                # Collect all x, y, and z values to determine axis width, height, and depth
                if(i % 4 == 1):
                    x.extend([float(x) for x in row[1:]])
                elif(i % 4 == 2):
                    y.extend([-float(x) for x in row[1:]])
                elif(i % 4 == 3):
                    z.extend([float(x) for x in row[1:]])
            i = i + 1
    
    LeftShoulder = data[:3]
    RightShoulder = data[3:6]
    LeftElbow = data[6:9]
    RightElbow = data[9:12]
    LeftWrist = data[12:15]
    RightWrist = data[15:18]
    LeftHip = data[18:21]
    RightHip = data[21:24]
    LeftKnee = data[24:27]
    RightKnee = data[27:30]
    LeftAnkle = data[30:33]
    RightAnkle = data[33:36]
    
    fig = plt.figure(dpi=100)
    fig.suptitle(args.name + " Gesture", fontsize=14) 
    ax = fig.add_subplot(projection='3d')
    ani = matplotlib.animation.FuncAnimation(fig = fig, func = update, frames = len(data[0]), interval = 10)
    plt.show()
    
    writervideo = matplotlib.animation.FFMpegWriter(fps=30) 
    ani.save(os.path.expanduser("~") + r"/pepper-motion-mimicking/videos/scatter-plots/" + args.name + r"_scatter.mp4", writer=writervideo) 
    plt.close() 