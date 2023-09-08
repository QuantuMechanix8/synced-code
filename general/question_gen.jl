function generate_question(summand1_max, summand2_max, max_offset = 0)
    rand_digit = rand(1:9)
    rand_digit_bond = 10 - rand_digit
    downward_offset = min(max_offset, rand_digit_bond-1)
    sum_digit = rand_digit_bond + rand(-(downward_offset):max_offset)
    summand1 = (rand(1:summand1_max) ÷ 10) * 10 + rand_digit
    summand2 = (rand(1:summand2_max) ÷ 10) * 10 + sum_digit
    return "$summand1 + $summand2" 
end

function is_carmichael(n)
    for i in 1:n
        valid = gcd(i, n) ≠ 1 || i^(n-1) % n == 1  
        if !valid
            return false
        end
    end
    return true
end

for n in 1:10_000
    if is_carmichael(n)
        println("$n is a carmicheal number!")
    end
end


print("wot fam")
