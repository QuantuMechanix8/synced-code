# there is a faulty odometer in a car which skips the number 4 when counting distance i.e. 13 -> 15, 39 -> 50, 213,999->215,000 etc
# given a distance on the faulty odometer, find the actual distance the car has travelled, accounting for the skipped 4s

"""
fours_missing(z::Integer, n::Integer)::Integer

returns the total 'fours-numbers' that are skipped up to a value `z` for a specific order `n` of four

e.g. 
    fours_missing(23, 0) -> 2 gives how many 'unit fours' are skipped up to 23 [4 and 14 are skipped giving 2]
    fours_missing(55, 1) -> 9 gives how many 'tens fours' are skipped up to 55 [9 are skipped as 44 was already skipped by units]
"""
function fours_missing(z::Integer, n::Integer)::Integer
    9^n * (z + 5*10^n)÷(10^(n+1))
    # 9^n gives how many are skipped in each 'run' and then this is multiplied by how many runs of the four order there are
end


"""
corrected_odometer(distance::Integer)::Integer

returns the corrected distance after accounted for the skipped 4's on the odometer

e.g. `corrected_odometer(6) -> 5` [as one 4 was skipped]
    `corrected_odometer(50) -> 36` [10 skipped from 40's and another 4 are skipped before that]
"""
function corrected_odometer(distance::Integer)::Integer
    n = trunc(Int, log(distance/4)/log(10)) # max order of 4 we need to consider - solution to max int n | 4*10^n < d
    corrected_distance = distance
    for n ∈ 0:n
        corrected_distance -= fours_missing(distance, n)
    end
    return corrected_distance
end
    
