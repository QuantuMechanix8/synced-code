import os
import GeneralFunctions
import time
ENCODINGCHARS = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩', '⑪', '⑫', '⑬', '⑭', '⑮', '⑯', '⑰', '⑱', '⑲', '⑳', '㉑', '㉒', '㉓', '㉔', '㉕', '㉖', '㉗', '㉘', '㉙', '㉚', '㉛', '㉜', '㉝', '㉞', '㉟', '㊱', '㊲', '㊳', '㊴', '㊵', '㊶', '㊷', '㊸', '㊹', '㊺', '㊻', '㊼', '㊽', '㊾', '㊿','❶', '❷', '❸', '❹', '❺', '❻', '❼', '❽', '❾', '❿','⓫', '⓬', '⓭', '⓮', '⓯', '⓰', '⓱', '⓲', '⓳', '⓴','㉈', '㉉', '㉊', '㉋', '㉌', '㉍', '㉎', '㉏','⑴', '⑵', '⑶', '⑷', '⑸', '⑹', '⑺', '⑻', '⑼', '⑽', '⑾', '⑿', '⒀', '⒁', '⒂', '⒃', '⒄', '⒅', '⒆', '⒇', 'Ⓐ', 'Ⓑ', 'Ⓒ', 'Ⓓ', 'Ⓔ', 'Ⓕ', 'Ⓖ', 'Ⓗ', 'Ⓘ', 'Ⓙ', 'Ⓚ', 'Ⓛ', 'Ⓜ', 'Ⓝ', 'Ⓞ', 'Ⓟ', 'Ⓠ', 'Ⓡ', 'Ⓢ', 'Ⓣ', 'Ⓤ', 'Ⓥ', 'Ⓦ', 'Ⓧ', 'Ⓨ', 'Ⓩ', 'ⓐ', 'ⓑ', 'ⓒ', 'ⓓ', 'ⓔ', 'ⓕ', 'ⓖ', 'ⓗ', 'ⓘ', 'ⓙ', 'ⓚ', 'ⓛ', 'ⓜ', 'ⓝ', 'ⓞ', 'ⓟ', 'ⓠ', 'ⓡ', 'ⓢ', 'ⓣ', 'ⓤ', 'ⓥ', 'ⓦ', 'ⓧ', 'ⓨ', 'ⓩ','🅐', '🅑', '🅒', '🅓', '🅔', '🅕', '🅖', '🅗', '🅘', '🅙', '🅚', '🅛', '🅜', '🅝', '🅞', '🅟', '🅠', '🅡', '🅢', '🅣', '🅤', '🅥', '🅦', '🅧', '🅨', '🅩','⒜', '⒝', '⒞', '⒟', '⒠', '⒡', '⒢', '⒣', '⒤', '⒥', '⒦', '⒧', '⒨', '⒩', '⒪', '⒫', '⒬', '⒭', '⒮', '⒯', '⒰', '⒱', '⒲', '⒳', '⒴', '⒵','🄰', '🄱', '🄲', '🄳', '🄴', '🄵', '🄶', '🄷', '🄸', '🄹', '🄺', '🄻', '🄼', '🄽', '🄾', '🄿', '🅀', '🅁', '🅂', '🅃', '🅄', '🅅', '🅆', '🅇', '🅈', '🅉','⓿','❶', '❷', '❸', '❹', '❺', '❻', '❼', '❽', '❾', '❿','⓫', '⓬', '⓭', '⓮', '⓯', '⓰', '⓱', '⓲', '⓳', '⓴','⓵', '⓶', '⓷', '⓸', '⓹', '⓺', '⓻', '⓼', '⓽', '⓾']

# list of all characters (259) i can use for encoding byte pairs - long list of unusual characters needed as it allows heavy compression (often around 50% for long text files such as Bee movie script) and are unlikely to be in any text being compressed


def getMostCommonPair(text, encodingDict):
    """function which returns the most common character pair in a string"""
    lastUsedIdenticalPair = 0
    pairDict = {}
    # initialise a dictionary with char-pairs as keys and their frequency as values
    i = 0
    while i < len(text) - 1:
        # iterates over entire string to check each pair
        first = text[i]
        second = text[i+1]
        currentPair = str(first + second)
        # gets the next character pair using getNextChar so that it will consider a pointer as a single char
        if currentPair in pairDict.keys():
            if currentPair[0] == currentPair[1]:
                if i-lastUsedIdenticalPair != 1:
                    lastUsedIdenticalPair = i
                    pairDict[currentPair] += 1
            else:
                pairDict[currentPair]+=1
            # increments frequency of a pair if it is "seen"
        else:
            pairDict[currentPair] = 1
            if currentPair[0] == currentPair[1]:
                lastUsedIdenticalPair = i
            # creates dictionary entry for pair if it is "new"
        i += 1
    mostCommon = max(
        pairDict, default=0, key=pairDict.get
    )  # returns the max key - but associated with the largest value
    return (mostCommon, pairDict[mostCommon]) # returns the most common pair and its value - so we can decide whether its worth encoding


def nextSubstringIndex(text, substring, encodingDict = {}):
    """function to find the first instance of a substring in a string"""
    fullMatch = len(substring)
    index = 0
    lengthMatched = 0
    finished = False
    while not finished:
        if lengthMatched == fullMatch:
            return index-lengthMatched
        nextTextChar = text[index]
        nextSubstrChar = substring[lengthMatched]
        if index == len(text)-1:
            return None # we have reached the end of the string without finding the substring
        elif nextTextChar == nextSubstrChar:
            lengthMatched+=1
        else:
            if lengthMatched>0:
                index -= lengthMatched
            lengthMatched = 0
        index += 1
    


def replaceSubStr(text, subStr, replacement):
    """function to replace (in position) all instances of a substring with a given replacement"""
    newText = text
    finished = False
    while not finished:
        nextIndex = nextSubstringIndex(newText, subStr) # gets the next index to be replaced
        if nextIndex != None:
            newText = newText[:nextIndex] + replacement + newText[
                (nextIndex + len(subStr)):]
            # inserts the replacement in place where the previous string used to be
        else:
            # means no substring was found and so we can end the function and return the newText
            finished = True
            return newText


def bytePairEncode(uncompressedText):
    compressionText = uncompressedText
    encodingDict = {}
    encodingChars = ENCODINGCHARS
    # a list of all the characters i can use to encode a byte pair
    currentEncodingChar = 0
    compressible = True
    while compressible:
        pair = getMostCommonPair(compressionText, encodingDict) #pair stores most common pair and their frequency
        if pair[1] <= 1: # if the freqency of the pair is 1 (or 0) we end the encoding as it is not worth compressing
            compressible = False
            break
        elif currentEncodingChar >= len(encodingChars)-1: # if we run out of encoding chars we must end compression
            print("ran out of encodingChars")
            compressible = False
            break
        
        bytePair = pair[0]
        replacement = encodingChars[currentEncodingChar]
        encodingDict[replacement] = bytePair
        bytePairIndexes = GeneralFunctions.indexesOfSubstring(compressionText, bytePair)
        bytePairIndexes.sort(reverse = True) # reverses indexes so we can remove them by index without changing the next's position
        for index in bytePairIndexes:
            compressionText = compressionText[:index] + replacement + compressionText[index+len(bytePair):]
        currentEncodingChar += 1
    return (compressionText, encodingDict)
    


def bytePairDecode(compressedText, encodingDict):
    for pair in encodingDict:
        compressedText = replaceSubStr(compressedText, pair, encodingDict[pair])
        # iterates through every key (encoding character) in the dictionary and replaces it with its value (meaning)
    return compressedText



# python3 BytePair.py
