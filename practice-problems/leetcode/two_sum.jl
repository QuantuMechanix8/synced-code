"""
`twosum(nums::Array{Number}, target::Number):: Array{Integer}`

finds two indexes of items in `nums` which will sum to `target` and returns them in an array - `[first_index, second_index]`

`twosum([0,1,2,3,4,5], 8) -> [4,6]` 
(indexes 4 and 6 correspond to the values 3,5 which add to the target 8)
"""
function twosum(nums::Array{<:Number}, target::Number)::Array{<:Integer}
    sorted_nums = sort(nums)
    start, finish = 1, length(sorted_nums) # pointers for the start and end of the array
    target_reached = false
    while !target_reached
        sum = sorted_nums[start] + sorted_nums[finish]
        if start == finish
            return []
        elseif sum == target
            target_reached = true
            start = findfirst(isequal(sorted_nums[start]), nums)
            finish = findfirst(isequal(sorted_nums[finish]), nums)
            return [start, finish]
        elseif sum < target
            start += 1
        elseif sum > target
            finish -= 1
        end
    end
end
