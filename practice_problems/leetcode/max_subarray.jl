""" 
max_subarray(nums::Array{Real})::Array{Real}

return subarray of nums with the largest sum 

e.g. max_subarray([-2,1,-3,4,-1,2,1,-5,4]) ->[4,-1,2,1]
"""
function max_subarray(nums::Array{<:Real})::Array{<:Real}
    finished = false
    threshold = maximum(nums)
    max_subarray = nums
    while !finished
        remove_nonpositive_edges(max_subarray)
        

end


"""
`remove_nonpositive_edges!(nums::Array{<:Real})::Array{<:Real}`

remove nonpositive values from the start and end of the array

e.g. `remove_nonpositive_edges!([-1,-2,7,-3,8,12,-5]) -> [7,-3,8,12]`
"""
function remove_nonpositive_edges!(nums::Array{<:Real})
    start = findfirst(x -> x>0, nums)
    finish = findlast(x -> x>0, nums)
    nums = nums[start:finish]
end
