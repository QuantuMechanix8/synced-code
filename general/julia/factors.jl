function primes_up_to(n) # function that returns list of all the primes up to the input number
	# uses recursive definition as you need the primes to efficiently check divisibility
	if n == 1
		return []
	end

	highest_possible_factor = floor(Int, sqrt(n))
	potential_prime_factors = primes_up_to(highest_possible_factor)
	prime_factors = potential_prime_factors
	new_prime_lower_bound = maximum(potential_prime_factors; init=1) + 1
	
	for n in new_prime_lower_bound:n
		if !divisible(potential_prime_factors, n)
			push!(prime_factors, n)
		end
	end
	return prime_factors
end


function divisible(potential_factors, n)
	for factor in potential_factors
		if n%factor == 0
			return true 
		end
	end
	return false 
end


function is_prime(n::Integer)::Bool
	potential_factors = primes_up_to(floor(Int, sqrt(n)))
	return !divisible(potential_factors, n)
end