list1 = [0,4,6,17,57]
list2 = [4,8,12,85]
mergeList = []
i,j = 0,0

# gradually moves pointers rightward, each time comparing two smallest elements and adding the lesser to the list
while not(i==len(list1) and j==len(list2)):
	if i==len(list1):
		mergeList.append(list2[j])
		j+=1
	elif j==len(list2):
		mergeList.append(list1[i])
		i+=1
	elif list1[i]>= list2[j]:
		mergeList.append(list2[j])
		j+=1
	elif list2[j]>list1[i]:
		mergeList.append(list1[i])
		i+=1
print(mergeList)
