digits = ['⓪', '①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩', '⑪', '⑫', '⑬', '⑭', '⑮', '⑯', '⑰', '⑱', '⑲', '⑳', '㉑', '㉒', '㉓', '㉔', '㉕', '㉖', '㉗', '㉘', '㉙', '㉚', '㉛', '㉜', '㉝', '㉞', '㉟', '㊱', '㊲', '㊳', '㊴', '㊵', '㊶', '㊷', '㊸', '㊹', '㊺', '㊻', '㊼', '㊽', '㊾', '㊿']
def RLE(uncompressed):
	compressed = ""
	currentIndex = 0
	currentCharCount = 1
	lastChar = False
	# initialises variables to be used
	while not lastChar:
		"""works on the 'character before' i.e. for each character it checks whether it matches the next character and updates currentCharCount and the resulting compressed text to be returned accordingly"""
		currentChar = uncompressed[currentIndex]
		# gives the current character to be looked at using currentIndex (which is iterated)
		if currentIndex + 1 == len(uncompressed):
			lastChar = True
			compressed += digits[currentCharCount] + currentChar
			# if the final character in the string is reached then it adds the next character-number to the string and ends
		elif currentChar == uncompressed[currentIndex + 1]:
			currentCharCount += 1
			# if the next character is the same as the current character the we increment currentCharCount
		else:
			# when the next character is not the same as the current (and not the last) we add the occurence count and letter to the string and then reset the occurence count to 1
			compressed += digits[currentCharCount] + currentChar
			currentCharCount = 1
		currentIndex += 1
		# increments current index after each pass
	return compressed.replace("1", "")
	# removes any 1s from the RLE as 1 occurence can be shown just using the letter i.e. 5J1H -> 5JH and this is more efficient


if __name__ == "__main__":
    #code for testing this file itself - wont be run when the file is imported
    pass