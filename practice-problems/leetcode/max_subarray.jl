"""
`max_subarray(nums::Array{<:Real})::Array{<:Real}`

returns the subarray with the largest sum

(will return the first subarray in case of multiple solutions
also solves for shortest form i.e. `[3-2,8]` rather than `[0,2,-2,8,-1,1]` 

# examples

max_subarray([1,7,-6,8,-5]) => [1,7,-6,8]
"""
function max_subarray(nums::Array{<:Real})::Array{<:Real}
    max_subarray_total = nums[1] 
    max_subarray_position = (1,1) # initialise largest subarray as first index

    start_index = 1
    running_subarray_total = 0
    for (index, value) in enumerate(nums)
        running_subarray_total += value
        if running_subarray_total ≤ 0
            start_index = index+1
            running_subarray_total = 0
        elseif running_subarray_total > max_subarray_total
            max_subarray_total = running_subarray_total
            max_subarray_position = (start_index, index)
        end
    end
    return nums[max_subarray_position[1]:max_subarray_position[2]]
end

