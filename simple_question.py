import random
import string
from functools import partial

from draw import Draw
from base_question import Question

class SimpleQuestion(Question) :
    ROMAN_DIGITS = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi" "xii", "xiii", "xiv", "xv"]
   
    def __init__(self, *args, **kwargs):
        super(SimpleQuestion, self).__init__(*args, **kwargs)   
        
    def generatePage(self) :
        super(SimpleQuestion, self).generatePage()
        
        self.paraMargin = int(random.choice([0, 2.2 * self.lineHeight, 1.8 * self.lineHeight]))
        self.subParaPrefix = int(random.randint(0,2) * self.lineHeight * 0.3)
        if self.paraMargin :
            self.subParaMargin = int(self.paraMargin)
        else :
            self.subParaMargin = int(random.choice([0,2.2 * self.lineHeight, 1.8 * self.lineHeight]))
            
        self.subParaTerminator = random.choice([".", ")", ")."])
        if random.random() < 0.5 :
            self.subParaDigits = string.ascii_lowercase
        else :
            self.subParaDigits = SimpleQuestion.ROMAN_DIGITS
                
    def getHorizontalPadding(self) :
        return self.vertical_space * self.lineHeight * 0.5
    
    def getTextRect(self, rect) :
        hspace = self.getHorizontalPadding()    
        return ((rect[0][0] + hspace, rect[0][1]), (rect[1][0] - hspace, rect[1][1]))
        
    def writeQuestionHeader(self, rect) :
        textRect = self.getTextRect(rect)
    
        return self.drawHorizontalStyles(textRect, True)  
    
    def writeQuestionFooter(self, rect, heightConsumed) :
        textRect = self.getTextRect(rect)
    
        bottom_rect = ((textRect[0][0], rect[0][1] + heightConsumed), textRect[1])

        return self.drawHorizontalStyles(bottom_rect, False)  
    
    def writeParagraphs(
        self, 
        rect, 
        questionNumber,
        paragraph, 
        subparagraph, 
        endparagraph,
        heightConsumed
    ) :
        textRect = self.getTextRect(rect)
        
        width = textRect[1][0] - textRect[0][0]
        paragraphNumer = 0
        textheight = 0
        top = textRect[0][1] + heightConsumed

        for text in paragraph :
            left = textRect[0][0] + self.paraMargin
            offset = 0
            if paragraphNumer == 0 :
                if self.paraMargin == 0:
                    self.draw.drawQuestionCircle((textRect[0][0], top + textheight))
                    offset = self.fontSize * 1.5   
                    numberColour = self.backgroundColor
                else :
                    numberColour = self.textColour
                                        
                self.draw.drawText((textRect[0][0], top + textheight), 
                              width, str(questionNumber) + ".", Draw.AlignLeft,
                              forceColor = numberColour)
              
            textheight += self.draw.drawText((
                left,  
                top + textheight), 
                width - self.paraMargin, 
                text, 
                self.textAlign,
                firstLineOffset = offset)
            
            paragraphNumer += 1
            if paragraphNumer != len(paragraph) or (len(subparagraph) or len(endparagraph)):
                textheight += self.paraSpacing 
             
        paragraphNumer = 0 
        for text in subparagraph :
            if self.subParaMargin :
                self.draw.drawText((
                    textRect[0][0] + self.paraMargin + self.subParaPrefix,  
                    top + textheight), 
                    width - self.paraMargin - self.subParaPrefix, 
                    self.subParaDigits[paragraphNumer] + self.subParaTerminator, 
                    self.textAlign)                
                
            textheight += self.draw.drawText((
                textRect[0][0] + self.paraMargin + self.subParaPrefix + self.subParaMargin,  
                top + textheight), 
                width - self.paraMargin - self.subParaPrefix -  self.subParaMargin, 
                text, 
                self.textAlign)
            
            paragraphNumer += 1
            if paragraphNumer != len(subparagraph) or len(endparagraph):
                textheight += self.paraSpacing   
             
        paragraphNumer = 0    
        for text in endparagraph :
            textheight += self.draw.drawText((
                textRect[0][0] + self.paraMargin,  
                top + textheight), 
                width - self.paraMargin, 
                text, 
                self.textAlign)
            
            paragraphNumer += 1
            if paragraphNumer != len(endparagraph) :
                textheight += self.paraSpacing        
            
        scanRect = (
            (
                textRect[0][0] - self.lineHeight * 0.5, 
                textRect[0][1] + heightConsumed - self.lineHeight * 0.5
            ),
            (
                textRect[1][0] + self.lineHeight * 0.5, 
                textRect[0][1] + heightConsumed + textheight + self.lineHeight * 0.5
            ),
        )
        
        return scanRect, textheight
    
    def calculateAreaConsumed(self, rect, heightConsumed) :
        return (rect[0], (rect[1][0], rect[0][1] + heightConsumed))
        
    def writeSimpleQuestion(self, number, rect, text) :
        """
        Number = 1-20, a-g 
        Usually in a margin but can be indented.
        Often bold and followed by dot or bracket.
        """        
        height = self.writeQuestionHeader(rect)
        
        scanRect, textheight = self.writeParagraphs(rect, number, text, [], [], height)
        
        height += textheight
        height += self.writeQuestionFooter(rect, height)
        
        return self.calculateAreaConsumed(rect, height), scanRect 
    
    
    def writeMultipartQuestion(self, number, rect, text, subparagraph, endparagraph) :
        height = self.writeQuestionHeader(rect)

        scanRect, textheight = self.writeParagraphs(rect, number, text, 
                            subparagraph, endparagraph, height)
    
        height += textheight
        height += self.writeQuestionFooter(rect, height)
    
        return self.calculateAreaConsumed(rect, height), scanRect 

    def generateQuestionTexts(self, sentence = False) :
        if sentence :
            return self.generator.generate_sentence()[2]
        else :
            return self.generator.generate_sentence()[2]
    
    def writeQuestion(self, questionNumber) :
        trys = 0
        new_rect = scan_rect =  None
        while True :
            rect = self.getCurrentWriteLocation()
            if rect is None :
                break
            
            trys += 1
            self.setMeasureOnlyMode(True)
            
            subparagraph = []
            endparagraph = []
            paragraph = [self.generateQuestionTexts()]
            if trys < 3 :
                if random.random() < 0.5 :
                    paragraph.append(self.generateQuestionTexts())
                    
                if random.random() < 0.75 :
                    for i in range(random.randint(1, 3)) :
                        subparagraph.append(self.generateQuestionTexts(True))
                    
            if trys < 2 and random.random() < 0.5 :
                endparagraph.append(self.generateQuestionTexts())

            if subparagraph or endparagraph :
                func = partial(self.writeMultipartQuestion, questionNumber, 
                                           rect, paragraph, subparagraph, endparagraph)                
            else :
                func = partial(self.writeSimpleQuestion, questionNumber, rect, paragraph)
                      
            new_rect, scan_rect = func()          
            if self.rectFitsInCurrentFrame(new_rect) :
                self.setMeasureOnlyMode(False)
                new_rect, scan_rect = func()  
                break
                
            elif trys > 4 :
                scan_rect = None
                break
               
        return new_rect, scan_rect
    