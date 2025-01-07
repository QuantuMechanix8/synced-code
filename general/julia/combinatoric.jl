# brute force solution to the following problem:

# 5 distinct (different coloured) dice are rolled, giving 3 different numbers 
# how many ways can this happen

function generate_dice()
    dice = []
    for i in 1:5
        push!(dice, rand(1:6))
    end
    return dice
end


function check_valid_roll(dice_numbers)
    if length(unique(dice_numbers)) == 3
        return true
    else
        return false
    end
end


function count_ways()
    valid_rolls = Set()
    for i in 1:100_000
        dice = generate_dice()
        if check_valid_roll(dice)
            push!(valid_rolls, dice)
        end
    end
    return valid_rolls
end