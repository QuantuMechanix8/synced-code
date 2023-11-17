def CountOccurences(CountCharacter, text):
    """counts the number of occurences of a given character in the text"""
    count = 0
    for char in text:
        if char == CountCharacter:
            count += 1
    return count


def FrequencyDict(text):
    """gives the frequency of each character in the text as a hashmap, character -> freq"""
    characters = [chr(i) for i in range(128)]
    charDict = {}
    for char in characters:
        charDict[char] = CountOccurences(char, text)
    return charDict


def OrderCharsByFrequency(charFrequency):
    """gives list of characters in the string ordered by freqency (most to least)"""
    orderedChars = []
    for char in charFrequency:
        if charFrequency[char] == 0:
            continue
            # if the character doesn't appear in the string we can ignore it and so dont add it to the ordered list
        elif len(orderedChars) == 0:
            orderedChars.append(char)
            continue
            # if the list is empty we append the character to it
        # simple insertion sort for adding characters into the list
        for i, entry in enumerate(orderedChars):
            if i == len(orderedChars)-1:
                orderedChars.append(char)
                break
                # if the character is less frequent than all other characters currently in the list we append it to the end
            elif charFrequency[char] > charFrequency[entry]:
                orderedChars.insert(i, char)
                break
                # if the character is more frequent that this entry we insert it to this position in the list (infront of the entry)
            elif (charFrequency[char] <= charFrequency[entry]):
                continue
                # if the character is less frequent (or equally) than the current entry in the list we skip to the next item in the list to compare with it
    return orderedChars


class node:
    """class for each node object (used in huffman tree)"""
    def __init__(self, data, freq, right, left):
        self.data, self.freq, self.right, self.left = data, freq, right, left

    def setParents(self):
        """assign's the current node as the parent to its child nodes - so child nodes have attribute .parent which points to this node"""
        if not self.left.parent:
            self.left.parent = self
            self.left.setParents()
        if not self.right.parent:
            self.right.parent = self
            self.right.setParents()


def BuildHuffmanTree(text):
    """creates huffman tree from the given text"""
    connectedTree = False
    freqDict = FrequencyDict(text)
    descendingChars = OrderCharsByFrequency(freqDict)
    allNodes = [] # list of all nodes to be added to the tree (will contain composites)
    for char in descendingChars:
        allNodes.append(node(char, freqDict[char], None, None))
    while not connectedTree:
        left = allNodes[-1] # the least frequent character node
        right = allNodes[-2] # the second least frequent character node
        newNode = node(left.data + right.data,
                       left.freq + right.freq, right, left) # new node with composite character i.e. 'zx' and summed frequency made, with pointers to its left and right child nodes
        allNodes.append(newNode)
        allNodes.remove(left)
        allNodes.remove(right)
        # print debug for when nodes are combined: print("removed '" + left.data + "' and also '" + right.data + "'")
        if len(allNodes) == 1:
            # when there is only one node left we have clearly combined all nodes together and so can finish
            connectedTree = True
        allNodes.sort(key=lambda node: node.freq, reverse=True) # sorts list into descending frequency order
    return allNodes[0] # returns root of the tree (as the nodes all point to one another so entire tree can be accessed from root)


def calculateCodes(root):
    """calculates huffman codes for every character in the huffman tree (DFS)"""
    currentCode = ''
    allCodes = {}
    # inner function used so we can store currentCode and allCodes outside the recursion required to traverse the tree
    def calculateCode(node):
        """calculates the huffman code using tree traversal starting at the input node"""
        nonlocal currentCode
        nonlocal allCodes
        """we make recursive calls down the tree leftwards, until they are 'unwound' (or simply no more left nodes exist) at which point we traverse down rightwards until reaching a leaf"""
        if node.left:
            # traverses leftwards if possible - adding 0 to encoding
            currentCode += "0"
            calculateCode(node.left)
        if node.right:
            # traverses rightwards if possible (after leftwards has been tried) and adds 1 to encoding
            currentCode += "1"
            calculateCode(node.right)
        else:
            # adds character code both to the node itself and the allcodes dictionary
            node.code = currentCode
            # print debug for each character's huffman-code: print(f"node {node.data} now has code {node.code}")
            allCodes[node.data] = node.code
        currentCode = currentCode[:-1]

    calculateCode(root) # starts evaluating codes recursively from the root (as then all nodes will be reached)
    return allCodes


def huffmanEncode(uncompressedText):
    """encodes the given text using huffman encoding - returns the resulting binary string and root of the encoding huffman tree in a tuple (text, root)"""
    compressedText = ""
    root = BuildHuffmanTree(uncompressedText)
    codes = calculateCodes(root)
    for char in uncompressedText:
        # maps each character in uncompressedText to its huffman code in compressedText
        compressedText += str(codes[char])
    return (compressedText, root)


def huffmanDecode(compressedText, huffmanTreeRoot):
    """function to decode huffman encoding binary string given the string and the root of its huffman tree"""
    decompressedText = ""
    endOfString = False
    while not endOfString:
        atLeaf = False
        currentNode = huffmanTreeRoot # starts at the root before following the binary string to traverse down the tree until a node is reached
        while not atLeaf:
            if len(compressedText) == 1:
                # if the last bit is reached we make this iteration final
                endOfString = True
            if not(currentNode.left or currentNode.right):
                # once a leaf node is reached we add its data (character) to the string
                decompressedText += currentNode.data
                atLeaf = True
                break
            nextTurn = compressedText[0]
            compressedText = compressedText[1:] # removes the currently acted on bit of the string
            if nextTurn == '0':
                currentNode = currentNode.left
            elif nextTurn == '1':
                currentNode = currentNode.right
    return decompressedText
