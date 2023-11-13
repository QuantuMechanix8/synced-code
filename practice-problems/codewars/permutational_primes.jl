using Combinatorics: Combinatorics
include("../../general/factors.jl") # code that computes primes


function integer_permutations(n::Integer)::Set{Integer}
	num_str_permutations = collect(Combinatorics.permutations(string(n))) # list of (string) permutations of the number
	filter!(x -> x[1] != '0', num_str_permutations) # removes permutations that start with 0
	return Set(parse.(Int, join.(num_str_permutations)))
end


"""find how many permutations of a given number are prime"""
function prime_permutations(n::Integer)::Set{Integer}
    return filter(is_prime, integer_permutations(n))
end


permutational_primes::Vector{Int} = []
for prime ∈ primes_up_to(1000)
    if length(prime_permutations(prime)) >= 3 # at least 3 permutations of the prime must be prime
        push!(permutational_primes, prime)
    end
end

print(permutational_primes)

