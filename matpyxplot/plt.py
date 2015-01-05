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


    def __init__(self, xpos=0, ypos=0, width=None, height=None, ratio=goldenMean, legend=None):

        assert width is not None or height is not None, 'Either height or width must be specified'

        if height is None:

            self.width = width
            self.height = width / ratio

        if width is None:

            self.height = height
            self.width = height * ratio


        self.plots = []
        self.xpos = xpos
        self.ypos = ypos
        self.legend = legend
        self.plots = []
        self.datas = []
        self.styles = []
        self.xAxis = None
        self.yAxis = None
        self.drawLegend = False


    def setXAxisParams(self, type='linear', label=None, manualTicks=[], min=None, max=None):

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

        self.drawLegend = True
        self.legendPos = pos

    def plot(self, x, y, c='b', ls='-', m='None', mfc='None', title=''):

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

    def addGraph(self, graph):
        self.graphs.append(graph)


    def addGraphBelowOf(self, graphToAdd, refGraph, distance=1):

        graphToAdd.xpos = refGraph.xpos
        graphToAdd.ypos = refGraph.ypos - graphToAdd.height - distance
        self.graphs.append(graphToAdd)

    def addGraphRightOf(self, graphToAdd, refGraph, distance=1):

        graphToAdd.ypos = refGraph.ypos
        graphToAdd.xpos = refGraph.xpos + graphToAdd.width + distance
        self.graphs.append(graphToAdd)

    def draw(self):

        if len(self.graphs) == 0:
            raise(AttributeError('Please add a few graphs to the canvas using addGraph...() funcs'))

        self.drawn = True
        for graph in self.graphs:

            g = graph.draw()
            self.canvas.insert(g)



    def writeAndOpen(self, fName):

        if not self.drawn:
            self.draw()
        self.canvas.writePDFfile(fName)
        subprocess.Popen(['evince', fName])


    def writePDF(self, fName):

        if not self.drawn:
            self.draw()

        self.canvas.writePDFfile(fName)

    def writeEPS(self, fName):

        if not self.drawn:
            self.draw()

        self.canvas.writeEPSfile(fName)





















