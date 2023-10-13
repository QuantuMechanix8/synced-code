def sum(n): # 1+2+3+4+5...n
    result = 0
    
    for i in range(1,n+1):
        result = result + i
    
    return result

def recursive_sum(n):
    if n==1:
        return 1
    else:
        return recursive_sum(n-1) + n

recursive_sum(3)