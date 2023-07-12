from tkinter import *
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from quadtree import Point, Rect, QuadTree
import tkinter as tk

# Top level window or the first window
frame = Tk()
frame.title("Enter location")
frame.geometry('500x320')
lbl = tk.Label(frame, text = "")
lbl2 = tk.Label(frame, text = "")

DPI = 100
np.random.seed()

width, height = 360, 180
N = 700


coords = np.random.randn(N, 2) * height/3 + (width/2, height/2)
points = [Point(*coord) for coord in coords]

domain = Rect(width/2, height/2, width, height)
qtree = QuadTree(domain, 1)
for point in points:
    qtree.insert(point)


fig = plt.figure(figsize=(700/DPI, 500/DPI), dpi=DPI)
ax = plt.subplot()
ax.set_xlim(0, width)
ax.set_ylim(0, height)

# this reads the image and then prints it
img = plt.imread("worldmap.jpg")
ax.imshow(img, extent=[360, 38,160,10])
qtree.draw(ax)

ax.scatter([p.x for p in points], [p.y for p in points], s=4)
ax.set_xticks([])
ax.set_yticks([])

# Second window 
def openWindow():
    frame2 =Toplevel()
    frame2.title("Car Option")
    frame2.geometry('800x760')

    radius = 0.0
    found_points = []
    distance = []
    distanceArray = np.array(distance, dtype=np.float32)

    userXLocation = float(choice1.get())
    xCalculation   = userXLocation
    userXLocation = userXLocation + 180

    userYLocation = float(choice2.get())
    yCalculation  = userYLocation
    if userYLocation < 0:
        userYLocation = (userYLocation * -1) + 90
    else:
        userYLocation = 90 - userYLocation

    centre = [userXLocation, userYLocation]

    # this finds the nearest five points and the nearest point is the last in the lists.
    while len(found_points) != 5:
        radius += 0.1
        found_points = []
        qtree.query_radius(centre, radius, found_points)

    # this takes all the points and saparates them into x and y points
    foundXPoints = [p.x for p in found_points]
    foundYPoints = [p.y for p in found_points]

    # this is the average of the distances of one degree to one mile times the difference inbetween the points
    for i in range(5):
        distanceArray = np.append(distanceArray, 61.8 * QuadTree.true_coors(foundXPoints[i], foundYPoints[i], xCalculation  , yCalculation ))
    # this draws the points on the map
    ax.scatter([userXLocation for p in centre], [userYLocation for p in centre],
               facecolors='r', edgecolors='r', s=10)
    ax.scatter([p.x for p in found_points], [p.y for p in found_points],
               facecolors='b', edgecolors='b', s=10)
    ax.scatter([foundXPoints for p in distanceArray], [foundYPoints for p in distanceArray],
               facecolors='g', edgecolors='g', s=25)
    Rect(*centre, 2 * radius, 2 * radius).draw(ax, c='g')
    canvas = FigureCanvasTkAgg(fig, master=frame2)
    canvas.draw()

    toolbar = NavigationToolbar2Tk(canvas, frame2)
    toolbar.update()

    # placing the patplotlib on the Tkinter window
    canvas.get_tk_widget().pack()

    lbl = tk.Label(frame2, text = "")

    ax.invert_yaxis()
    plt.tight_layout()

    lbl.config(text='Which driver would you prefer to come:\n' + "For Option One, type 1, it is " + str('{:.2f}'.format(distanceArray[0])) + "miles away\n" +
     "For Option two, type 2, it is " + str('{:.2f}'.format(distanceArray[1])) + "miles away\n" +
    "For Option three, type 3, it is " + str('{:.2f}'.format(distanceArray[2])) + "miles away\n" +
    "For Option four, type 4, it is " + str('{:.2f}'.format(distanceArray[3])) + "miles away\n" +
    "For Option five, type 5, it is " + str('{:.2f}'.format(distanceArray[4])) + "miles away\n Enter selection below ")

    def printInput():
        inputtxt=QuadTree.switch(int(choice.get(1.0, "end-1c")))
        lbl.config(text = inputtxt)

    lbl.pack()

    choice = tk.Text(frame2, height = 1, width = 1)
    choice.pack()
    printButton = tk.Button(frame2, text = "Select", command = printInput)

    printButton.pack(pady=10)
    exitButton = tk.Button(frame2, text="Quit", command=frame2.destroy)
    exitButton.pack(pady=10)


lbl2.config(text = "Enter your Longitude: ")
choice1 = Entry(frame, width= 40)

lbl.config(text = "Enter your Latitude: ")
choice2 = Entry(frame, width= 40)

exitButton = tk.Button(frame, text="Quit", command = frame.quit)
createMap = tk.Button(frame, text="Show Nearest Rides", command = openWindow)

lbl2.pack(pady=10)
choice1.pack(pady=10)
lbl.pack(pady=10)
choice2.pack(pady=10)
createMap.pack(pady=30)
exitButton.pack()
frame.mainloop()