from DEgraphics import *
import math as m
import sys
import time
import cmath as cm
from random import random
from NLDUtils import *

'''
    Name: Ethan Leifer
    File: EthanLeiferMSetExplorer.py
'''
SIZE = 400

MSetWin = DEGraphWin(title="Mandelbrot Set Dispaly", width=SIZE, height=SIZE, defCoords=[-2, -2, 2, 2])
JSetWin = DEGraphWin(title="Julia Set Display", width=SIZE, height=SIZE, defCoords=[-2, -2, 2, 2])

autoClear = True
cos = False

def f(z, c):
    """"Quadratic Map with veritcal shift c"""
    return z * z + c

def inverseQMap(z, c):
    """returns a randomly choosen positve or negative root of the quadratic map"""
    x = cm.sqrt(z - c)
    # randomizes postive or negative root
    if random() > .5:
        x *= -1
    return x

def inverseQMapBoth(z, c):
    """ retuns both positve and negative root of the inverse of the quadratic map"""
    x = cm.sqrt(z - c)
    return [x, -1 * x]

def inMset(c, maxIters, maxRadius):
    """returns a (true if z is inside Mandelbrot set and False otherwise, the amount of iterations it took to get there)"""
    # intialize z0 = 0
    z0 = complex(0, 0)
    # intialize numIterations to 0
    numIters = 0
    # while numIters < maxIters AND |z0| < escR
    while numIters < maxIters and abs(z0) < maxRadius:
        # iterate once
        z0 = f(z0, c)
        numIters += 1
    # if numIters < maxIters then c is in the Mset
    return (not(numIters < maxIters), numIters)

def inFilledJSet(z, c, maxIters, maxRadius):
    """returns a tuple (true if z is inside Closed Julia set and False otherwise, the amount of iterations it took to get there)"""
    # amount of times z has been iterated
    numIters = 0
    # if z is less than maxRadius and numIters is less than maxIters
    while numIters < maxIters and abs(z) < maxRadius:
        # iterate z
        z = f(z, c)
        numIters += 1
    # return if numIters < maxIters and numIters
    return (not(numIters < maxIters), numIters)

def getColor(numIters, maxIters):
    '''gets grayscale for MSet or JSet'''
    # if else statement lets user choose between two transformations
    if cos:
        # puts maps numIters/maxIters into the cos function
        shade = (255 * numIters / maxIters)
        shade = int(255 * abs(m.cos(shade)))

    else:
        shade = int(150 - (maxIters - numIters) / maxIters * 255)
        if shade < 0:  # because it can go negative makes it positve
            extra = shade % 100
            shade = (100 - extra)
        shade = 255 - shade
    return color_rgb(shade, shade, shade)

def plotMSet(maxIters, maxRadius, resolution, MSetColor):
    rowCount = 0
    # set horizontal and vertical stepsize
    hstep = resolution[0] * (MSetWin.currentCoords[2] - MSetWin.currentCoords[0]) / MSetWin.width
    vstep = resolution[1] * (MSetWin.currentCoords[3] - MSetWin.currentCoords[1]) / MSetWin.height

    # graphs a two toned mSet
    curReal = MSetWin.currentCoords[0]
    maxReal = MSetWin.currentCoords[2]
    maxImag = MSetWin.currentCoords[3]

    while curReal < maxReal:
        curImag = MSetWin.currentCoords[1]
        while curImag < maxImag:
            # check if the current pixel is in the Mset
            result = inMset(complex(curReal, curImag), maxIters, maxRadius)
            # if it is in the Mset plot the point according to the color
            if result[0]:
                MSetWin.plot(curReal, curImag, MSetColor)
            # otherwise color it according to the amount of iterations it took to escape
            else:
                MSetWin.plot(curReal, curImag, getColor(result[1], maxIters))
            curImag += vstep
        rowCount += 1
        # update window every 100 rows
        if rowCount % 50 == 0:
            MSetWin.update()
        curReal += hstep

def plotJSetInterior(c, maxIters, maxRadius, resolution, JSetColor):

    # ask user if they want to see just the interior, the escape iterations or two toned
    interior = False
    showDistance = False
    exterior = False
    option = getOption(['i', 'e', 't'], "'i' to see the interior colored\n'e' to see the escape iterations\n't' to see the exterior colored\n(After it runs through you can go back and add a different color scheme)")
    if option == 'i':
        interior = True
    if option == 'e':
        showDistance = True
    if option == 't':
        exterior = True

    # calculate step sizes
    hstep = resolution[0] * (JSetWin.currentCoords[2] - JSetWin.currentCoords[0]) / JSetWin.width
    vstep = resolution[1] * (JSetWin.currentCoords[3] - JSetWin.currentCoords[1]) / JSetWin.height

    # keeps track of rows so window is not plotting points everytime
    rowCount = 0

    # update every row by row
    x = JSetWin.currentCoords[0]
    xMax = JSetWin.currentCoords[2]
    yMax = JSetWin.currentCoords[3]
    while x < xMax:
        y = JSetWin.currentCoords[1]
        while y < yMax:
            # check if the current pixel is in JSet
            result = inFilledJSet(complex(x, y), c, maxIters, maxRadius)
            # plot results according to what the user wants
            if result[0]:
                if interior:
                    JSetWin.plot(x, y, JSetColor)
            else:
                if showDistance:
                    JSetWin.plot(x, y, getColor(result[1], maxIters))
                if exterior:
                    JSetWin.plot(x, y, JSetColor)
            y += vstep
        JSetWin.update()
        x += hstep
        # update rows every 100 rows
        rowCount += 1
        if rowCount % 50 == 0:
            MSetWin.update()

def plotJSetInverse(c, maxIters, maxRadius, JSetColor):
    """draws the J Set using the orginal inverse function (where yuo only go down one of the binary tree pairs for each level)"""
    # generate a random x0 value
    z = complex(random() * 10, random() * 10)

    # iterate through the inverse of Qmap it a large number of times
    # EXPLAINED: For the algorithm to work, you first must drive your z value that you just created towards the Julia set through a large number of iterations
    for i in range(100000):
        z = inverseQMap(z, c)

    # iterate through inverse of Qmap again but this time plot the iterations
    # EXPLAINED: Then iterate again to graph the Julia set
    for i in range(20000):
        JSetWin.plot(z.real, z.imag, JSetColor)
        z = inverseQMap(z, c)

def plotJSetNewInverse(c, maxIters, maxRadius, JSetColor):
    """draws a slower more accurate picture of a J Set"""
    # 1. Randomly create a z0 value
    z0 = complex(random() * 10, random() * 10)
    z = z0
    # 2.  Drive z value towards J Set by iterating
    TransIters = 100000
    for i in range(TransIters):
        z = inverseQMap(z, c)

    # iters is the number of levels deep of the binary tree, 15 is a happy medium
    iters = confirmOptionBetweenNum(type(1), [1, 30], "Please enter an integer for the number of levels deep you want to iterate through. The time it takes to grows expontially. Suggestion: 15")

    # 3. Make the set of all points on the border of the J Set. If you iterate on the J Set it moves the z point along the J Set, we then put that point in a set (after rounding to remove duplicate points)
    JSetPoints = makeJSetList(z, c, iters, 50)  # the last number (the amount of decimals you round too) has a smaller impact on speed so I hardcoded it
    print("This process is a little slow. Please wait. Thanks for understanding!")
    # 4. plot all of the points in the set
    for i in range(len(JSetPoints)):
        z = JSetPoints.pop()
        JSetWin.plot(z.real, z.imag, JSetColor)

def makeJSetList(z, c, iters, roundDigits):
    """ recursive function that creates a set of all of the numbers in the binary tree of the inverseQMap(z)"""
    if iters == 0:
        return inverseQMapBoth(z, c)
    else:
        # iterate z
        zBoth = inverseQMapBoth(z, c)
        # round both numbers
        zBoth = [complex(round(zBoth[0].real, roundDigits), round(zBoth[0].imag, roundDigits)), complex(round(zBoth[1].real, 5), round(zBoth[1].imag, 5))]
        # call makeJSetList again on the two z values and add them to the set
        return set(makeJSetList(zBoth[0], c, iters - 1, roundDigits)).union(makeJSetList(zBoth[1], c, iters - 1, roundDigits))

def zoom(MSetZoomed, JSetZoomed, c, maxItersM, maxItersJ, maxRadiusM, maxRadiusJ, resolutionM, resolutionJ, MSetColor, JSetColor, JSetAlgo):
    '''MSetZoomed and JSetZoomed are boolean values that keep track of if the two windows have been zoomed in
        It regraphs JSet and MSet so I have to pass in all of the coorelating values
    '''
    # values for getting option from user
    zoomGraphOptions = ['m', 'j']
    zoomGraphStatement = "'m' to change zoom on Mandelbrot set\n'j' to change zoom on Julia set"
    zoomOptions = ['in', 'out']
    zoomStatment = "'in' to zoom in\n'out' to zoom out (to default coordinates)"
    # get input from user
    graph = getOption(zoomGraphOptions, zoomGraphStatement)

    while not(graph == 'q'):

        # asks user to zoom in on Mandelbrot Set
        if graph == 'm':
            # if Mandlebrot Set has not been zoom in before only let user zoom in
            if not(MSetZoomed):
                print("You must zoom in first")
                MSetWin.zoom("in")

            # ask user if they want to zoom in
            else:
                if getOption(zoomOptions, zoomStatment) == 'in':
                    MSetWin.zoom("in")

                else:
                    MSetWin.zoom("out")
                    # you have zoomed in so change cooresponding variables

            MSetZoomed = not(MSetZoomed)

            # regraph window
            plotMSet(maxItersM, maxRadiusM, resolutionM, MSetColor)

        if graph == 'j':
            if not(JSetZoomed):
                print("You must zoom in first")
                JSetWin.zoom("in")
            else:
                if getOption(zoomOptions, zoomStatment) == 'in':
                    JSetWin.zoom("in")

                else:
                    JSetWin.zoom("out")
                    # you have zoomed in so change cooresponding variables

            JSetZoomed = not(JSetZoomed)

            graphJSet(c, JSetAlgo, maxItersJ, maxRadiusJ, resolutionJ, JSetColor)
        # make sure user is is done zooming
        if confirmOption(['y', 'n'], "Do you want to zoom again? ") == 'n':
            graph = 'q'
        # if not get new input
        else:
            graph = getOption(zoomGraphOptions, zoomGraphStatement)

    return [MSetZoomed, JSetZoomed]

def getCValue(maxIters, maxRadius):
    # returns a c value that is chosen from the Mandelbrot set diagram
    if getOption(['c', 'e'], "Enter 'c' to click your own c value from Mandlebrot set or 'e' to enter your own text value") == 'c':
        print("Please click on the Mandelbrot Set to choose your new C value")
        p = MSetWin.getMouse()
        c = complex(p.getX(), p.getY())
        print("You have clicked the point " + str(c))
    else:
        real = input("Please enter the real portion of your c value: ")
        while not(isValid(type(1.0), real)):
            real = input("INVALID! Please enter the real portion of your c value: ")
        imag = input("Please enter the imaginary portion of your c value: ")
        while not(isValid(type(1.0), imag)):
            imag = input("INVALID! Please enter the imaginary portion of your c value: ")

        c = complex(float(real), float(imag))
        print("You have entered the point " + str(c))

    return c

def chooseJSet():
    # let user choose which Jset to be redraw on JSetWin
    options = ['1', '2', '3', '4']
    statement = "Please select the Julia Set you would like to draw:\n\n'1' to draw the J set using a brute force algorithm\n'2' to draw the J set using the orginal inverse algorithm\n'3' to draw the J set using the updated inverse algorithm"
    return getOption(options, statement)

def graphJSet(c, JSetAlgo, maxItersJ, maxRadiusJ, resolution, JSetColor):
    # manages redrawing of julia sets
    JSetAlgoDict = {'1': "brute force algorithm", '2': "orginal inverse algorithm", '3': "modifed inverse algorithm"}

    print("You have currently chosen the " + JSetAlgoDict[JSetAlgo])

    # let user change Julia Set algorithm if desired
    if getOption(['y', 'n'], "Would you like to change your Julia set algorithm? ('y' or 'n')") == 'y':
        JSetAlgo = chooseJSet()

    # lets user clear the window
    if autoClear:
        JSetWin.clear()
        print("The window has been automatically cleared (go back to main menu to change)")
    else:
        if getOption(['y', 'n'], "Would you like to clear the window before redrawing? ('y' or 'n')") == 'y':
            JSetWin.clear()
            print("The window has been cleared")

    if JSetAlgo == '1':
        plotJSetInterior(c, maxItersJ, maxRadiusJ, resolution, JSetColor)
    if JSetAlgo == '2':
        plotJSetInverse(c, maxItersJ, maxRadiusJ, JSetColor)
    if JSetAlgo == '3':
        plotJSetNewInverse(c, maxItersJ, maxRadiusJ, JSetColor)

    return JSetAlgo  # so the main function can keep track

def changeResolution(currentRes=[[1, 1], [1, 1]], firstTime=False):
    resJ = currentRes[0]
    resM = currentRes[1]
    if not(firstTime):
        resOption = getOption(['b', 'm', 'j'], "'b' to change both resolutions\n'm' to change just the Mandelbrot set's resolution\n'j' to change just the Julia set's resolution")
    else:
        resOption = '-1'

    if resOption == 'b' or firstTime:
        isMSet = True
        isJSet = True

    elif resOption == 'm':
        isMSet = True
        isJSet = False

    elif resOption == 'j':
        isMSet = False
        isJSet = True

    else:
        isJSet = False
        isMSet = False

    if isMSet:
        vM = input("Please enter a valid vertical resolution for the Mandelbrot Set: ")
        while not(isValid(type(1), vM)):
            vM = input("INVALID! Please enter a valid vertical resolution for the Mandelbrot Set: ")

        hM = input("Please enter a valid horizontal resolution for the Mandelbrot Set: ")
        while not(isValid(type(1), hM)):
            hM = input("INVALID! Please enter a valid horizontal resolution for the Mandelbrot Set: ")

        resM = [int(hM), int(vM)]

    if isJSet:
        vJ = input("Please enter a valid vertical resolution for the Julia Set: ")
        while not(isValid(type(1), vJ)):
            vJ = input("INVALID! Please enter a valid vertical resolution for the Julia Set: ")

        hJ = input("Please enter a valid horizontal resolution for the Julia Set: ")
        while not(isValid(type(1), hJ)):
            hJ = input("INVALID! Please enter a valid horizontal resolution for the Julia Set: ")

        resJ = [int(hJ), int(vJ)]

    return [resJ, resM]

def changeMaxIters(currentMaxIters=[50, 50], firstTime=False):
    J = currentMaxIters[0]
    M = currentMaxIters[1]
    if not(firstTime):
        ItersOption = getOption(['b', 'm', 'j'], "'b' to change both maximum iterations\n'm' to change just the Mandelbrot set's maximum iterations\n'j' to change just the Julia set's maximum iterations")
    else:
        ItersOption = '-1'

    if ItersOption == 'b' or firstTime:
        isMSet = True
        isJSet = True

    if ItersOption == 'm':
        isJSet = False
        isMSet = True

    if ItersOption == 'j':
        isJSet = True
        isMSet = False

    if isMSet:
        M = input("Please enter a valid maximum iterations for the Mandelbrot Set: ")
        while not(isValid(type(1), M)):
            M = input("INVALID! Please enter a valid maximum iterations for the Mandelbrot Set: ")

    if isJSet:
        J = input("Please enter a valid maximum iterations for the Julia Set: ")
        while not(isValid(type(1), J)):
            J = input("INVALID! Please enter a valid maximum iterations for the Julia Set: ")

    return [int(J), int(M)]

def changeMaxRadius(currentMaxRadius=[2, 2], firstTime=False):
    J = currentMaxRadius[0]
    M = currentMaxRadius[1]
    if not(firstTime):
        ItersOption = getOption(['b', 'm', 'j'], "'b' to change both sets maximum radius values\n'm' to change just the Mandelbrot set's max radius\n'j' to change just the Julia set's max radius")
    else:
        ItersOption = '-1'

    if ItersOption == 'b' or firstTime:
        isMSet = True
        isJSet = True

    if ItersOption == 'm':
        isJSet = False
        isMSet = True

    if ItersOption == 'j':
        isJSet = True
        isMSet = False

    if isMSet:
        M = input("Please enter a valid max radius for the Mandelbrot Set: ")
        while not(isValid(type(1), M)):
            M = input("INVALID! Please enter a valid max radius for the Mandelbrot Set: ")

    if isJSet:
        J = input("Please enter a valid max radius for the Julia Set: ")
        while not(isValid(type(1), J)):
            J = input("INVALID! Please enter a valid max radius for the Julia Set: ")

    return [int(J), int(M)]

def close():
    MSetWin.close()
    JSetWin.close()

def intro():
    print("This program was made by Ethan Leifer for Non Linear Dynamics Class at Dwight Englewood School")
    time.sleep(1)
    print("You will be asked to set a bumch of intial values to set up windows. After you will be able to change any of them through a menu interface. ")
    time.sleep(3)

def main():
    global autoClear, cos

    intro()

    # user can change the following values so it make opening shorting a set deafults
    maxRadius = [2, 2]
    maxIters = [50, 50]
    maxItersJ = maxIters[0]
    maxItersM = maxIters[1]
    maxRadiusJ = maxRadius[0]
    maxRadiusM = maxRadius[1]

    JSetColor = 'red'
    MSetColor = 'blue'
    JSetAlgo = '1'
    JSetAlgoDict = {'1': "brute force algorithm", '2': "orginal inverse algorithm", '3': "modifed inverse algorithm", '4': "exterior algorithm"}

    resolution = changeResolution(firstTime=True)  # IMPORTANT: changes the speed of the drawing of the program so I let user set their own
    resolutionJ = resolution[0]
    resolutionM = resolution[1]

    MSetZoomed = False
    JSetZoomed = False

    plotMSet(maxItersM, maxRadiusM, resolutionM, MSetColor)
    c = getCValue(maxItersM, maxRadiusM)

    statement = "\n'0' to quit\
                \n'1' to change Julia Set algorithm and redraw\
                \n'2' to redraw Mandelbrot set\n'3' to change C value\
                \n'4' to change maximum iterations\
                \n'5' to change maximum radius\
                \n'6' to change resolution\
                \n'7' to change the color scheme\
                \n'8' to change zoom\
                \n'9' to change automatically clear of the Julia Set Display when redrawn\
                \n'10' to change color transformation"
    options = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    option = '1'
    getNewOption = True

    # MENU
    while not(option == '0'):

        if option == '1':
            # manages redrawing of julia set
            JSetAlgo = graphJSet(c, JSetAlgo, maxItersJ, maxRadiusJ, resolutionJ, JSetColor)

        if option == '2':
            print("You are now regraphing the Mandelbrot set")
            plotMSet(maxItersM, maxRadiusM, resolutionM, MSetColor)

        if option == '3':
            # This gets the C value and updates both windows accordingly
            c = getCValue(maxItersM, maxRadiusM)
            graphJSet(c, JSetAlgo, maxItersJ, maxRadiusJ, resolutionJ, JSetColor)

        if option == '4':
            # lets user change maxIters and updates both windows accordingly
            maxIters = changeMaxIters(maxIters)
            maxItersJ = maxIters[0]
            maxItersM = maxIters[1]
            plotMSet(maxItersM, maxRadiusM, resolutionM, MSetColor)
            JSetAlgo = graphJSet(c, JSetAlgo, maxItersJ, maxRadiusJ, resolutionJ, JSetColor)

        if option == '5':
            # lets user change maxRadius and update both windows according
            maxRadius = changeMaxRadius(maxRadius)
            maxRadiusJ = maxRadius[0]
            maxRadiusM = maxRadius[1]
            plotMSet(maxItersM, maxRadiusM, resolutionM, MSetColor)
            JSetAlgo = graphJSet(c, JSetAlgo, maxItersJ, maxRadiusJ, resolutionJ, JSetColor)

        if option == '6':
            resolution = changeResolution(resolution)
            resolutionJ = resolution[0]
            resolutionM = resolution[1]
            plotMSet(maxItersM, maxRadiusM, resolutionM, MSetColor)
            JSetAlgo = graphJSet(c, JSetAlgo, maxItersJ, maxRadiusJ, resolutionJ, JSetColor)

        if option == '7':
            # change colors:
            # NEW FEATURE: after change color let user look at it (on new window?) to see if they like it better than the previous one, then replace previous one with new window
            if getOption(['m', 'j'], "Would you like to change the color of the Julia Set ('j') or Mandlebrot set ('m')") == 'm':
                MSetColor = getNewColor()
                pass
            else:
                JSetColor = getNewColor()
                pass

        if option == '8':
            # zoom
            zoomVals = zoom(MSetZoomed, JSetZoomed, c, maxItersM, maxItersJ, maxRadiusM, maxRadiusJ, resolutionM, resolutionJ, MSetColor, JSetColor, JSetAlgo)
            MSetZoomed = zoomVals[0]
            JSetZoomed = zoomVals[1]

        if option == '9':
            autoClear = not(autoClear)
            if autoClear:
                print("You are now automatically clearing the Julia Set window when you choose to redraw")
            else:
                print("You are now not automatically Clearing the Julia Set window when you choose to redraw")

        if option == '10':
            cos = not(cos)
            if cos:
                print("Your color will now be based on a cos transformation (This looks cooler when zooming)")
            else:
                print("Your color will now be based on a linear transformation (This shows the escape iterations more clearly)")
            plotMSet(maxItersM, maxRadiusM, resolutionM, MSetColor)
            JSetAlgo = graphJSet(c, JSetAlgo, maxItersJ, maxRadiusJ, resolutionJ, JSetColor)

        if getNewOption:
            option = getOption(options, statement)
        getNewOption = True

    close()


if __name__ == "__main__":
    main()
