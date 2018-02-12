import random

def probChoiceList(probChoiceList) :
    pick = random.random()
    for prob, choice in probChoiceList :
        if prob > pick :
            return choice
        
    return probChoiceList[-1][1]

def generateColor(base) :
    value_range = 4
    c = value_range / 2
    r = max(0, min(255, base + random.randint(0, value_range) - c))
    b = max(0, min(255, base + random.randint(0, value_range) - c))
    g = max(0, min(255, base + random.randint(0, value_range) - c))

    col = "#%02x%02x%02x" % (int(r),int(g),int(b)) 

    if len(col) < 7 :
        raise Exception("Bad color")

    return col

def inflateRect(rect, inflateByX, inflateByY) :
    return (
        (
            rect[0][0] - inflateByX, 
            rect[0][1] - inflateByY
        ),
        (
            rect[1][0] + inflateByX, 
            rect[1][1] + inflateByY
        ),
    )    

def resizeRects(rectList, currentSize, newSize) :
    newRects = []
    xscale = newSize[0] / currentSize[0]
    yscale = newSize[1] / currentSize[1]
    
    for rect in rectList :
        newRects.append((
            (rect[0][0] * xscale, rect[0][1] * yscale),
            (rect[1][0] * xscale, rect[1][1] * yscale)
        ))
    
    return newRects

def resizeOffsetRects(rectList, offset, currentSize, newSize) :
    newRects = []
    xoffset = -offset[0]
    yoffset = -offset[1]
    
    for rect in rectList :
        newRects.append((
            (rect[0][0] + xoffset, rect[0][1] + yoffset),
            (rect[1][0] + xoffset, rect[1][1] + yoffset)
        ))
    
    return resizeRects(newRects, currentSize, newSize)

def rectEnclosedByRect(enclosingRect, testRect) :
    return (
        (testRect[0][0] >= enclosingRect[0][0]) and 
        (testRect[0][0] <= enclosingRect[1][0]) and 
        (testRect[1][0] >= enclosingRect[0][0]) and 
        (testRect[1][0] <= enclosingRect[1][0]) and 
        (testRect[0][1] >= enclosingRect[0][1]) and 
        (testRect[0][1] <= enclosingRect[1][1]) and 
        (testRect[1][1] >= enclosingRect[0][1]) and 
        (testRect[1][1] <= enclosingRect[1][1])        
    )

def overlapRect(enclosingRect, testRect) :
    return (
        ((testRect[0][0] >= enclosingRect[0][0]) and 
        (testRect[0][0] <= enclosingRect[1][0])) or 
        ((testRect[1][0] >= enclosingRect[0][0]) and 
        (testRect[1][0] <= enclosingRect[1][0])) or 
        ((testRect[0][1] >= enclosingRect[0][1]) and 
        (testRect[0][1] <= enclosingRect[1][1])) or 
        ((testRect[1][1] >= enclosingRect[0][1]) and 
        (testRect[1][1] <= enclosingRect[1][1]))        
    )
    

