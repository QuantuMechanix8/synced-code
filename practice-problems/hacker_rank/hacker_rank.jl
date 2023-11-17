function array_splitting(arr)
    if length(arr) == 1 # no partition possible for singleton array
        return 0 
    end
    # arr elements must be all positive
    l_sum, r_sum = 0, 0
    l_pointer, r_pointer = 1, length(arr)
    l_sum += arr[l_pointer]
    r_sum += arr[r_pointer]
    while !(l_pointer + 1 == r_pointer) # not properly partitioned arr
        if l_sum <= r_sum
            l_pointer += 1
            l_sum += arr[l_pointer]
            # bias extending left arr when equal sum
        elseif l_sum > r_sum
            r_pointer -= 1
            r_sum += arr[r_pointer]
        end
    end
    l_arr = arr[1:l_pointer]
    r_arr = arr[r_pointer:end]
    if l_sum != r_sum
        return 0
    else
        return max(array_splitting(l_arr), array_splitting(r_arr)) + 1
    end
end


function circular_rotate(arr::Vector, places::Int)::Vector
    shift::Int = places % length(arr)
    shifted_arr::Vector = []
    append!(shifted_arr, arr[1+shift:end], arr[1:shift])
    return shifted_arr
end


"""returns the minimum total distance between 1s in array when covering them cumulatively  """
function oil_well(blocks::Array{Array{Int}})::Int
end