def find_num_factors(number):
    factors = []
    for i in range(1, int(number**0.5)+1):
        if number%i == 0:
            factors.append(i)
            if i != number//i:
                factors.append(number//i)
    return len(factors)

finished = False
current_triangle = 0
triangle_index = 0
while not finished:
    triangle_index+=1
    current_triangle += triangle_index
    if find_num_factors(current_triangle)>500:
        print(current_triangle)
        finished = True
        break
        
    
    
    