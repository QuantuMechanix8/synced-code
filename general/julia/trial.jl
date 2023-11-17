function round_to_sf(number::Number, SF::Int)::Number
    shifts = floor(Int, log10(number))
    number *= 10.0^(-shifts)
    number = round(number, digits = SF-1)
    return number * 10^(shifts)
end


function truncate_to_sf(number::Number, SF::Int)::Number
    shifts = floor(Int, log10(number))
    number /= 10^shifts
    number = trunc(number, digits=SF-1)
    number *= 10^shifts
    return number
end


function and_needed(number::Int)::Bool
    three_sf_num = truncate_to_sf(number, 3)
    ord_of_mag = floor(Int, log10(three_sf_num))
    if ord_of_mag % 3 == 2
        numbers_after_hundred = three_sf_num % 10^(ord_of_mag)
        return numbers_after_hundred != 0
    end
    return false 
end

 
"""Takes a number and returns the english written representation for the first grouping (up to first comma)
e.g. SF_to_name(137) -> 'one hundred and thirty seven'  
     SF_to_name(8_000) -> 'eight thousand'
     SF_to_name(209_000_000) -> 'two hundred and nine million' """
function single_grouping_to_number(number)
    add_and = and_needed(number)
    digits = Dict(1 => "one ", 2 => "two ", 3 => "three ", 4 => "four ", 5 => "five ", 6 => "six ", 7 => "seven ", 8 => "eight ", 9 => "nine ")
    teens = Dict(10 => "ten ", 11 => "eleven ", 12 => "twelve ", 13 => "thirteen ", 14 => "fourteen ", 15 => "fifteen ", 16 => "sixteen ", 17 => "seventeen ", 18 => "eighteen ", 19 => "nineteen ")
    tens = Dict(2 => "twenty ", 3 => "thirty ", 4 => "forty ", 5 => "fifty ", 6 => "sixty ", 7 => "seventy ", 8 => "eighty ", 9 => "ninety ")
    macro_scale_prefixes = Dict(1 => "m", 2 => "b", 3 => "tr", 4 => "quadr", 5 => "quint", 6 => "sext", 7 => "sept", 8 => "oct", 9 => "non", 10 => "dec")
    ord_of_mag = floor(Int, log10(number))
    macro_scale = (ord_of_mag ÷ 3) 
    macro_suffix = ""
    if macro_scale >= 2
        macro_suffix = macro_scale_prefixes[macro_scale - 1] * "illion " # shifted so that 1->million, 2-> billion etc
    elseif macro_scale == 1 
        macro_suffix = "thousand "
    end
    micro_scale = ord_of_mag % 3
    micro_suffix = ""
    hundreds_digit = number ÷ 10^(macro_scale*3 + 2) % 10 # magic bro
    tens_digit = number ÷ 10^(macro_scale*3 + 1) % 10 
    ones_digit = number ÷ 10^(macro_scale*3) % 10
    if hundreds_digit ≠ 0
        micro_suffix *= digits[hundreds_digit]*"hundred "* (add_and ? "and " : "") 
    end
        # have to do tens & ones together which makes for annoying edge case because you say nineteen instead of 10 9 thousand 
    if tens_digit ≠ 0
        if tens_digit == 1
            micro_suffix *= teens[10tens_digit + ones_digit]
        else
            micro_suffix *= tens[tens_digit]
        end
    end
    if ones_digit ≠ 0 && tens_digit ≠ 1 # no need to do ones digit if its a teen number as handled by above logic
        micro_suffix *= digits[ones_digit]
    end
    return micro_suffix * macro_suffix 
end


function number_to_name(number::Int)::String
    if number == 0 # otherwise it breaks as log10(0) is problematic
        return ""
    end
    ord_of_mag = floor(Int, log10(number))
    if ord_of_mag <= 2
        return single_grouping_to_number(number)
    else
        shift_to_next_group = ord_of_mag % 3
        return single_grouping_to_number(number) * number_to_name(number % 10^(ord_of_mag-shift_to_next_group))
    end
end


function no_space_count(str::AbstractString)::Int
    return length(str) - count(c->c==' ', str)
end
