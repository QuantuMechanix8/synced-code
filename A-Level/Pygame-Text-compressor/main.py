# pygame and pygame widgets import for visuals
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.button import Button

# other imports (for accessing images, timing algorithms, closing the program and general maths)
import time
import sys
import os
import math

# importing my own files to use their functions
import RunLengthEncoding
import BytePairEncoding
import LempelZiv77
import HuffmanEncoding
import GeneralFunctions

# initialising pygame
pygame.init()
pygame.font.init
# list of all objects that are on the screen - all implement objectInterface (allows me to redraw the screen by storing all the objects on it)
ALLOBJECTS = []
# note that all draw methods must only require self as input as they will be called from this list

# defining used colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
darkGrey = (50, 50, 50)
moderateGrey = (70, 70, 70)
lightGrey = (150, 150, 150)
backgroundColour = (25, 25, 25)
inputPassiveColour = (230, 247, 255)
inputActiveColor = (128, 212, 255)
infoRectColour = (221, 255, 204)

# defining fonts
# only font i could find with characters like ㉜ so had to include it in the project's assets
compressionFont = "assets/Quivira.otf"
inputFont = "roboto"
uiFont = "constantia"

# setting up animation window
FPS = 60
WIDTH, HEIGHT = 1050, 450  # 21:9 aspect ratio default
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.get_surface().fill(backgroundColour)
pygame.display.set_caption("Text Compression Visualiser")
compressionIcon = pygame.image.load(
    os.path.join('assets', 'compressionIcon.png'))
pygame.display.set_icon(compressionIcon)

MAINARROW = None

class objectInterface():
    # technically this is an abstract class but it functions like an interface
    """interface for all objects that will be drawn on the screen - ensures they all have a draw method"""

    def __init__(self):
        pass

    def draw():
        raise Exception(
            "draw method not implemented in a class using the objectInterface")
        # if a class implementing (inheriting from) the interface class has not overridden a draw method we raise an error as it needs to have one


class regionRect(objectInterface):
    """class of rectangles outlining regions on the screen (needed to allow drawing and undrawing)"""

    def __init__(self, rect, colour=black):
        # initialising attributes (having the position is neater than always accessing position from self.rect)
        self.rect = rect
        self.position = self.rect.topleft
        self.colour = colour

    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), self.colour, self.rect)
        # simply draws the rectangle (self.rect) onto the screen


class textRegionRect(regionRect):
    """class of rectangles outlining regions on the screen that will contain text - subClass of general regionRect"""

    def __init__(self, rect, text, colour=lightGrey, fontColour=black, fontSize=None, font=uiFont):
        # calling superclass (regionRect) constructor to initialise rectangle properties
        super().__init__(rect, colour)

        # assigning text attributes
        self.text = text
        numChars = len(self.text)
        self.fontSize = fontSize
        self.fontColour = fontColour

        if not fontSize:
            # if fontsize is not provided we find the largest viable fontsize - dependent on the more constraining of its rectangle's height and width
            self.fontSize = min(
                int(1.8*self.rect.width//(numChars+1)), int(0.8*self.rect.height))
        # even when fontsize is provided we ensure it isnt too large
        # note the use of numChars+1 in implementation to avoid /0
        self.fontSize = min(self.fontSize, 1.8*self.rect.width //
                            (numChars+1), int(0.8*self.rect.height))
        self.font = pygame.font.SysFont(font, self.fontSize)

    def changeStr(self, newText):
        """simple function to change the text in the regionRect - modifies fontsize accordingly"""
        self.text = newText
        numChars = len(self.text)
        self.fontSize = min(self.fontSize, int(
            1.6*self.rect.width//(numChars+1)), int(0.8*self.rect.height))

    def draw(self, clear=False):
        """draw method for textRegionRect class - has option clear to draw it without text"""
        pygame.draw.rect(pygame.display.get_surface(), self.colour,
                         self.rect)  # draws the rectangle (without text)
        if not clear:
            # if clear is false we blit the region's text onto the rectangle
            pygame.display.get_surface().blit(self.font.render(self.text, True, self.fontColour),
                                              (self.position[0] + pygame.display.get_surface().get_width()//256, self.position[1] + self.rect.height//12))
        if self == INFORECT:
            drawInfo(self.stringArray)
            # the INFORECT is also a textRegionRect but we need it to draw the information when we call drawInfo() (INFORECT has multiple lines etc so this method doesnt generalise - but should still implement objectInterface and so needs draw method)


class compressionString(objectInterface):
    """A class of the strings that are displayed on screen whilst being compressed/decompressed - composed of compressionStringChar objects"""

    def __init__(self, text, height=0.5):
        self.text = text
        self.height = height  # height is the proportion "down" the COMPRESSIONRECT surface the string is - 1 is sitting at the bottom 0 at the top
        # list comprehension to give the list of char objects contained in the string
        self.chars = [compressionStringChar(char) for char in text]
        self.font = compressionFont

    def updateText(self):
        """updates compressionString.text to match the compressionString.chars"""
        # often I manipulate the actual char objects rather than the text itself so a simple function that keeps them consistent is useful
        self.text = ""
        for char in self.chars:
            self.text += char.char

    def changeStr(self, newtext):
        """updates the string (text and chars attributes) for a new string"""
        self.text = newtext
        # again list comprehension to give the list of char objects contained in the string
        self.chars = [compressionStringChar(char) for char in self.text]

    def addStr(self, addedStr):
        """method to concatenate the compressionString (used for adding characters to the enteredString)"""
        self.text += addedStr
        additionalChars = [compressionStringChar(char) for char in addedStr]
        self.chars += additionalChars

    def backspace(self):
        """method to delete a character from the compressionString (used for deleting character in the enteredString)"""
        pygame.draw.rect(pygame.display.get_surface(),
                         inputActiveColor, INPUTRECT)
        # removing the last character and charObj from the compressionString
        self.text = self.text[:-1]
        self.chars = self.chars[:-1]

    def draw(self):
        """method which draws the compressionString (as line of boxed chars) on the COMPRESSIONRECT surface"""
        numBoxes = len(self.chars)
        margin = int(COMPRESSIONRECT.rect.width//(numBoxes+1))
        # margin adjusts to the string length (numboxes+1 used so the margin isnt entire string when a single char entered)

        # calculates the height for the box around each char
        charWidth = (COMPRESSIONRECT.rect.width-margin)//(numBoxes+1)
        charHeight = min(int(1.5*charWidth), COMPRESSIONRECT.rect.height//2)
        self.position = (margin//5, COMPRESSIONRECT.rect.y +
                         int(self.height*COMPRESSIONRECT.rect.height//2))
        # the pygame surface on which the whole string is based
        self.surface = pygame.Rect(
            self.position, (COMPRESSIONRECT.rect.width-margin, charHeight+1))
        pygame.draw.rect(pygame.display.get_surface(), darkGrey, self.surface)
        # starts x,y position at smallest values (top left) of the text surface
        currentXPos, currentYPos = self.surface.topleft
        # moves across by half the gap between rectangles for margin on the text surface
        currentXPos += int(0.5*charWidth)

        for char in self.chars:
            # sets the surface for each char with small (0.05*charWidth) gap between chars
            char.setRectangle(pygame.Rect(
                currentXPos, currentYPos, int(0.95*charWidth), charHeight))
            char.draw()
            currentXPos += charWidth  # moves along by character width to draw the next character

    def unDraw(self):
        """simple method which completely undraws the string"""
        deleteObj(self)
        drawScreen()

    def delete(self):
        """method to delete the string (doesn't affect screen)"""
        self.text = ""
        self.chars = []

    def isEmpty(self):
        """method to check if the string is empty"""
        if self.chars == []:
            return True
        else:
            return False

    def highlightChars(self, startIndex, endIndex, colour):
        """method to highlight a range of characters in the string"""
        for i in range(startIndex, endIndex):
            self.chars[i].highlight(colour, 3)


class compressionStringChar(objectInterface):
    """the component class of compressionString, being the objects for each character in the string"""

    def __init__(self, character):
        self.char = character

    def setRectangle(self, rectangle):
        """sets the rectangle surface where the character is based"""
        self.rectangle = rectangle

    def draw(self):
        """method to draw the character"""
        fontSize = int(0.7*self.rectangle.height)
        font = pygame.font.Font(compressionFont, fontSize)
        # draws white rectangle outline for the character
        pygame.draw.rect(pygame.display.get_surface(),
                         white, self.rectangle, 1)

        if self.char in ['W', 'w', 'M', 'm']:
            # if the character is wide it isn't indented from the left of the box to make it fit better
            charPosX = self.rectangle.left
        elif self.char in BytePairEncoding.ENCODINGCHARS:
            charPosX = self.rectangle.left - fontSize//12
        else:
            # regularly sized characters are indented slightly rightwards to appear central in the string
            charPosX = self.rectangle.topleft[0] + self.rectangle.width//6
        charPosY = self.rectangle.topleft[1] + self.rectangle.height//8
        # sets the position (top left) from which to render the character
        pygame.display.get_surface().blit(font.render(
            self.char, True, white), (charPosX, charPosY))

    def highlight(self, colour=red, thickness=1):
        """method to highlight a char object"""
        pygame.draw.rect(pygame.display.get_surface(),
                         colour, self.rectangle, thickness)

    def unhighlight(self):
        pygame.draw.rect(pygame.display.get_surface(),
                         white, self.rectangle, 1)


class pointer(objectInterface):
    """a class of functions relating to the pointer head (red arrow) which moves along the string"""

    def __init__(self, arrowImage):
        arrowWidth = pygame.display.get_surface().get_width()//15
        arrowHeight = pygame.display.get_surface().get_height()//8
        self.image = arrowImage
        self.image = pygame.transform.scale(
            self.image, (arrowWidth, arrowHeight))
        self.rect = self.image.get_rect()
        self.position = self.rect.topright
        self.headPos = self.rect.midbottom
        self.currentCharIndex = None
        self.draw()

    def draw(self):
        pygame.display.get_surface().blit(self.image, self.position)

    def unDraw(self):
        #self.rect.topleft = self.position
        #pygame.draw.rect(pygame.display.get_surface(), backgroundColour, self.rect)
        deleteObj(self)

    # explain the move function in implementation - rounding and discrete math
    def move(self, destinationPos, time=1):
        """method to smoothly move pointer from one position to another in a given time interval"""
        remainingTravel = (
            destinationPos[0]-self.headPos[0], destinationPos[1]-self.headPos[1])
        # per frame velocity calculated so that it will travel to the point within the given time
        perFrameVel = (math.ceil(
            remainingTravel[0]/(time*FPS)), math.ceil(remainingTravel[1]/(time*FPS)))

        moved = False
        ticks = 0
        clock = pygame.time.Clock()
        addObj(self)
        while not moved:
            # clock tick needs to be before object is removed - so it is visible on screen whilst moving
            clock.tick(FPS)
            deleteObj(self)
            if ticks == time*FPS or (sepDist(remainingTravel, perFrameVel) < (abs(perFrameVel[0]) + abs(perFrameVel[1]))):
                # if the current "distance" between points is smaller than the next we stop moving the pointer and snap it into place
                moved = True
                break
            remainingTravel = (
                destinationPos[0]-self.headPos[0], destinationPos[1]-self.headPos[1])
            velocity = (int(remainingTravel[0]//(time*FPS - ticks)),
                        int(remainingTravel[1]//(time*FPS - ticks)))
            self.position = (
                self.position[0] + velocity[0], self.position[1] + velocity[1])
            self.rect.topleft = self.position
            ticks += 1
            self.headPos = self.rect.midbottom
            addObj(self)
            drawScreen()
        self.headPos = destinationPos
        self.rect.midbottom = self.headPos
        self.position = self.rect.topleft
        self.draw()

    def moveToChar(self, stringObj):
        """method to move pointer to its current character on a given string"""
        destinationChar = stringObj.chars[self.currentCharIndex]
        self.move(destinationChar.rectangle.midtop, 0.1)
        destinationChar.highlight()


def sepDist(a, b):
    """simple function to give a somewhat seperation distance between two co-ordinates (sum of x and y distances)"""
    # using the sum of x and y distances is much computationally faster than pythagoras (no square and sqrt, especially the latter) whilst still serving its purpose
    return abs(a[0]-b[0]) + abs(a[1] - b[1])


def validateInputStr(inputStr, algorithm):
    if len(inputStr) == 0:
        return False
    if algorithm == "Byte Pair Encoding":
        for char in BytePairEncoding.ENCODINGCHARS:
            if char in inputStr:
                return False
        return True
    elif algorithm == "Run Length Encoding":
        for digitChar in RunLengthEncoding.digits:
            if digitChar in inputStr:
                return False
        return True
    elif algorithm == "Lempel Ziv 1977":
        return True
    elif algorithm == "Huffman Encoding":
        return True
    else:
        raise Exception("no valid algorithm chosen")
        return False


def drawInput(enteredString):
    """function which will display the input text onto the input box"""

    # font size only constrained by height for input (thin rectangle)
    fontSize = int(INPUTRECT.rect.height//1.5)
    maxLength = int(INPUTRECT.rect.width//(0.85*fontSize+1))
    # the input will only contain the ending substring which fits in the INPUTRECT
    if len(enteredString) > maxLength:
        outputString = enteredString[-maxLength:]
    else:
        outputString = enteredString
    INPUTRECT.text = outputString


def drawInfo(stringArray):
    """function which will display the info text onto the information box"""
    INFORECT.stringArray = stringArray
    # redraws the INFORECT without text
    pygame.draw.rect(pygame.display.get_surface(),
                     INFORECT.colour, INFORECT.rect)
    numLines = len(stringArray)
    lineHeight = int(INFORECT.rect.height//(numLines+1))
    longestStrInArr = len(max(stringArray, key=len))
    # textposition is indented from topleft corner
    textPos = (INFORECT.rect.topleft[0] + INFORECT.rect.width //
               16, INFORECT.rect.topleft[1] + lineHeight//4)
    # gives an appropriate font size for the displayed string
    fontSize = int(
        min(0.75*lineHeight, 2*INFORECT.rect.width//longestStrInArr))
    # compression font used as it needs to be able to display encoding characters
    font = pygame.font.Font(compressionFont, fontSize)
    for i in range(numLines):
        # draws each string in the array to the box on an individual line
        text = font.render(stringArray[i], True, black)
        pygame.display.get_surface().blit(
            text, (textPos[0], textPos[1] + lineHeight*i))


def drawScreen():
    """function which draws every object in ALLOBJECTS onto the screen """
    pygame.display.get_surface().fill(
        backgroundColour)  # redraws backround to 'erase' everything
    for object in ALLOBJECTS:
        object.draw()
    pygame.display.update()


def addObj(newObj):
    """add a given object to the ALLOBJECTS list meaning it is now on screen"""
    ALLOBJECTS.append(newObj)


def deleteObj(remObj):
    """remove a given object to the ALLOBJECTS list meaning it is now not on screen"""
    ALLOBJECTS.remove(remObj)


def clearCompressionRect():
    """function which removes compressionStrings from the objects list and then draws the screen - clearing the compressionRect"""
    i = 0
    finished = False
    while not finished:
        if i == len(ALLOBJECTS):
            # breaks when end of list is reached
            finished = True
            break
        object = ALLOBJECTS[i]
        if isinstance(object, compressionString):
            # if the object is a compression string we remove it (and also backtrack an index so to not miss an object as the list has "shuffled down")
            deleteObj(object)
            i -= 1
        i += 1
    drawScreen()


def showPseudoCode():
    algorithm = ALGSELECTION.getSelected()
    if algorithm == None:
        COMMENTRECT.changeStr(
            "You need to select an algorithm first before you can see its Pseudocode.")
        drawScreen()
        return None
    elif algorithm == "Run Length Encoding":
        pseudocode = pygame.image.load(os.path.join('assets', 'pseudoRLE.png'))
    elif algorithm == "Byte Pair Encoding":
        pseudocode = pygame.image.load(
            os.path.join('assets', 'pseudoBytePair.png'))
    elif algorithm == "Lempel Ziv 1977":
        pseudocode = pygame.image.load(
            os.path.join('assets', 'pseudoLZ77.png'))
    elif algorithm == "Huffman Encoding":
        pseudocode = pygame.image.load(
            os.path.join('assets', 'pseudoHuffman.png'))
    else:
        return None

    scaling = min(pygame.display.get_surface().get_width()/pseudocode.get_width(),
                  pygame.display.get_surface().get_height()/pseudocode.get_height())
    pseudocode = pygame.transform.scale(pseudocode, (int(
        pseudocode.get_width()*scaling), int(pseudocode.get_height()*scaling)))
    XPos = int(
        0.5*(pygame.display.get_surface().get_width() - pseudocode.get_width()))
    pygame.display.get_surface().blit(pseudocode, (XPos, 0))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # if the quit button (X) is hit we end the program
                print("you quitted")
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    guiSetup()
                    return None


def guiSetup():
    """function to setup GUI (to allow handling of window resizing)"""
    global INPUTRECT, CLEARTEXTBUTTON, ANIMATIONSPEEDSLIDER, ANIMATIONSPEEDVALUE, COMPRESSIONRECT, INFORECT, COMMENTRECT, ALGSELECTION, ALLOBJECTS, MAINARROW, SHOWCODEBUTTON  # graphical objects have to be global :(
    ALLOBJECTS = []

    # setting up input (input and clear rectangles)

    # INPUTRECT setup
    inputRect = pygame.Rect(0, 0, int(pygame.display.get_surface(
    ).get_width()//1.5), pygame.display.get_surface().get_height()//20)
    inputRect.center = (pygame.display.get_surface().get_width(
    )//2, pygame.display.get_surface().get_height()//20)
    INPUTRECT = textRegionRect(inputRect, "Enter text to be compressed here:",
                               infoRectColour, inputRect.height)  # creating INPUTRECT object
    addObj(INPUTRECT)

    # CLEARTEXTBUTTON setup
    CLEARTEXTBUTTON = Button(pygame.display.get_surface(), pygame.display.get_surface().get_width()-pygame.display.get_surface().get_width()//10, 0, pygame.display.get_surface().get_width()//10, pygame.display.get_surface(
    ).get_height()//15, inactiveColour=(100, 1, 150), hoverColour=(140, 15, 205), pressedColour=(225, 50, 255), text="Clear Text", fontSize=pygame.display.get_surface().get_height()//25, onClick=lambda: clearCompressionRect())
    addObj(CLEARTEXTBUTTON)

    # ANIMATIONSPEEDSLIDER setup
    ANIMATIONSPEEDSLIDER = Slider(pygame.display.get_surface(), inputRect.bottomleft[0], inputRect.bottomleft[1]+(pygame.display.get_surface(
    ).get_height()//64), pygame.display.get_surface().get_width()//2, pygame.display.get_surface().get_height()//32, min=0.1, max=2, step=0.05, initial=1)
    addObj(ANIMATIONSPEEDSLIDER)

    # ANIMATIONSPEEDVALUE setup
    animationSpeedValueRect = pygame.Rect(ANIMATIONSPEEDSLIDER._x - ANIMATIONSPEEDSLIDER._height*5,
                                          ANIMATIONSPEEDSLIDER._y, ANIMATIONSPEEDSLIDER._height*4, ANIMATIONSPEEDSLIDER._height)
    ANIMATIONSPEEDVALUE = textRegionRect(
        animationSpeedValueRect, "Speed = " + str(ANIMATIONSPEEDSLIDER.getValue()), colour=white)
    addObj(ANIMATIONSPEEDVALUE)

    # SHOWCODEBUTTON setup
    SHOWCODEBUTTON = Button(pygame.display.get_surface(), pygame.display.get_surface().get_width()//16, 0, pygame.display.get_surface().get_width()//10, pygame.display.get_surface(
    ).get_height()//16, inactiveColour=(100, 1, 150), hoverColour=(140, 15, 205), pressedColour=(225, 50, 255), text="Show Pseudocode", fontSize=pygame.display.get_surface().get_height()//36, onClick=lambda: showPseudoCode())
    addObj(SHOWCODEBUTTON)
    # setting up compression and info space

    # COMPRESSIONRECT setup
    compressionRectSpaceX = 0
    compressionRectSpaceY = int(pygame.display.get_surface().get_height()//2.5)
    compressionRectSpaceWidth = int(
        pygame.display.get_surface().get_width()//1.3)
    compressionRectSpaceHeight = int(
        pygame.display.get_surface().get_height() - compressionRectSpaceY)
    compressionRectangle = pygame.Rect(
        compressionRectSpaceX, compressionRectSpaceY, compressionRectSpaceWidth, compressionRectSpaceHeight)
    COMPRESSIONRECT = regionRect(compressionRectangle)
    addObj(COMPRESSIONRECT)

    # INFORECT setup
    infoRect = pygame.Rect(COMPRESSIONRECT.rect.topright, (pygame.display.get_surface().get_width(
    ) - COMPRESSIONRECT.rect.width, pygame.display.get_surface().get_height()-COMPRESSIONRECT.rect.top))
    INFORECT = textRegionRect(infoRect, "")
    INFORECT.stringArray = ["Compression Info: "]
    addObj(INFORECT)

    # COMMENTRECT setup
    commentRect = pygame.Rect(COMPRESSIONRECT.rect.left, COMPRESSIONRECT.rect.top - int(pygame.display.get_surface(
    ).get_height()//3.7), pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()//24)
    COMMENTRECT = textRegionRect(
        commentRect, "here is where comments will go", darkGrey, white, int(0.9*commentRect.height))
    addObj(COMMENTRECT)

    # ALGSELECTION setup
    ALGSELECTION = Dropdown(pygame.display.get_surface(), int(pygame.display.get_surface().get_width()/1.2), commentRect.bottom, pygame.display.get_surface().get_width()//6, pygame.display.get_surface().get_height()//24, "Algorithm Choice", [
                            "Run Length Encoding", "Byte Pair Encoding", "Huffman Encoding", "Lempel Ziv 1977"], inactiveColour=(153, 255, 170), hoverColour=(51, 255, 255), pressedColour=(255, 119, 51), fontSize=pygame.display.get_surface().get_height()//32)
    addObj(ALGSELECTION)

    # MAINARROW setup
    arrowImage = pygame.image.load(os.path.join('assets', 'pointer.png'))
    MAINARROW = pointer(arrowImage)
    addObj(MAINARROW)

    drawScreen()
    MAINARROW.move((pygame.display.get_surface().get_width() //
                   32, MAINARROW.rect.height), 0.1)


def checkQuit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("you quitted")
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
    return False

# algorithms ↓

def visualiseRLE(compressionStringObj, MAINARROW, animationSpeed=0.5):
    """function which visualises the application of Run Length Encoding to a string"""
    clock = pygame.time.Clock()
    uncompressedText = compressionStringObj.text
    # inputted object is deleted (so it is not drawn anymore) once its text is stored
    deleteObj(compressionStringObj)
    # uncompressed text object created at top of COMPRESSIONRECT
    uncompressedObj = compressionString(uncompressedText, 0)
    addObj(uncompressedObj)
    compressedText = ""
    # compressed text object created at bottom of COMPRESSIONRECT
    compressedObj = compressionString(compressedText, 1)
    addObj(compressedObj)
    drawScreen()

    currentIndex = 0
    currentCharCount = 1
    lastChar = False
    while not lastChar:
        # sets up the visual for the current state the algorithm is in
        clock.tick(animationSpeed)
        MAINARROW.currentCharIndex = currentIndex
        currentCharObj = uncompressedObj.chars[currentIndex]
        MAINARROW.moveToChar(uncompressedObj)
        currentChar = uncompressedText[currentIndex]
        info = [f"Index = {currentIndex}  ('{currentChar}')",
                f"current sequential chars  = {currentCharCount}"]

        drawScreen()  # draw screen needs to occur before highlighting
        drawInfo(info)
        # chars is current "run" are highlighted
        uncompressedObj.highlightChars(
            currentIndex-(currentCharCount-1), currentIndex, blue)
        currentCharObj.highlight()  # current char object is highlighted
        pygame.display.update()

        if currentIndex + 1 == len(uncompressedText):
            lastChar = True
            COMMENTRECT.changeStr(
                "final character reached, adding encoding and ending iteration")
            compressedText += RunLengthEncoding.digits[currentCharCount] + currentChar
            compressedText = compressedText.replace("1", "")
        elif currentChar == uncompressedText[currentIndex + 1]:
            currentCharCount += 1
            COMMENTRECT.changeStr("next character matches so extending run")
        else:
            compressedText += RunLengthEncoding.digits[currentCharCount] + currentChar
            currentCharCount = 1
            COMMENTRECT.changeStr("run broke, adding new encoding ")
            compressedText = compressedText.replace("①", "")
        compressedObj.changeStr(compressedText)
        pygame.display.update()
        if checkQuit():
            guiSetup()
            COMMENTRECT.changeStr("Cancelled RunLengthEncoding")
            return
        currentIndex += 1
    drawScreen()
    start = time.time()
    RunLengthEncoding.RLE(uncompressedText)
    end = time.time()
    executionTime = GeneralFunctions.roundToSF(end-start, 4)
    compressionRatio = GeneralFunctions.roundToSF(
        GeneralFunctions.compressionRatio(uncompressedText, compressedText)*100, 3)
    executedInfo = [f"Achieved compression ratio {compressionRatio}%", f"Algorithm completed in {executionTime} seconds",
                    "RLE has linear - O(n) - time complexity", "RLE also has linear - O(n) - space complexity"]
    drawInfo(executedInfo)


def visualiseBytePairEncoding(compressionStrObj, animationSpeed=0.5):
    clock = pygame.time.Clock()
    uncompressedText = compressionStrObj.text
    clearCompressionRect()
    compressionObj = compressionString(uncompressedText, 0.5)
    addObj(compressionObj)
    drawScreen()
    encodingDict = {}
    encodingChars = BytePairEncoding.ENCODINGCHARS
    # a list of all the characters i can use to encode a byte pair
    startingArray = ["Encoding Dict: ↓"]
    currentEncodingChar = 0
    compressible = True
    while compressible:
        drawScreen()
        # pair stores most common pair and their frequency
        pair = BytePairEncoding.getMostCommonPair(
            compressionObj.text, encodingDict)
        # if the freqency of the pair is 1 (or 0) we end the encoding as it is not worth compressing
        if pair[1] <= 1:
            compressible = False
            COMMENTRECT.changeStr(
                "encoding finished, string is no longer compressible")
            break
        # if we run out of encoding chars we must end compression
        elif currentEncodingChar >= len(encodingChars)-1:
            compressible = False
            COMMENTRECT.changeStr(
                "encoding finished - ran out of characters to use to encode bytes")
            break

        bytePair = pair[0]
        replacement = encodingChars[currentEncodingChar]
        encodingDict[replacement] = bytePair
        bytePairIndexes = GeneralFunctions.indexesOfSubstring(
            compressionObj.text, bytePair)
        COMMENTRECT.changeStr(
            f"most common byte pair in string '{bytePair}' to be encoded with '{replacement}'")
        encodingDictStrArr = str(encodingDict).split(",")
        if len(encodingDictStrArr)>2:
            for i in range(len(encodingDictStrArr)-1):
                encodingDictStrArr[i] += ","
        stringArray = startingArray + encodingDictStrArr
        drawInfo(stringArray)
        drawScreen()
        clock.tick(animationSpeed/2.5)
        # reverses indexes so we can remove them sequentially
        bytePairIndexes.sort(reverse=True)
        for index in bytePairIndexes:
            COMMENTRECT.changeStr(
                f"replacing bytePair '{bytePair}' at {index} with encoding '{replacement}'")
            COMMENTRECT.draw()
            compressionObj.draw()
            compressionObj.highlightChars(index, index+len(bytePair), green)
            pygame.display.update()
            compressionObj.chars = compressionObj.chars[:index] + [
                compressionStringChar(replacement)] + compressionObj.chars[index+len(bytePair):]
            compressionObj.text = compressionObj.text[:index] + \
                replacement + compressionObj.text[index+len(bytePair):]
            clock.tick((FPS*animationSpeed)/64)
            clearCompressionRect()
            if checkQuit():
                guiSetup()
                COMMENTRECT.changeStr("Cancelled BytePairEncoding")
                return
        currentEncodingChar += 1
        addObj(compressionObj)
    start = time.time()
    compressedText = BytePairEncoding.bytePairEncode(uncompressedText)[0]
    end = time.time()
    executionTime = GeneralFunctions.roundToSF(end-start, 4)
    compressionRatio = GeneralFunctions.roundToSF(
        GeneralFunctions.compressionRatio(uncompressedText, compressedText)*100, 3)
    try:
        stringArray = [f"Achieved compression ratio of {compressionRatio}%",
                       f"Algorithm completed in {executionTime}s"] + stringArray
    except:
        stringArray = [
            "no compression occured (ratio 100%)", f"Algorithm completed in {executionTime}s"]
    stringArray += ["BytePairEncoding has linear - O(n) - time complexity",
                    "BytePairEncoding has logarithmic - O(log[n]) - space complexity"]
    drawInfo(stringArray)


def visualiseLZ77(compressionStrObj, MAINARROW, animationSpeed):
    clock = pygame.time.Clock()
    COMMENTRECT.changeStr("Visuals for LZ77 not implemented yet")
    uncompressed = compressionString(compressionStrObj.text, 0)
    addObj(uncompressed)
    deleteObj(compressionStrObj)
    drawScreen()
    MAINARROW.currentCharIndex = 0
    MAINARROW.moveToChar(uncompressed)
    clock.tick(animationSpeed)
    start = time.time()
    compressedStr = LempelZiv77.LZ77(uncompressed.text, 256, 16, 2)
    end = time.time()
    compressed = compressionString(compressedStr, 1)
    addObj(compressed)
    drawScreen()
    compressionRatio = GeneralFunctions.roundToSF(GeneralFunctions.compressionRatio(
        uncompressed.text, compressed.text.replace("}", "").replace("{", ""))*100, 3)
    COMMENTRECT.changeStr(
        "Compression ratio doesn't consider curly braces (not used in non visual implementation)")
    executionTime = GeneralFunctions.roundToSF(end-start, 4)
    INFORECT.stringArray = [f"Achieved compression ratio {compressionRatio}%", f"Algorithm completed {executionTime}s",
                            "Memory length of 256 characters", "Lookahead length 16 character", "LZ77 has quadratic - O(n^2) - time complexity", "LZ77 has linear - O(n) - space complexity"]
    drawScreen()


def visualiseHuffman(compressionStrObj, MAINARROW, animationSpeed):
    clock = pygame.time.Clock()
    COMMENTRECT.changeStr(f"Visuals for Huffman encoding not implemented yet")
    uncompressedText = compressionStrObj.text
    deleteObj(compressionStrObj)
    uncompressed = compressionString(uncompressedText, 0)
    addObj(uncompressed)
    drawScreen()
    MAINARROW.currentCharIndex = 0
    MAINARROW.moveToChar(uncompressed)
    clock.tick(animationSpeed)
    start = time.time()
    huffman = HuffmanEncoding.huffmanEncode(uncompressedText)
    end = time.time()
    compressedBinary = huffman[0]
    root = huffman[1]
    compressedText = GeneralFunctions.convertBinstringToString(
        compressedBinary)
    huffmanCodes = HuffmanEncoding.calculateCodes(root)
    compressed = compressionString(compressedText, 1)
    addObj(compressed)
    startingArray = ["Huffman Codes: ↓ "]
    huffmanCodesStrArr = str(huffmanCodes).split(",")
    if len(huffmanCodesStrArr)>1:
        for i in range(len(huffmanCodesStrArr)-1):
            huffmanCodesStrArr[i] += ","
    stringArray = startingArray + huffmanCodesStrArr
        
    drawInfo(stringArray)
    compressionRatio = GeneralFunctions.roundToSF(
        GeneralFunctions.compressionRatio(uncompressedText, compressedText)*100, 3)
    executionTime = GeneralFunctions.roundToSF(end-start, 4)
    INFORECT.stringArray += ["(notice more common characters have shorter encodings)",
                             f"Achieved compression ratio {compressionRatio}%", f"Algorithm completed {executionTime}s", "Huffman Encoding has log linear - O(nlog[n]) - time complexity", "Huffman encoding has linear - O(n) - space complexity"]
    COMMENTRECT.changeStr(
        "resulting string is the huffman codes converted back to text")
    drawScreen()


def main():
    guiSetup()
    drawScreen()
    # initialising variables
    inputActive = False
    compressionActive = False
    running = True
    clock = pygame.time.Clock()
    enteredString = compressionString("")
    #stringArray = input("enter strings separated by commas:\n").split(",")
    # drawInfo(stringArray)

    def checkEvents():
        """function which responds to inputs from the user"""
        nonlocal inputActive
        nonlocal enteredString
        nonlocal compressionActive
        animationSpeed = ANIMATIONSPEEDSLIDER.getValue()
        algorithm = ALGSELECTION.getSelected()
        ANIMATIONSPEEDVALUE.changeStr(
            "Speed = " + str(GeneralFunctions.roundToSF(animationSpeed, 3)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # if the quit button (X) is hit we end the program
                print("you quitted")
                pygame.quit()
                sys.exit()

            if inputActive and event.type == pygame.KEYDOWN:
                # handles input keypresses
                if event.key == pygame.K_RETURN:
                    # ends input when user presses return (enter)
                    inputActive = False
                    INPUTRECT.colour = inputPassiveColour
                    if algorithm == None:
                        COMMENTRECT.changeStr(
                            "No algorithm selected - cannot perform visualisation")
                        drawScreen()
                    elif not enteredString.isEmpty():
                        addObj(enteredString)
                        drawScreen()
                        MAINARROW.move(
                            enteredString.chars[0].rectangle.midtop, 0.1*animationSpeed)
                        MAINARROW.currentCharIndex = 0
                        compressionActive = True
                        if validateInputStr(enteredString.text, algorithm):
                            if algorithm == "Byte Pair Encoding":
                                visualiseBytePairEncoding(
                                    enteredString, animationSpeed)
                            elif algorithm == "Run Length Encoding":
                                visualiseRLE(
                                    enteredString, MAINARROW, animationSpeed)
                            elif algorithm == "Lempel Ziv 1977":
                                visualiseLZ77(
                                    enteredString, MAINARROW, animationSpeed)
                            elif algorithm == "Huffman Encoding":
                                visualiseHuffman(
                                    enteredString, MAINARROW, animationSpeed)
                            else:
                                COMMENTRECT.changeStr("Something went wrong")
                                drawScreen()
                        else:
                            COMMENTRECT.changeStr(
                                f"the string you entered was invalid for {algorithm} - please try again")
                            drawScreen()

                elif event.key == pygame.K_ESCAPE:
                    # cancels user input when the escape character is pressed
                    inputActive = False
                    INPUTRECT.colour = inputPassiveColour
                    drawScreen()
                    enteredString.chars = []
                    print("text input terminated")

                elif event.key == pygame.K_BACKSPACE:
                    # removes last character (rather than adding a delete character which is default behaviour) when backspace pressed
                    enteredString.backspace()
                    drawInput(enteredString.text)

                else:
                    # adds the inputted character to the string
                    enteredString.addStr(event.unicode)
                    drawInput(enteredString.text)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if INPUTRECT.rect.collidepoint(event.pos):
                    # if the input box is clicked on we begin input and change the box's colour to indicate this
                    compressionActive = False
                    clearCompressionRect()
                    drawScreen()
                    if not inputActive:
                        inputActive = True
                        INPUTRECT.colour = inputActiveColor
                        INPUTRECT.text = ""
                    elif inputActive:
                        inputActive = False
                        INPUTRECT.colour = inputPassiveColour
                        INPUTRECT.text = "Enter text to be compressed here:"
            if event.type == pygame.VIDEORESIZE:
                guiSetup()
        pygame_widgets.update(pygame.event.get())

    while running:
        clock.tick(FPS)  # runs pygame at given framerate
        checkEvents()
        drawScreen()


if __name__ == "__main__":
    main()

# test rect to find places on screen - pygame.draw.rect(pygame.display.get_surface(), red, pygame.Rect(posx, posy, 20, 20))

# type up things.
