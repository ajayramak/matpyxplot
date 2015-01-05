from matpyxplot import plt
import numpy as np
import math

t = np.linspace(0, 5, 100)
PI = math.pi

canvas = plt.Canvas()

g1 = plt.Graph(width=8)
g1.plot(t, np.sin(2 * PI * t), c='r', ls='-', title=r"$V_1$")
g1.plot(t, np.sin(2 * PI * (t - 0.25)), c='g', ls=':', title=r"$V_2$")
g1.plot(t, np.sin(2 * PI * (t + 0.25)), c='b', ls='.-', title=r"$V_3$")
g1.showLegend('tr')
g1.setXAxisParams(label='time(s)')
g1.setYAxisParams(label='Voltage(V)', min=-1.5, max=3.5)

g2 = plt.Graph(width=8)
g2.plot(t, np.cos(2 * PI * t), c='r', m='o')
g2.setXAxisParams(label='time t(s)')
g2.setYAxisParams(label=r'$\cos{2\pi t}$', min=-2, max=2)

t1 = np.linspace(0, 5, 20)
g3 = plt.Graph(width=8)
g3.plot(t1, np.exp(-t1/2), c='b', m='s', mfc='r')
g3.setXAxisParams(label='time t(s)')
g3.setYAxisParams(label=r'$\exp{-t/2}$')


g4 = plt.Graph(width=8)
g4.plot(t, np.log(1 + t))
g4.setXAxisParams(label='time t(s)')
g4.setYAxisParams(label=r'$\log{(1 + t)}$')


margin = 2
canvas.addGraph(g1)
canvas.addGraphRightOf(g2, g1, margin)
canvas.addGraphBelowOf(g3, g1, margin)
canvas.addGraphRightOf(g4, g3, margin)

canvas.writeEPS('example.eps')
canvas.writePDF('example.pdf')
# canvas.writeAndOpen('example.pdf')