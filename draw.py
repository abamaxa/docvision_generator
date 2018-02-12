from PIL import Image, ImageDraw, ImageFont
import os
import random
from dictionary_generator import TextGen
import pickle
import json

class Draw :
    AlignLeft    = 0
    AlignRight   = 1
    AlignCenter  = 2
    AlignJustify = 3  
        
    def __init__(self, state) :
        self.questionState = state   
        self.image = None
        self.font = None
        self.draw = None  
        self.measure_only = False
        
    def initImage(self) :
        self.image = Image.new('RGB', self.getImageSize())
        
    def createDraw(self) :
        self.cleanup()
        
        self.font = ImageFont.truetype("fonts/" + self.questionState.fontName, 
                                       self.questionState.fontSize)
        self.draw = ImageDraw.Draw(self.image)   
                
    def getLineHeight(self) :
        return self.draw.textsize("Hg", font=self.font)[1]
    
    def drawBackground(self) :
        self.draw.rectangle(((0,0), self.getImageSize()), 
                            fill=self.questionState.backgroundColor)   
        
    def getImageSize(self) :
        return (self.questionState.width,  self.questionState.height)
                    
    def setMeasureOnlyMode(self, mode) :
        self.measure_only = mode
        
    def rectangle(self, points, fill=None, outline=None) :
        if not self.measure_only :
            self.draw.rectangle(points, fill, outline)
              
    def drawLine(self, points, width = 1, style = None) :
        if not self.measure_only :
            self.draw.line(points, fill=self.questionState.borderColour, width = width)
            
    def drawQuestionCircle(self, xy) :
        if not self.measure_only :
            extra = int(self.questionState.fontSize * 0.2)
            pt = ((xy[0] - extra, 
                   xy[1] - extra), 
                  (xy[0] + self.questionState.lineHeight + extra, 
                   xy[1] + self.questionState.lineHeight + extra))
            self.draw.ellipse(pt, 
                              fill = self.questionState.questionFillColour, 
                              outline = self.questionState.borderColour)
        
    def drawText(self, position, width, text, align = AlignLeft, firstLineOffset = 0, forceColor = None) :
        #print(text)
        if forceColor :
            textColour = forceColor
        else :
            textColour = self.questionState.textColour
            
        def renderText(position, lineWidth, wordList, align) :
            if align in (Draw.AlignLeft, Draw.AlignJustify) :
                writePosition = position
            else :
                last_text_width, last_text_height = self.draw.textsize(" ".join(wordList), font=self.font)
                if align == Draw.AlignRight :
                    writePosition = (position[0] + (lineWidth - last_text_width), position[1])
                elif align == Draw.AlignCenter :
                    writePosition = (position[0] + ((lineWidth - last_text_width) / 2), position[1])
                    
            if align == Draw.AlignJustify and len(wordList) > 1:
                justifySpace = []
                for jw in wordList :
                    jwidth, _ = self.draw.textsize(jw, font=self.font)
                    justifySpace.append(jwidth)
                                            
                extra_space = (lineWidth - sum(justifySpace)) / (len(wordList) - 1)
                curx = position[0]
                jw_count = 0
                
                for jw, jwidth in zip(wordList, justifySpace) :  
                    jw_count += 1
                    if jw_count == len(wordList) :
                        curx = position[0] + lineWidth - jwidth
                        
                    if not self.measure_only : 
                        self.draw.text((curx, position[1]), jw, 
                                font=self.font, fill=textColour)
                        
                    curx += jwidth + extra_space
                    
            elif not self.measure_only :
                self.draw.text(writePosition, " ".join(wordList), 
                               font=self.font, fill=textColour)
                
                            
        words = text.split(' ')
        wordList = []
        totalHeight = 0
        
        lastText = testText = ""
        counter = 0
        
        for word in words :
            counter += 1
            if totalHeight == 0 :
                lineWidth = width - firstLineOffset
            else :
                lineWidth = width
                
            text_width, text_height = self.draw.textsize(" ".join(wordList + [word]), font=self.font)
                        
            if text_width > lineWidth or counter == len(words):
                thisAlign = align
                if text_width <= lineWidth or len(wordList) == 0 :
                    wordList.append(word)
                    if align == Draw.AlignJustify :
                        align = Draw.AlignLeft
                    
                if totalHeight == 0 and firstLineOffset :
                    offsetPosition = (position[0] + firstLineOffset, position[1])
                    renderText(offsetPosition, lineWidth,  wordList, align)
                else :
                    renderText(position, lineWidth,  wordList, align)
                    
                totalLineHeight = int(text_height * self.questionState.lineSpacing)
                position = (position[0], position[1] + totalLineHeight)
                totalHeight += totalLineHeight
                
                if text_width > width and counter == len(words):
                    renderText(position, width,  [word], align)
                    totalHeight += totalLineHeight
                
                wordList = []
                                
            wordList.append(word)
        
        return totalHeight

    def save(self, filename, rect = None, resizeTo = None) :  
        os.makedirs(os.path.dirname(filename), exist_ok=True)
                
        if rect is None and resizeTo is None :
            img = self.image
        else :
            img = self.copyRect(rect, resizeTo)

        img.save(filename)
        return img

    def copyRect(self, rect, resizeTo) :
        img = Image.new('RGB', (rect[1][0] - rect[0][0], rect[1][1] - rect[0][1]))
        imSrc = self.image.crop( (rect[0][0], rect[0][1], rect[1][0], rect[1][1]))
        img.paste(imSrc)
        img = img.resize(resizeTo, Image.BILINEAR)
        return img
        
    def cleanup(self) :
        if self.draw :
            del self.draw   
            self.draw = None        
        
    @staticmethod
    def debugRects(img, rectangles, saveAsFile) :
        draw = ImageDraw.Draw(img) 
        for rect in rectangles :
            draw.rectangle(rect, outline="red")
        img.save(saveAsFile)        
