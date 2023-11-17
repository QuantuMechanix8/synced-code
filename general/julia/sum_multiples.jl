# Program to solve and generalise the first problem of the Euler Project
using Test

"""Iterates over each value in the range and checks if it divides by any of the relevant multiples, if so it adds it to the total - then just returns the total"""
function slow_solution(upper_bound, lower_bound=1; multiples=[3, 5])
    total::Int = 0
    for i ∈ lower_bound:upper_bound
        for multiple ∈ multiples
            if i % multiple == 0
                total += i
                break
            end
        end
    end
    return total
end

"""Calculates the number of multiples of a given value are within the specified range (defaults to 1..1000 inclusive)"""
function num_multiples(value, lower_bound=1, upper_bound=1_000)
    lmargin = lower_bound % value == 0 ? 0 : (value - lower_bound % value) # distance from lower bound to next multiple
    rmargin = upper_bound % value # distance from upper bound to previous multiple
    margins = lmargin + rmargin
    range_length = upper_bound - (lower_bound - 1) - margins
    # if two multiples of m are R values apart we can say that R = (n-1)m + 1 where n is the number of multiples contained in that range e.g. 2-12 have a distance of 11 which is 𝟱*2 + 1, and contain 6 multiples of 2, we simply rearrange this for n 
    return (range_length - 1) ÷ value + 1
end

function sum_using_formula(lower_bound=1, upper_bound=1_000; multiples=[3, 5])

end


"""Solves the problem for a single desired multiple"""
function sum_single_multiple(multiple::Int, lower_bound=1, upper_bound=1_000)
    starting_value = lower_bound % multiple == 0 ? lower_bound : lower_bound + (multiple - lower_bound % multiple)
    multiples = num_multiples(multiple, lower_bound, upper_bound)
    return multiples * (starting_value + multiples * multiple) ÷ 2
end

@testset "single_multiple" begin
    @test sum_single_multiple(1, 1, 10) == 55
    @test sum_single_multiple(2, 1, 10) == 30
    @test sum_single_multiple(3, 3, 14) == 30
    @test sum_single_multiple(5, 1, 1000) == 100_500
end



@testset "test_num_multiples" begin
    @test num_multiples(2, 1, 10) == 5
    @test num_multiples(2, 2, 10) == 5
    @test num_multiples(3, 5, 20) == 5
    @test num_multiples(7, 8, 13) == 0
end