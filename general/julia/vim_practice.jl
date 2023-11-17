function backward_index(arr, index_from_end)
    if index_from_end>length(arr)
        return nothing
    else
        return arr[end-(index_from_end-1)]
    end
end


function rowwise_mat_to_arr(arr)
    return vec(arr')
end 


function descriminint_2x2(matrix::Matrix{Int})
    if size(matrix) != (2,2)
        return nothing
    else
        a,b,c,d = rowwise_mat_to_arr(matrix) 
        return a*d - b*c
    end
end