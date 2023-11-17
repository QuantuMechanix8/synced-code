# find the number of valid substrings of length k within a number natural

function num_substrings(number, substr_length)
    number_str = repr(number)
    total_digits = length(number_str)
    if substr_length > total_digits
        return 0
    end
    last_substring_index = total_digits - (substr_length - 1)
    substring_starts = number_str[1:last_substring_index]
    return last_substring_index - count('0', substring_starts) 
end


#seems good?
function majority_count(list::Vector)::Any
    # walk through arr in pairs and "cancels out" when pairs are different
    finished = false
    last_index = length(list)
    i₁ = 1
    i₂ = 2
    while !finished
        first, second = list[i₁], list[i₂]
        if first ≠ second && i₂-i₁ == 1
            i₁ += 2
            i₂ += 2
        elseif first ≠ second
            i₁ += 1
            i₂ = i₁ + 1
        elseif first == second
            i₂ += 1
        end
        finished = i₂ >= last_index
    end
    return list[i₁]
end


majority_count([1,2,3,3,3,2,3])