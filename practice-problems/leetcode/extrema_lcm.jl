"""
`extrema_lcm(nums::Array{<:Unsigned})<:Unsigned`

return the lowest common multiple of the minimum and maximum value in an array

# examples
extrema_lcm([7,12,9]) => 84 # lcm(7,12)
extrema_lcm([3,51,16,5) => 51 # lcm(3,51)
"""
extrema_lcm(nums::Array{<:Unsigned})::Unsigned = extrema(nums) |> collect |> lcm
