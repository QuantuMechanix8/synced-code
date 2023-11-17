import time

def next_collatz(number):
    if number%2 == 0: 
        return number >> 1 # division by 2
    else:
        return 3*number + 1

def len_collatz(seed, neededMax = 500):
    currentNum = seed
    currentNum_Len = 1
    while currentNum != 1 and currentNum_Len < neededMax:
        currentNum = next_collatz(currentNum)
        currentNum_Len += 1
        if currentNum == 4:
            return currentNum_Len + 2
    return currentNum_Len

def iterative_len_collatz(seed):
    collatz_len = 1
    currentValue = seed
    while currentValue != 1:
        if currentValue%2 == 0:
            currentValue = currentValue >> 1
        else:
            currentValue = 3*currentValue + 1
        collatz_len += 1
    return collatz_len
    
max_collatz = 0
max_collatz_seed = 0
for i in range(1, 1_000_000):
    current_collatz = iterative_len_collatz(i)
    if current_collatz > max_collatz:
        max_collatz = current_collatz
        max_collatz_seed = i
print(f"The seed of the longest collatz sequence is {max_collatz_seed} with a length of {max_collatz}")