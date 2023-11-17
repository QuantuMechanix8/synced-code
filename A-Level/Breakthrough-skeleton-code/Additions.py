# camel case used to match Breakthrough convention
import math
import random


def perfectRiffle(array):
    split = math.ceil(len(array)/2)
    leftArr = array[:split]
    rightArr = array[split:]
    finalArr = []
    leftHalf = True
    for i in range(len(array)):
        if leftHalf:
            finalArr.append(leftArr.pop(0))
        else:
            finalArr.append(rightArr.pop(0))
        leftHalf = not leftHalf
    return finalArr


def riffle(array):
    split = math.ceil(len(array)/2)
    leftHalf = array[:split]
    rightHalf = array[split:]
    finalArr = []
    maxCardBunch = max(1, len(array)//8)
    complete = False
    leftPile = True
    while not complete:
        nextBunch = random.randint(1, maxCardBunch)
        if leftPile:
            finalArr += leftHalf[:nextBunch]
            leftHalf = leftHalf[nextBunch:]
        elif not leftPile:
            finalArr += rightHalf[:nextBunch]
            rightHalf = rightHalf[nextBunch:]
        leftPile = not leftPile
        if len(leftHalf) == 0 and len(rightHalf) == 0:
            complete = True
        elif len(leftHalf) == 0:
            leftPile = False
        elif len(rightHalf) == 0:
            leftPile = True
    return finalArr


def manyRiffle(array, iterations, perfect = False):
    currentArray = array
    for i in range(iterations):
        if perfect:
            currentArray = perfectRiffle(currentArray)
        else:
            currentArray = riffle(currentArray)
    return currentArray

def removeLastOccurrence(substring, text):
    reversedText = text[::-1]
    length = len(substring)
    for index in range(0, len(reversedText)-length):
        if reversedText[index : index+length] == substring:
            print(f"found at index {index}")
            return index
    return None
    # add 
    

myArr = [i for i in range(100)]
print(riffle(myArr))