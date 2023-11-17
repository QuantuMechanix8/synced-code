POINTERCHARS= {'{', '}', '0','1', '2','3','4','5','6','7','8','9'}

def getMatchIndexes(firstStr, secondStr):
    """Finds the longest matching substring in the two arrays (strings) and returns the start and end indexes of this match (from the first array) as well as the length of the match i.e. (firstStrMatchStartIndex, secondStrMatchStartIndex, matchLength) """
    global POINTERCHARS
    longestMatch = 0
    currentMatchLen = 0
    firstStrLongestMatchEnd = 0
    secondStrLongestMatchEnd = 0
    # initialises values that will be modified in loops
    for firstStrIndex in range(len(firstStr)-1):
        for secondStrIndex in range(len(secondStr)):
            # iterates over each item in the first array and then checks if the subarray after this item matches any in the second array
            firstStrChar = firstStr[firstStrIndex]
            secondStrChar = secondStr[secondStrIndex]
            # gets the value of the list items currently being checked (helped for debugging also)
            if firstStrChar in POINTERCHARS or secondStrChar in POINTERCHARS:
                # if we reach part of a pointer the match will break as we cannot reference a pointer.
                #print(f"reached pointer - firstStrChar is '{firstStrChar}' and second is '{secondStrChar}'")
                if currentMatchLen>longestMatch:
                    longestMatch = currentMatchLen
                    firstStrLongestMatchEnd = firstStrIndex
                    secondStrLongestMatchEnd = secondStrIndex
                    firstStrIndex -= currentMatchLen
                currentMatchLen = 0
                break
            elif firstStrChar == secondStrChar:
              firstStrIndex += 1
              currentMatchLen += 1
              # if the Characters match then we move onto the next character to see if this matching substring continuesC- note that we have to manually increase the firstStrIndex
              if firstStrIndex == len(firstStr):
                  break
                  # If we have reached the end of the firstStr then we break out of the loop (check not needed for secondStr as we are looping over it - but manually iterating through firstStr)
            else:
                if currentMatchLen>longestMatch:
                    longestMatch = currentMatchLen
                    firstStrLongestMatchEnd = firstStrIndex
                    secondStrLongestMatchEnd = secondStrIndex
                    firstStrIndex -= currentMatchLen
                    # if our current match is longer than the held longestMatch we update it (as we have reached the end of the match) and return firstStrIndex back to where it "was" manually (to check for any other matching substrings starting at this character)
                currentMatchLen = 0
        if currentMatchLen>longestMatch:   
            # case where match doesn't end before finishing secondStr iteration - same process as reaching the end of the match
            longestMatch = currentMatchLen
            firstStrLongestMatchEnd = firstStrIndex
            secondStrLongestMatchEnd = secondStrIndex+1
            firstStrIndex -= currentMatchLen
        currentMatchLen = 0
    # converts the indexes for match ends to be indexes for match starts (this is more useful) and returns as a tuple
    return (firstStrLongestMatchEnd-longestMatch, secondStrLongestMatchEnd-longestMatch, longestMatch)

def insertLZ77Pointer(text, referenceStartIndex, matchStartIndex, matchLen):
    relativeJump = matchStartIndex - referenceStartIndex
    pointerStr = "{" + str(relativeJump) + "," + str(matchLen) + "}"
    newText = text[:matchStartIndex] + pointerStr + text[matchStartIndex+matchLen:]
    # copies the text before and after the match and inserts the pointer inbetween
    return newText


def getMemory(text, pos, memoryLength):
    fullMemory = text[:pos]
    if len(fullMemory)<=memoryLength:
        return fullMemory
    else:
        return text[pos-memoryLength:pos]


def getLookahead(text, pos, lookAheadLength):
    fullLookahead = text[pos:]
    if len(fullLookahead)<=lookAheadLength:
        return fullLookahead
    else:
        return fullLookahead[:lookAheadLength]


def pointerNextMatch(text, memoryLength, lookAheadLength, shortestMatch = 2, startIndex = 0):
    compressedText = text
    largestMatchFound = False
    finished = False
    currentIndex = startIndex
    largestMatch = {"match" : [0,0,0], "matchIndex" : 0, "referenceIndex" : 0} # holds 
    localMax = True
    while not largestMatchFound:
        localMax=True
        if currentIndex == len(compressedText):
            return False
        memory = getMemory(text, currentIndex, memoryLength)
        lookAhead = getLookahead(text, currentIndex, lookAheadLength)
        #print(f"current memory is \n'{memory}'\n and current lookahead is \n'{lookAhead}'")
        matches = getMatchIndexes(memory, lookAhead)
        if matches[2]>largestMatch["match"][2]:
            localMax = False
            largestMatch["match"] = matches
            largestMatch["matchIndex"] = currentIndex+matches[1]
            largestMatch["referenceIndex"] = currentIndex-(len(memory)-matches[0])
            #matchText = memory[matches[0]:matches[0]+matches[2]]    
        if largestMatch["match"][2]>=shortestMatch and localMax:
            largestMatchFound = True
            # if our index is the last then this will be the final iteration
        currentIndex +=1
    matchLen = largestMatch["match"][2]
    matchIndex = largestMatch["matchIndex"]
    #print(f"longest match found was '{text[matchIndex:matchIndex+matchLen]}'")
    referenceIndex = largestMatch["referenceIndex"]
    compressedText = insertLZ77Pointer(compressedText, referenceIndex, matchIndex, matchLen)
    return compressedText
        

def LZ77(text, memoryLength = 4095, lookAheadLength = 15, shortestMatch = 3):
    compressedText = text
    complete = False
    while not complete:
        try:
            lastPointer = compressedText.rindex("}")
        except:
            lastPointer = 0
        newText = pointerNextMatch(compressedText, memoryLength, lookAheadLength, shortestMatch, lastPointer)
        if not newText:
            return compressedText
        else:
            compressedText = newText


def decodeLZ77(compressedText):
    uncompressedText = compressedText
    currentPointer = ""
    currentPointerStr = ""
    currentPointerStart = 0
    currentPointerEnd = 0
    for i in range(len(compressedText)-1, 0, -1): # decompresses backwards to undo pointers
        currentChar = compressedText[i]
        if currentChar == "}": # reached the end of a pointer
            currentPointerEnd = i
        if currentChar == "{": # reached the start of a pointer:
            currentPointerStart = i
            currentPointer = uncompressedText[currentPointerStart:currentPointerEnd+1]
            uncompressedText = uncompressedText[:currentPointerStart] + getPointerStr(uncompressedText, i,currentPointer) + uncompressedText[currentPointerEnd+1:]
            print(uncompressedText)
            

def getPointerStr(text, index, pointer):
    pointer = pointer.split(",")
    relativeJump = int(pointer[0].strip("{"))
    Length = int(pointer[1].strip("}"))
    referenceStart = index-relativeJump
    return text[referenceStart:referenceStart+Length]
    
    
theLordHathSpoken = "Greeting. Yee Thee who be of GODLY BEING. A brief explanation of energy centres of you as the SPIRIT. How to open all your sha-kras and heal your own DNA and how to connect to the Universe. Energy-centres from lowest to highest, above, for Ones well being the the FORM of Physical and Spiritual. Each energy-sphere has a certain sound (frequency = Hz) of music that they vibrate on and when you MAKE THE SAME SOUND IN YOUR MIND THAT YOU ARE HEARING while listening to the sound while meditating or just listening with headphones to get maximum effect and tuning the sound into your MIND. You can also listen all of the frequencies at the same time, but first listen to them one at the time. WITH GREAT POWER COMES GREAT RESPONSIBILITY. As SPIRIT in a PHYSICAL FORM, is a BEING of FREQUENCY of HARMONIOUS SOUND can make items vibrate with their MIND, by learning the SOUND for their MIND, for benefit of OTHERS and your-SELF by creating the frequency of the Hz above with your MIND and then directing it to an ITEM or another BEING. One can create their own energy by learning of the start tetrahedron after the physical form or while in the physical FORM*turning negativity into positivity*. Making the STAR from MIND and counter-rotating hedrons*circling the angles* and using the STAR from through the energy-centres chakras from lower to the MIND's EYE. Centre of your SEAT is where the STAR is located."
testString = "repeating string has repeats in a string"

if __name__ == "__main__":
    #here is the place to code tests for this file specifically - wont run when imported
    print(LZ77(testString))
    #decodeLZ77("this {3,3}a repeated string, so {32,5}can have{18,3}me {40,6}{37,3} matches")
    