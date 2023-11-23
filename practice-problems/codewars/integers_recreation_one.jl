# get the divisors of a number n


"""return the divisors of a number n in a vector of integers
    e.g. 6 => [1, 2, 3, 6]
        24 => [1, 2, 3, 4, 6, 8, 12, 24]"""
function divisors(n::Integer)::Vector{Integer} # vector used rather than set for ascending order (+ faster)
    divisors::Vector{Integer} = []
    for i ∈ 1:floor(Int, sqrt(n))
        if n % i == 0
            push!(divisors, i)
            if i != n/i # if i is not the square root of n then n/i is also a divisor
                push!(divisors, n/i)
            end
        end
    end
    return sort(divisors)
end


"""return sum of squared divisors of a number n"""
function squared_divisors(n::Integer)::Integer
    sum::Integer = 0
    for i ∈ divisors(n)
        sum += i^2
    end
    return sum
end


function is_square(n::Integer)::Bool
    return n == floor(Int, sqrt(n))^2
end


function list_squared(m::Integer, n::Integer)::Vector{Vector{Integer}}
    result::Vector{Vector{Integer}} = []
    for i ∈ m:n
        if is_square(squared_divisors(i))
            push!(result, [i, squared_divisors(i)])
        end
    end
    return result
end

divisors(120)