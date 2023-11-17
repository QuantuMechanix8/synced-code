# test string to be used for easily copying to encode something so that I dont have to type out a long string each time I test the program mid development, this should be sufficiently long to ensure that efficiency isn't a serious problem but still reasonably lengthed for ease of use; this will also contain all 10 different numbers and some symbols to ensure the program can handle these 987234675 "" .
import math
import random
import BytePairEncoding
import HuffmanEncoding
import RunLengthEncoding
import LempelZiv77


def roundToSF(number, SF):
    """function which rounds the input number to the given amount of significant figures"""
    # "decimal shifts" so that taking the desired SF is the same as 0DP 
    leftShift = (SF-1) - math.floor(math.log10(number))
    intNumber = number*(10**leftShift)
    intNumber = round(intNumber)
    return intNumber/(10**leftShift) # downshifting the number to be the correct 


def compressionRatio(uncompressed, compressed):
    # returns a simply fraction that indicates the size of the compressed text compared with its original - only works if both are in the same format
    return float(len(compressed))/(len(uncompressed))


def convertBinstringToString(binString):
    # converts a binary string to a string of characters (to allow for compression ratio calculations on huffman encoded text)
    asciiString = ""
    end = False
    while not end:
        if len(binString) <= 8:
            newChar = chr(int(binString, 2))
            if newChar == "\0":
                print("null character found")
                newChar = " "
            asciiString += newChar
            return asciiString
        else:
            newChar = chr(int(binString[0:8], 2))
            if newChar == "\0":
                print("null character found")
                newChar = " "
            asciiString += newChar
            binString = binString[8:]
    return asciiString


def convertStringToBinstring(string):
    binString = ""
    for char in string:
        binString += format(ord(char), 'b')
    return binString


def getUserInputString(illegalChars = {}, maxLength = 1024):
    uncompressedString = input("Please enter a string:\n")
    for illegalChar in illegalChars:
        if illegalChar in uncompressedString:
            print(f"illegal character '{illegalChar}' in your string - please enter a different string")
            uncompressedString = getUserInputString()
    if len(uncompressedString)>maxLength:
        print(f"\nyou entered {len(uncompressedString)} chars, which is too long, please enter a shorter one (up to {maxLength} chars)\n")
        uncompressedString = getUserInputString()
    return uncompressedString


def indexesOfSubstring(string, substring):
    """Returns a list of the starting indexes of the substring in the string"""
    matchIndexes = []
    substringIndex = 0
    for index, char in enumerate(string):
        if char == substring[substringIndex]:
            substringIndex += 1
            if substringIndex == len(substring):
                matchIndexes.append(index+1-substringIndex)
                substringIndex = 0
        else:
            substringIndex = 0
    return matchIndexes    


def removeIndexesFromArray(array, removalIndexes):
    """removes set of indexes from array"""
    removalIndexes.sort(reverse=True)
    for removalIndex in removalIndexes:
        if removalIndex > len(array)-1:
            raise Exception(f"removal index '{removalIndex}' was outside of array")
        else:
            array.pop(removalIndex)
    return array
    
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

if __name__ == "_main__":
    pass
