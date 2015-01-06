Welcome to Matpyxplot
=====================

What is it?
----------

Matpyxplot is a wrapper for pyx with a matplotlib-like syntax. Latex quality figures can be generated directly 
in PDF and EPS formats with simple code.
 
How to Use?
----------

Basic steps involved in creating figures are:

        from matpyxplot import plt
1. Create a canvas

        canvas = plt.Canvas(...)
        
2. Create 'floating' graphs
 
        g1 = plt.Graph(...)
         
3. Add plots to them

        g1.plot(....)
        
4. (optional) Specify axis parameters

        g1.setXAxisParams(...)
        g1.setXAxisParams(...)
        
5. (optional) Insert a legend

        g1.showLegend(....)
        
6. Arrange the graphs in the canvas

        canvas.addGraph(...) 
        canvas.addGraphBelowOf(...)
        canvas.addGraphRightOf(...)
        
7. Write the PDF/EPS file

        canvas.writePDF()
        canvas.writeEPS()
        

Limitations:
-----------

1. Cannot produce empty marker symbols(can be circumvented with specifying markerfacecolor to be white).
2. Logarithm axis are not supported as of now.
3. The set of possible colors, markers, line styles are limited.

        