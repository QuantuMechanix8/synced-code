"""Encodes a string such that unique characters map '(' and non-unique/duplicate characters map to ')' (ignores case)
e.g. duplicate_encode('Success') ↦ ')())())'"""
function duplicate_encode(word)
    word = lowercase(word)
    chars = Set(word)
    unique_chars = Dict{Char,Bool}()
    for char in chars
        unique_chars[char] = (count(x -> x == char, word) == 1)
    end
    encoded_word = ""
    for char in word
        encoded_word *= (unique_chars[char] ? "(" : ")")
    end
    return encoded_word
end


"""Returns the integer in the array that has odd multiplicity"""
function find_odd(int_array)
    array_integers = Set(int_array)
    for integer in array_integers
        if count(i -> (i == integer), int_array) % 2 == 1
            return integer
        end
    end
end


"""Returns whether the second array simply contains the same elements as the first but squared (same multiplicity)
e.g. is_square([1,2,3,4], [16,4,1,9]) ↦ true"""
function is_square(first_array, second_array)
    count_value(n, iterable) = count(x -> (x == n), iterable)
    first_array_square = [n^2 for n in first_array]
    first_array_square_freqs = Dict{Integer,Integer}(n => count_value(n, first_array_square) for n in Set(first_array_square))
    second_array_freqs = Dict{Integer,Integer}(n => count_value(n, second_array) for n in Set(second_array))
    return first_array_square_freqs == second_array_freqs
end


"""Returns the total time required for customers to checkout, where each element of the customer_times array represents the time a given customer will take to checkout and tills the number of tills
the customer at the front of the 'queue' is assigned to a till as soon as it is free
e.g. queue_time([5,3,4], 1) = 12, queue_time([10,2,3,3] 2) = 10 as the 10 min customer will finish after the 2, 3, 3 have all checked out from other till"""
function queue_time(customer_times, num_tills)
    total_time = 0
    empty_queue = false
    tills = zeros(num_tills)
    while !empty_queue
        tills, customer_times = move_to_zeros(tills, customer_times)
        empty_queue = length(customer_times) == 0 ? true : false
        if empty_queue
            break
        end
        timestep = minimum(tills)
        total_time += timestep
        tills .-= timestep
    end
    total_time += maximum(tills)
    return total_time
end


"""Will move front items in `move_from` to positions in `move_to` that are zero - returns (move_to, move_from)
e.g. move_to_zeros([6,0,1.1, 0, 0], [1,2,3,4,5,6]) ⟼ ([6, 1, 1.1, 2, 3], [4,5,6])"""
function move_to_zeros(move_to, move_from)
    zeros = [index for (index, value) in enumerate(move_to) if (value == 0)]
    if length(zeros) == 0 # no moves need to be made
        return (move_to, move_from)
    end
    max_moves = min(length(zeros), length(move_from))
    zeros = zeros[1:max_moves]
    move_to[zeros] = move_from[1:max_moves]
    return (move_to, move_from[max_moves+1:end])
end


"""Returns the text but using capitalization (camelcase) instead of a separators - separators defaults to Set('-', '_', ' ')
e.g. to_camelcase("this is_a-trial_string", Set('-', '_', ' ')) ⟼ "thisIsATrialString"""
function to_camelcase(text, separators=nothing)
    if isnothing(separators)
        separators = Set('-', '_', ' ')
    end
    letters = Set(Char(i) for i ∈ 65:90) ∪ Set(Char(i) for i ∈ 97:122)
    text = strip(text)
    final_index = length(text)
    separation_indexes = [index for (index, char) in enumerate(text) if (char ∈ separators) && (index ∈ 1:final_index)]
    
end


# """Returns the index of the next letter in `text` starting from the provided `index`"""
# function next_letter_index(text, index)
    
#     for i ∈ index:length(text)
#         if text[i] ∈ letters
#             return i
#         end
#     end
#     return nothing
# end