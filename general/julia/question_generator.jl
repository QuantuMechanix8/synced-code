function number_bond_Q(addend1_max::Int, addend2_max::Int, max_offset::Int = 0)
    rand_digit = rand(1:9)
    addend2_bond = 10 - rand_digit
    if max_offset ≠ 0
        offset_range = -min(addend2_bond - 1, max_offset):max_offset
        offset_range = filter(x->!iszero(x), offset_range) # remove 0 from offset range
        addend2_bond = addend2_bond + rand(offset_range)
    end
    addend1 = (rand(1:addend1_max) ÷ 10) * 10 + rand_digit
    addend2 = (rand(1:addend2_max) ÷ 10) * 10 + addend2_bond
    return "$addend1 + $addend2"
end


function print_question_set(question_set)
    println("Printing question Set:\n\n")
    for question in question_set
        println("$question = \n_________________\n")
    end
end


function generate_qs(addend1_max = 50, addend2_max = 9, num_questions = 10, max_offset = 1)
    questions = Set()
    for i ∈ 1:num_questions
        push!(questions, number_bond_Q(addend1_max, addend2_max, max_offset))
    end
    return questions
end