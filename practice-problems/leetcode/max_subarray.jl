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


"""
`remove_nonpositive_edge_subarrays!(nums::Array{<:Real}, threshold::Real)`


remove nonpositive subarrays from start and end of the array
"""
function remove_nonpositive_edge_subarrays!(nums::Array{<:Real}, threshold::Real, dir = 1)
    finished = false 
    subtotal = 0
    index = dir == 1 ? 1 : length(nums) # sets index to correct end of array depending on iteration direction
    while !finished 
        subtotal += nums[index]
        index += dir
        if subtotal ≤ 0
            nums = dir == 1 ? nums[index:end] : nums[1:index] # removes negative subarray from array
        elseif subtotal > threshold
            threshold = subtotal



# this function ^ can probably do the entire computation, iterating inwards from both sides and removing subarrays
# smaller than the `threshold` (current largest subarray) and updating this threshold whenever it is beaten
#  - just need to thing about how to handle then end case, on actually ending the iteration and returning the 
#  remeaining max subarray
