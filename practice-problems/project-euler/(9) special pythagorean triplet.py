def findPythagoreanTriple(sum):
    a,b,c = 0,0,sum
    done = False
    while not done:
        for i in range(1, sum):
            for j in range(1, sum):
                a,b,c = i,j, sum -(j+i)
                #print(f"a = {a}, b = {b}, c = {c}")
                if c<=0:
                    break
                elif a**2 + b**2 == c**2:
                    print(f"Triple found at: a - {a}, b - {b}, c - {c}")
                    return a*b*c
        return None
print(findPythagoreanTriple(1000))