import os
import random
from collections import UserDict
import pickle
import json

from dictionary_generator import TextGen
from question_state import QuestionState
from util import *
from draw import Draw

class Question(dict) :
    Layout_HSep_None = 0
    Layout_HSep_BlankLine1 = 0.5
    Layout_HSep_BlankLine2 = 0.75
    Layout_HSep_BlankLine3 = 1.
    Layout_HSep_BlankLine4 = 1.25
    
    Layout_HSep_SolidLine = 0x8
    Layout_HSep_DashedLine = 0x10
    Layout_HSep_DottedLine = 0x20
    
    Layout_HLine_Top = 0x40
    Layout_HLine_Bottom = 0x80
    
    Layout_VSep_None = 0
    Layout_VSep_BlankLine1 = 1
    Layout_VSep_BlankLine2 = 1.25
    Layout_VSep_BlankLine3 = 1.5
    Layout_VSep_BlankLine4 = 1.75
    
    Layout_VSep_SolidLine = 0x8
    Layout_VSep_DashedLine = 0x10
    Layout_VSep_DottedLine = 0x20  
    
    Layout_VLine_Left = 0x40
    Layout_VLine_Right = 0x80  
    Layout_VLine_LeftAndRight = 0x100  
    Layout_VLine_Internal = 0x40
    Layout_VLine_ExternalAndInternal = 0x80   
            
    def __init__(self, options) :
    #def __init__(self, *args, **kwargs):
        super(Question, self).__init__()
        self.__dict__ = self  

        self.name = "Unset"
        self.options = options
        dimensions = options["dimensions"]
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.imageFormat = options.get("format", "png")
                        
        self.drawDebugRects = False
        
        self.draw = Draw(self)
        self.draw.initImage()        
        
    def generatePage(self) :
        self.left_margin = self.width * (0.03 + (0.05 * random.random()))
        self.right_margin = self.width * (0.03 + (0.05 * random.random()))
        self.top_margin = self.height * (0.04 + (0.05 * random.random()))
        self.bottom_margin = self.height * (0.04 + (0.05 * random.random()))
    
        fontnames = ["verdana.ttf", "times.ttf", "georgia.ttf", "arial.ttf"]

        # Assume that its A4 size, calculate relative to width
        #self.lineHeight = self.fontSize = random.randint(18,24)  
        self.lineHeight = self.fontSize = random.randint(int(self.width / 70), int(self.width / 50))  
        self.fontName = random.choice(fontnames)
        self.questionFrames = []
        self.questionTextFrames = []
    
        self.generateRandomStyle()
    
        self.minimumQuestionGap = self.paraSpacing * 1.5
        
        self.draw.createDraw()
        self.generator = TextGen.getGenerator()
    
        self.lineHeight = self.draw.getLineHeight()
    
        self.generateLayout() 
        self.draw.drawBackground()
    
        self.drawColumns()        
        
    #def saveState(self) :
        #os.makedirs("state", exist_ok=True)
        #with open(os.path.join("state", self.name + ".state.bin"), "wb") as pickleFile :
            #pickle.dump(self, pickleFile)
        
    #@classmethod
    #def restoreState(cls, name) :
        #with open(os.path.join("state", str(name) + ".state.bin"), "rb") as pickleFile :
            #return pickle.load(pickleFile)
    
    def generateRandomStyle(self) :        
        columns = ( (0.66, 1), (0.9, 2), (1., 3) )
        hseps_lines = (
            (0.2,  Question.Layout_HSep_BlankLine1),
            (0.6,  Question.Layout_HSep_BlankLine2),
            (0.85, Question.Layout_HSep_BlankLine3),
            (1.0,  Question.Layout_HSep_BlankLine4),
        )
        
        vseps_lines = (
            (0.2,  Question.Layout_VSep_BlankLine1),
            (0.6,  Question.Layout_VSep_BlankLine2),
            (0.85, Question.Layout_VSep_BlankLine3),
            (1.0,  Question.Layout_VSep_BlankLine4),
        )

        hseps_styles = (
            (0.7,  Question.Layout_HSep_None),
            (0.8,  Question.Layout_HSep_SolidLine),
            (0.9,  Question.Layout_HSep_DashedLine),
            (1.0,  Question.Layout_HSep_DottedLine),
        )    
        
        vseps_styles = (
            (0.7,  Question.Layout_VSep_None),
            (0.8,  Question.Layout_VSep_SolidLine),
            (0.9,  Question.Layout_VSep_DashedLine),
            (1.0,  Question.Layout_VSep_DottedLine),
        )
        
        hseps_positions = (
            #(0.65, Question.Layout_HSep_None),
            (0.9, Question.Layout_HLine_Bottom),
            (1.0, Question.Layout_HLine_Top),
        )
        
        vseps_positions = (
            #(0.65, Question.Layout_VSep_None),
            (0.85, Question.Layout_VLine_LeftAndRight),
            (0.93, Question.Layout_VLine_Left),
            (1.0, Question.Layout_VLine_Right),
        )
        
        alignment = (
            (0.65, Draw.AlignLeft),
            (0.85, Draw.AlignJustify),
        )  
        
        self.lineSpacing = probChoiceList(((0.65, 1.2), (0.85, 1.3), (1.0,1.5)))
        self.paraSpacing = self.lineHeight * self.lineSpacing * (0.25 + (random.random() * 0.5))
        
        self.textAlign = probChoiceList(alignment)
        self.columns = probChoiceList(columns)
        
        if self.columns > 1 :
            vseps_styles = [(p * .5, a) for p, a in vseps_styles]
        
        self.horizontal_space = probChoiceList(hseps_lines)    
        self.horizontal_linestyle = probChoiceList(hseps_styles) 
        self.horizontal_lineposition = probChoiceList(hseps_positions)
        
        self.vertical_space = probChoiceList(vseps_lines)    
        self.vertical_linestyle = probChoiceList(vseps_styles)    
        self.vertical_lineposition = probChoiceList(vseps_positions)     
        
        self.horizontalPriority = random.random()
        self.setMeasureOnlyMode(False)
        
        self.backgroundColor = generateColor(random.randint(245,255))
        self.textColour = generateColor(random.randint(4,96))
        
        if random.random() > 0.7 :
            self.borderColour = generateColor(random.randint(245,255))
        else :
            self.borderColour = self.textColour 
            
        self.horizontal_line_width = random.choice(list(range(1,5)))
        self.vertical_line_width = random.choice(list(range(1,5)))
        
        self.questionFillColour = random.choice([self.borderColour, self.textColour,
                                                 "blue", "grey", "green", "purple"])
            
    def setMeasureOnlyMode(self, mode) :
        self.draw.measure_only = mode
        
    def adjustRectForStyle(self, rect, column = 0) :
        top = rect[0][1]
        if self.horizontal_lineposition == Question.Layout_HLine_Top :
            top += (self.lineHeight * self.horizontal_space)
        
        bottom = rect[1][1]
        if self.horizontal_lineposition == Question.Layout_HLine_Bottom :
            bottom -= (self.lineHeight * self.horizontal_space)     
                   
        left = rect[0][0]
        if column != 0 :
            if self.columns == 1 and self.vertical_lineposition in \
               (Question.Layout_VLine_Left, 
                Question.Layout_VLine_LeftAndRight) :
                left += self.lineHeight * self.vertical_space   
            elif self.columns > 1 and self.vertical_lineposition == \
                 Question.Layout_VLine_ExternalAndInternal :
                left += self.lineHeight * self.vertical_space          
            elif self.columns > 1 and self.vertical_lineposition == \
                 Question.Layout_VLine_Internal :
                if column != 1 :
                    left += self.lineHeight * self.vertical_space
                
        right = rect[1][0]  
        if column != 0 :
            if self.columns == 1 and self.vertical_lineposition  in \
               (Question.Layout_VLine_Right, Question.Layout_VLine_LeftAndRight) :
                right -= self.lineHeight * self.vertical_space   
            elif self.columns > 1 and self.vertical_lineposition == \
                 Question.Layout_VLine_ExternalAndInternal :
                right -= self.lineHeight * self.vertical_space          
            elif self.columns > 1 and self.vertical_lineposition == \
                 Question.Layout_VLine_Internal :
                if column != self.columns :
                    left -= self.lineHeight * self.vertical_space        

        return ((left, top), (right, bottom))

    def drawColumns(self) :       
        column = 1
        
        if self.horizontalPriority > 0.5 :
            pass
        
        for rect in self.rawFrames :
            if (self.columns == 1 and self.vertical_lineposition in \
                (Question.Layout_VLine_Left, Question.Layout_VLine_LeftAndRight)) or \
               (self.columns > 1 and self.vertical_lineposition == \
                Question.Layout_VLine_ExternalAndInternal) or \
               (self.columns > 1 and self.vertical_lineposition == \
                Question.Layout_VLine_Internal and column != 1) :
                line = (rect[0], (rect[0][0],rect[1][1]))
                self.draw.drawLine(line, self.vertical_line_width, style=self.vertical_linestyle)                
      
            if (self.columns == 1 and self.vertical_lineposition  in \
                (Question.Layout_VLine_Right, Question.Layout_VLine_LeftAndRight)) or \
               (self.columns > 1 and self.vertical_lineposition == \
                Question.Layout_VLine_ExternalAndInternal) or \
               (self.columns > 1 and self.vertical_lineposition == \
                Question.Layout_VLine_Internal and column != self.columns) :
                line = ((rect[1][0],rect[0][1]), rect[1])
                self.draw.drawLine(line, self.vertical_line_width, style=self.vertical_linestyle)    
                    
            column += 1    
    
    def generateLayout(self) :
        available_width = self.width - self.left_margin - self.right_margin
        column_width = available_width / self.columns
        available_height = self.height - self.top_margin - self.bottom_margin
        
        self.textFrames = []
        self.rawFrames = []
        
        for i in range(self.columns) :
            rect = (
                ( self.left_margin + (i * column_width), self.top_margin),
                ( self.left_margin + ((1 + i) * column_width), self.height - self.bottom_margin)
            )
            
            self.rawFrames.append(rect)
            textRect = rect # self.adjustRectForStyle(rect, i + 1)
            self.textFrames.append(textRect)

    def getCurrentWriteLocation(self) :
        """
        This should return a rectangle specifiying where to write the next 
        question. 
        """
        if self.textFrames :
            return self.textFrames[0]
        else :
            return None
        
    def rectFitsInCurrentFrame(self, removeRect) :
        height = removeRect[1][1] - removeRect[0][1]
        currentFrame = self.textFrames[0]
    
        remainingHeight = currentFrame[1][1] - currentFrame[0][1]
        return (height < remainingHeight)        
    
    def updateCurrentWriteLocation(self, removeRect) :
        """
        Remove rect specifies an area to remove from the available space, either 
        because a question has been written to it or because its too small to
        write the next question into.
        """
        height = removeRect[1][1] - removeRect[0][1]
        currentFrame = self.textFrames[0]
        
        remainingHeight = currentFrame[1][1] - currentFrame[0][1]
        if height >= remainingHeight :
            self.textFrames.remove(currentFrame)
        else :
            self.textFrames.remove(currentFrame)
            self.textFrames.insert(0, ((currentFrame[0][0], currentFrame[0][1] + height) , currentFrame[1]))
            
    def drawHorizontalStyles(self, rect, isTop) :
        height = 0 
        left = rect[0][0]
        right = rect[1][0]
        line_gap = int(self.horizontal_space * self.lineHeight * 0.5)
        if line_gap < self.minimumQuestionGap * 0.5 :
            line_gap = self.minimumQuestionGap * 0.5 
        
        if self.horizontal_lineposition == Question.Layout_HLine_Top and isTop :
            line_top = rect[0][1]
            self.draw.drawLine(((left, line_top), (right, line_top)), 
                          self.horizontal_line_width, style=self.horizontal_linestyle)
            
        elif self.horizontal_lineposition == Question.Layout_HLine_Bottom and not isTop :
            line_top = rect[0][1] + line_gap
            self.draw.drawLine(((left, line_top), (right, line_top)), 
                          self.horizontal_line_width, style=self.horizontal_linestyle)   

        return line_gap + line_gap
 
    def createPage(self, name) :
        self.name = name
        self.generatePage()
        
        questionNumber = random.randint(1,20)
        while True :
            rect = self.getCurrentWriteLocation()
            if rect is None :
                break
            
            new_rect, scan_rect = self.writeQuestion(questionNumber)
            
            if scan_rect and self.rectFitsInCurrentFrame(new_rect) :
                self.questionTextFrames.append(scan_rect)
                self.questionFrames.append(inflateRect(
                    new_rect, self.lineHeight * 0.5, self.lineHeight * 0.5))
                
                if self.drawDebugRects :
                    #self.draw.rectangle(scan_rect, outline="red")
                    self.draw.rectangle(new_rect, outline="blue")
                    
                questionNumber += 1

            self.updateCurrentWriteLocation(new_rect)  
             
    def save(self, size = None) :
        if size :
            output_size = size
        else :
            output_size = self.options.get("outputSize")
            
        dirname = self.options.get("outputDir", "output")
        
        if self.options.get("saveTiles", False) :
            self.saveTiles(dirname, output_size)
        else :        
            self.savePage(dirname)
            
    def savePage(self, dirname, size = None) :
        filename = os.path.join(dirname, "{}.{}".format(self.name, self.imageFormat))
        if size :
            img = self.draw.save(filename, rect = ((0,0),(self.width, self.height)), resizeTo = size)
            
            questionFrames = resizeRects(self.questionFrames, (self.width, self.height), size)
            questionTextFrames = resizeRects(self.questionTextFrames, (self.width, self.height), size)
            
            #Draw.debugRects(img, self.questionFrames, "1" + ".png")
        else :
            self.draw.save(filename) 
            questionFrames = self.questionFrames
            questionTextFrames = self.questionTextFrames

        metaData = {
            "enclosedQuestions" : questionFrames,
            "enclosedText" : questionTextFrames,
            "overlapQuestions" : questionFrames,
            "overlapText" : questionTextFrames,
        }

        self.saveMetaData(filename, metaData)
            
    def saveTiles(self, dirname, size) :
        increment = int((self.height - self.width) / 2)
        
        tiles = [
            ("top", ((0,0), (self.width, self.width))),
            ("middle", ((0,increment), (self.width, self.width + increment))),
            ("bottom", ((0,increment * 2), (self.width, self.width + (increment * 2)))),
        ]
        
        for name, tile in tiles :
            filename = os.path.join(dirname, "{}-{}.{}".format(self.name, name, self.imageFormat))
  
            img = self.draw.save(filename, tile, size)
            
            offset = tile[0]
    
            questionFrames = resizeOffsetRects(self.questionFrames, tile[0], (self.width, self.width), size)
            questionTextFrames = resizeOffsetRects(self.questionTextFrames, tile[0], (self.width, self.width), size)
            
            enclosedQuestionFrames = [r for r in questionFrames if rectEnclosedByRect(((0,0), size), r)]
            enclosedQuestionTextFrames = [r for r in questionTextFrames if rectEnclosedByRect(((0,0), size), r)]
            overlappedQuestionFrames = [r for r in questionFrames if overlapRect(((0,0), size), r)]
            overlappedQuestionTextFrames = [r for r in questionTextFrames if overlapRect(((0,0), size), r)]   
            
            metaData = {
                "enclosedQuestions" : enclosedQuestionFrames,
                "enclosedText" : enclosedQuestionTextFrames,
                "overlapQuestions" : overlappedQuestionFrames,
                "overlapText" : overlappedQuestionTextFrames,                
            }

            #Draw.debugRects(img, questionTextFrames, filename + ".png")
            self.saveMetaData(filename, metaData)
                            
    def saveMetaData(self, filename, metadata) :
        metadata.update({
            "width" : self.width,
            "height" : self.height,
            "filename" : os.path.basename(filename),
        })
        
        with open(os.path.join("{}.json".format(os.path.splitext(filename)[0])), "w")  as jsonfile:  
            json.dump(metadata, jsonfile, indent=2)         

    def generateQuestionTexts(self) :
        pass
      
    def writeQuestion(self, questionNumber) :
        pass  
