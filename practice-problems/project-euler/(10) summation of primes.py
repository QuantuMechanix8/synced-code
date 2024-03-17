import numpy as np

def getPrimes(Ubound, Lbound = 2, primeList = None):
	Lbound = max(Lbound, 2)
	primes = []
	Lbound, Ubound = int(Lbound), int(Ubound)
	for i in range(Lbound, Ubound+1):
		if isPrime(i, primeList):
			primes.append(i)    
	return primes

def isPrime(num, primeList = None):
	factor = False
	floorSqrt = int(np.sqrt(num))
	if not primeList:
		factorList = [i for i in range(3,floorSqrt+1, 2)]
		factorList.insert(0,2)
		for i in factorList:
			if num == i:
				return not factor
			if num%i==0:
				factor = True
				return not factor
	elif primeList:
		for prime in primeList:
			if prime>floorSqrt:
				break
			if num%prime == 0:
				factor = True
				return not factor
	return not factor
	
lbound = int(input("enter the lower bound (natural number) to start finding primes from: "))
ubound = int(input("enter the upper bound (natural number) to start finding primes from: "))
largestPossiblePrimeFactor = int(np.sqrt(ubound))
primeFactorList = getPrimes(largestPossiblePrimeFactor)
#print(f"prime list: {primeFactorList}")
#start = time.time()
primes = getPrimes(ubound, lbound, primeFactorList)
#end = time.time()
#print(f"execution took {end-start} to find the primes")
sum = 0
for prime in primes:
	sum+=prime
print(sum)