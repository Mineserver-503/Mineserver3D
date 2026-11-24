# Mineserver3D v1.0.0.20261122_alpha Made by Mineserver

import tkinter
import math

import lib.tensor as tensor
import lib.quaternion as quaternion
import lib.geometry as geometry
import lib.display as display

Graphics1 = [
    geometry.Vector([2, 0, 0], [-1, 1, 1]),
    geometry.Vector([2, 0, 0], [-1, -1, 1]),
    geometry.Vector([2, 0, 0], [-1, -1, -1]),
    geometry.Vector([2, 0, 0], [-1, 1, -1]),
    geometry.Vector([0, 2, 0], [1, -1, 1]),
    geometry.Vector([0, 2, 0], [-1, -1, 1]),
    geometry.Vector([0, 2, 0], [-1, -1, -1]),
    geometry.Vector([0, 2, 0], [1, -1, -1]),
    geometry.Vector([0, 0, 2], [1, 1, -1]),
    geometry.Vector([0, 0, 2], [-1, 1, -1]),
    geometry.Vector([0, 0, 2], [-1, -1, -1]),
    geometry.Vector([0, 0, 2], [1, -1, -1]),
]
G = Graphics1

GUI = tkinter.Tk()

test_Camera = display.Camera(
    mode="persp",
    fov=math.pi / 3,
    aspect=GUI.maxsize()[0] / GUI.maxsize()[1],
    near=0.05,
    far=100,
    eye=geometry.Vector([-2,-1.5,-2.5],[2,1.5,2.5]),
)

pro_Graphics = []
for v in range(len(G)):
    if display.pro(G[v], test_Camera) != None:
        pro_Graphics.append(display.pro(G[v], test_Camera))

GUI.title("Mineserver3D")
GUI.iconbitmap("logo.ico")
GUI.geometry(
    str(int(GUI.maxsize()[0] / 2))
    + "x"
    + str(int(GUI.maxsize()[1] / 2))
    + "+"
    + str(int(GUI.maxsize()[0] / 4))
    + "+"
    + str(int(GUI.maxsize()[1] / 4))
)
GUI.resizable(width=None, height=None)
GUI.config(bg="#3D3D3D")
V_Brush = tkinter.Canvas(
    GUI, width=GUI.maxsize()[0], height=GUI.maxsize()[1], bg="#000000"
)
V_Brush.pack()
for t in range(len(pro_Graphics)):
    V_Brush.create_line(
        GUI.maxsize()[0] / 4 + GUI.maxsize()[0] / 4 * pro_Graphics[t][0][0],
        GUI.maxsize()[1] / 4 - GUI.maxsize()[1] / 4 * pro_Graphics[t][0][1],
        GUI.maxsize()[0] / 4 + GUI.maxsize()[0] / 4 * pro_Graphics[t][1][0],
        GUI.maxsize()[1] / 4 - GUI.maxsize()[1] / 4 * pro_Graphics[t][1][1],
        fill="#FF0000",
        width=0.1,
    )

GUI.mainloop()
