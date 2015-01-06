# Ajayrama Kumaraswamy, 6th Jan 2015

import pyx
import subprocess
import math

goldenMean = (1 + math.sqrt(5))/2

class Graph(object):

    _colMap = {
                'b' : pyx.color.rgb.blue,
                'r' : pyx.color.rgb.red,
                'g' : pyx.color.rgb.green,
                'm' : pyx.color.cmyk.Magenta,
                'y' : pyx.color.cmyk.Yellow,
                'k' : pyx.color.gray.black,
                }

    _lsMap = {
                '-'     :    pyx.style.linestyle.solid,
                '--'    :    pyx.style.linestyle.dashed,
                ':'     :   pyx.style.linestyle.dotted,
                '.-'    :   pyx.style.linestyle.dashdotted,
    }

    _mMap = {
                'o' : pyx.graph.style.symbol.circle,
                'x' : pyx.graph.style.symbol.cross,
                '^' : pyx.graph.style.symbol.triangle,
                'd' : pyx.graph.style.symbol.diamond,
                's' : pyx.graph.style.symbol.square,
                '+' : pyx.graph.style.symbol.plus,
    }


    def __init__(self, width=None, height=None, ratio=goldenMean):

        '''

        Either widht or height must be specified.

        :param width: width of graph in cm
        :param height: height of graph in cm
        :param ratio: widht/height
        :return: graph object
        '''

        assert width is not None or height is not None, 'Either height or width must be specified'

        if width is not None and height is not None:

            assert ratio == width / height, 'Ratio is not width/height'

        if height is None:

            self.width = width
            self.height = width / ratio

        if width is None:

            self.height = height
            self.width = height * ratio


        self.plots = []
        self.xpos = 0
        self.ypos = 0
        self.plots = []
        self.datas = []
        self.styles = []
        self.xAxis = None
        self.yAxis = None
        self.drawLegend = False


    def setXAxisParams(self, type='linear', label=None, manualTicks=[], min=None, max=None):

        '''

        :param type: The type of the axis. 'linear' or 'log'. Only 'linear' supported
        :param label: axis label
        :param manualTicks: axis manual ticks, Will override autmatically generated ones.
        :param min: axis lower limit
        :param max: axis upper limit
        :return:
        '''

        if type == 'linear':

            self.xAxis = pyx.graph.axis.axis.linear(
                                                    min = min,
                                                    max = max,
                                                    title = label,
                                                    manualticks = manualTicks
                                                   )

        else:
            raise(NotImplementedError())

    def setYAxisParams(self, type='linear', label=None, manualTicks=[], min=None, max=None):

        '''

        :param type: The type of the axis. 'linear' or 'log'. Only 'linear' supported
        :param label: axis label
        :param manualTicks: axis manual ticks, Will override autmatically generated ones.
        :param min: axis lower limit
        :param max: axis upper limit
        :return:
        '''

        if type == 'linear':

            self.yAxis = pyx.graph.axis.axis.linear(
                                                    min = min,
                                                    max = max,
                                                    title = label,
                                                    manualticks = manualTicks
                                                   )

        else:
            raise(NotImplementedError())

    def showLegend(self, pos='tr'):

        '''
        Insert a legend
        :param pos: Specify where to place the legend. 'tr' for top right and 'bl' for lower bottom
        :return:
        '''

        self.drawLegend = True
        self.legendPos = pos

    def plot(self, x, y, c='b', ls='-', m='None', mfc='None', title=''):

        '''

        :param x: iterable containing x axis values of the points
        :param y: iterable containing y axis values of the points
        :param c: string specifying color. One of {'r', 'g', 'b', 'k', 'm', 'y', }
        :param ls: string specifying line style. '-'(continous), ':'(dotted), '--'(dashed), '.-'(dot-dash)
        :param m: string specifiying marker. 's'(square), 'o'(circle), 'd'(diamond), 'x'(crosss), '+'(plus), '^'(upright triangle)
        :param mfc: string specifiying marker face color. Same as param c
        :param title: tag string to use in legend.
        :return:
        '''

        self.datas.append(pyx.graph.data.values(x=x, y=y, title=title))

        style = []


        if not ls == 'None':

            style.append(pyx.graph.style.line([self._lsMap[ls], self._colMap[c]]))

        if not m == 'None':

            if mfc == 'None':

                mfc = c


            symbol = pyx.graph.style.symbol(symbol=self._mMap[m],
                                            symbolattrs=[pyx.deco.stroked.clear,
                                                         pyx.deco.filled([self._colMap[mfc]])])
            style.append(symbol)

        self.styles.append(style)


    def draw(self):

        '''
        Draws the graph using pyx
        :return:
        '''

        args = dict(width=self.width,
                                  height=self.height,
                                  xpos=self.xpos,
                                  ypos=self.ypos)

        if self.xAxis is not None:

            args['x'] = self.xAxis

        if self.yAxis is not None:

            args['y'] = self.yAxis

        if self.drawLegend:

            args['key'] = pyx.graph.key.key(pos=self.legendPos)

        g = pyx.graph.graphxy(**args)

        for data, style in zip(self.datas, self.styles):

            g.plot(data, style)

        return g



class Canvas(object):

    def __init__(self):

        self.canvas = pyx.canvas.canvas()
        self.graphs = []
        self.drawn = False

    def addGraph(self, graph, xpos=0, ypos=0):
        '''
        Add a graph to the canvas. The graph is placed at (0, 0) of the canvas
        :param graph: a Graph object.
        :param xpos: xpos of the lower bottom corner of the graph in the canvas
        :param ypos: ypos of the lower bottom corner of the graph in the canvas
        :return:
        '''

        graph.xpos = xpos
        graph.ypos = ypos
        self.graphs.append(graph)


    def addGraphBelowOf(self, graphToAdd, refGraph, distance=1):

        '''
        Add a graph to the canvas below an already added graph
        :param graphToAdd: Graph object
        :param refGraph: Graph Object
        :param distance: vertical distance between graphToAdd and refGraph in cm
        :return:
        '''

        graphToAdd.xpos = refGraph.xpos
        graphToAdd.ypos = refGraph.ypos - graphToAdd.height - distance
        self.graphs.append(graphToAdd)

    def addGraphRightOf(self, graphToAdd, refGraph, distance=1):

        '''
        Add a graph to the canvas to the right of an already added graph
        :param graphToAdd: Graph Object
        :param refGraph: Graph Object
        :param distance: horizontal distance between graphToAdd and refGraph in cm
        :return:
        '''

        graphToAdd.ypos = refGraph.ypos
        graphToAdd.xpos = refGraph.xpos + graphToAdd.width + distance
        self.graphs.append(graphToAdd)

    def draw(self):

        '''
        Draws the canvas and it's graphs in pyx
        :return:
        '''

        if len(self.graphs) == 0:
            raise(AttributeError('Please add a few graphs to the canvas using addGraph...() funcs'))

        self.drawn = True
        for graph in self.graphs:

            g = graph.draw()
            self.canvas.insert(g)



    def writeAndOpen(self, fName):

        '''
        Writes PDF and opens with evince. Works only in linux.
        :param fName: filename of the output PDF file.
        :return:
        '''

        if not self.drawn:
            self.draw()
        self.canvas.writePDFfile(fName)
        subprocess.Popen(['evince', fName])


    def writePDF(self, fName):

        '''
        Writes PDF.
        :param fName: filename of the output PDF file.
        :return:
        '''

        if not self.drawn:
            self.draw()

        self.canvas.writePDFfile(fName)

    def writeEPS(self, fName):

        '''
        Writes EPS.
        :param fName: filename of the output EPS file.
        :return:
        '''

        if not self.drawn:
            self.draw()

        self.canvas.writeEPSfile(fName)





















