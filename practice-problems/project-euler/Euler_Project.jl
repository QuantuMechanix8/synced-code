"""Problem 1 - Returns the sum of the numbers in the given range that are a mulitple of one of the given values"""
function sum_multiples(upper_bound, lower_bound=1; multiples=[3, 5])
    sum = 0
    for i in lower_bound:upper_bound
        for multiple in multiples
            if i % multiple == 0
                sum += i
                break
            end
        end
    end
    return sum
end


"""Problem 2 - Returns the sum of the fibonacci numbers below upper_bound that satisfy a given condition (fib_condition function returns true for desired numbers and false for others)"""
function sum_fibonacci(upper_bound; fib_condition=x -> (x % 2 == 0) ? true : false)
    sum = 0
    first = 0
    second = 1
    current = 1
    while first < upper_bound
        if fib_condition(first)
            sum += first
        end
        first = second
        second = current
        current = first + second
    end
    return sum
end

# prime time :)
"""function to determine if a number is prime by checking divisibility of primes up to its square root"""
function is_prime(number)
    if number == 1
        return false
    elseif number == 2
        return true
    else
        highest_possible_prime_factor = floor(sqrt(number))
        for i in primes_up_to(highest_possible_prime_factor)
            if number % i == 0
                return false
            end
        end
        return true
    end
end


"""Returns the primes up to the given upper bound"""
function primes_up_to(upper_bound)
    prime_set = Set()
    if upper_bound == 1
        return prime_set
    else
        # recursively calls itself to get the primes up to the square root of the largest number in the desired range so that it can efficiently generate such primes
        highest_possible_prime_factor = floor(sqrt(upper_bound))
        potential_factors = primes_up_to(highest_possible_prime_factor)
        lower_bound = (length(potential_factors) == 0) ? 2 : maximum(potential_factors) + 1
        for potential_prime in lower_bound:upper_bound
            is_prime = true
            for potential_factor in potential_factors
                if (potential_prime % potential_factor == 0)
                    is_prime = false
                    break
                end
            end
            if is_prime
                push!(prime_set, potential_prime) # ?
            end
        end
    end
    return prime_set ∪ potential_factors
end


"""Problem 3 - Returns the prime factors of a given number"""
function get_factors(number)
    fully_factorized = false
    factors = []
    while (!fully_factorized)
        prime = true
        highest_possible_prime_factor = floor(sqrt(number))
        potential_factors = primes_up_to(highest_possible_prime_factor)
        for prime_factor in potential_factors
            if number % prime_factor == 0
                prime = false
                number /= prime_factor
                push!(factors, prime_factor)
                break
            end
        end
        # if loop this is reached then number must be prime
        if prime == true
            fully_factorized = true
            push!(factors, number)
        end
    end
    return factors
end


"""Check whether a number is a palendrome"""
function is_palendrome(number)
    number = string(number)
    return number == reverse(number)
end


"""Problem 4 - Returns the largest palendrome that is formed from the product of two numbers with the given number of digits, returns tuple - (palendrome_factor1, palendrome_factor2, max_palendrome) """
function largest_product_palendrome(digits)
    max_palendrome = 0
    palendrome_factor1, palendrome_factor2 = 0, 0
    max_value = 10^(digits) - 1
    min_value = 10^(digits - 1)
    first_num, second_num = max_value, max_value
    for first_num in max_value:-1:min_value
        if first_num^2 <= max_palendrome
            break
        end
        for second_num in first_num:-1:min_value
            product = first_num * second_num
            if (is_palendrome(product) && product > max_palendrome)
                max_palendrome = product
                palendrome_factor1, palendrome_factor2 = first_num, second_num
            end
        end
    end
    return (palendrome_factor1, palendrome_factor2, max_palendrome)
end


"""Problem 5 - returns the lowest common mulitple of an array of numbers"""
function lowest_common_multiple(numbers)
    all_factors = Dict()
    for number in Set(numbers)
        factors = get_factors(number)
        unique_factors = Set(factors)
        for factor in unique_factors
            factor_count = count(x -> (x == factor), factors)
            if (!haskey(all_factors, factor))
                all_factors[factor] = factor_count
            elseif all_factors[factor] < factor_count
                all_factors[factor] = factor_count
            end
        end
    end
    product = 1
    for (factor, frequency) in all_factors
        product *= factor^frequency
    end
    return product
end


"""Problem 6 - returns the difference between the sum of the num_list squared and the sum of the squares of the elements in the list i.e. for a list [1,2,3] returns (1+2+3)^2 - (1^2 + 2^2 + 3^2)"""
function sum_squared_vs_squared_sum(num_list)
    squared_sum = reduce(+, map(x -> x^2, num_list))
    sum_squared = reduce(+, num_list)^2
    return sum_squared - squared_sum
end


"""Problem 7 - Returns the nᵗʰ prime number"""
function nth_prime(n)
    # using fact that all primes after 3 are of form 6n±1
    if n == 1
        return 2
    elseif n == 2
        return 3
    end
    prime_order = 3
    prime_value = 5
    below_multiple_of_6 = true
    while prime_order < n
        prime_value += below_multiple_of_6 ? 2 : 4
        if is_prime(prime_value)
            prime_order += 1
        end
        below_multiple_of_6 = !below_multiple_of_6
    end
    return prime_value
end


"""Problem 8 - gives the larges product of (num_digits) adjacent digits in the number - returns an array of these digits and the corresponding product"""
function largest_adjacent_digit_product(num_digits, number)
    # uses a sliding window across the number
    digit_arr = [parse(Int, digit) for digit in string(number)]
    total_digits = length(digit_arr)
    if num_digits > total_digits
        println("number does not contain $(num_digits) adjacent digits")
        return
    elseif total_digits == num_digits
        return (reduce(*, digit_arr), digit_arr)
    else
        max_product = 0
        max_product_digits = []
        current_start_index = 1
        reached_number_end = false
        while (!reached_number_end)
            if (current_start_index + (num_digits - 1) == total_digits)
                reached_number_end = true
            end
            current_digit_arr = digit_arr[current_start_index:current_start_index+(num_digits-1)]
            product = reduce(*, current_digit_arr)
            if product > max_product
                max_product = product
                max_product_digits = current_digit_arr
            end
            current_start_index += 1
        end
        return (max_product, max_product_digits)
    end
end


function is_pythag_triple(a, b, c)
    return (a^2 + b^2) == c^2
end


"""Problem 9 - returns a pythagorean triplet a,b,c where a+b+c = sum if it exists, otherwise returns Nothing"""
function pythag_triple(sum)
    # iterate over values of c from largest possible (still need 'leeway' of 2 for a,b ≠ 0)
    for c in (sum-2):-1:1
        # total 'real-estate' that can be split across a,b
        total = sum - c
        for a in 1:(total-1)
            # iterate over all possible values of a (still need 'leeway' of 1 for b ≠ 0)
            b = total - a
            if (is_pythag_triple(a, b, c))
                return (a, b, c)
            end
        end
    end
    # if entire loop completes with no triplet then none exists
    return Nothing
end

#=
Problem 10
ans = 142913828922
The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

Find the sum of all the primes below two million.
=#
"""
Problem 10
Using the prime finder function from problem 3 finds the sum of all primes below a number
"""
sum_primes_upto = sum ∘ primes_up_to


"""returns a bool for whether the given indexes are valid within the given matrix"""
function valid_indexes(matrix::Matrix, indexes::Vector)::Bool
    matrix_dims = size(matrix)
    if length(matrix_dims) ≠ length(indexes)
        return false
    end
    for (axis, size) in enumerate(matrix_dims)
        #println("axis = $axis, size = $size")
        if indexes[axis] < 1 || indexes[axis] > size
            return false
        end
    end
    return true
end


"""Gives the largest product of a `max_terms` number of consecutive values in the line"""
function max_product_in_line(line::Vector, max_terms::Integer)
    # will get thrown off when less than the maximum number of terms gives a higher result
    max = 0
    size = min(length(line), max_terms)
    for i ∈ 1:length(line)-size + 1
        product = prod(line[i:i+(size-1)])
        if product > max
            max = product
        end
    end
    return max
end


"""Creates a vector of a 'line' of coefficients within the matrix, given a starting position and direction"""
function matrix_to_line(matrix::Matrix, direction::Vector, start_position::Vector)::Vector
    line_finished = false
    vector = []
    position = start_position
    if !valid_indexes(matrix, start_position)
        println("Start index is outside matrix!")
        line_finished = true
    end
    while !line_finished
        push!(vector, matrix[position...])
        position += direction
        if !valid_indexes(matrix, position)
            line_finished = true    
        end
    end
    return vector
end


"""returns a vector of vectors giving all the 'lines' of coefficients in the matrix"""
function matrix_lines(matrix)
    lines = []
    matrix_rows, matrix_columns = size(matrix)
    directions = [[1,0], [0,1], [1,1], [1, -1]] # Down, Right, DownRight, DownLeft
    # starting positions for lines (corners are considered as at the top)
    right = [[n, matrix_columns] for n ∈ 1:matrix_rows]
    top = [[1, n] for n ∈ 1:matrix_columns]
    left = [[n, 1] for n ∈ 1:matrix_rows]
    bottom = [[matrix_rows, n] for n ∈ 1:matrix_columns] # typically not needed
    for direction in directions
        start_positions = Set()
        if direction[1] > 0
            start_positions = start_positions ∪ top 
        elseif direction[1] < 0
            start_positions = start_positions ∪ bottom
        end
        if direction[2] > 0
            start_positions = start_positions ∪ left
        elseif direction[2] < 0
            start_positions = start_positions ∪ right
        end 
        for start_position ∈ start_positions
            line = matrix_to_line(matrix, direction, start_position)
            push!(lines, line)
        end
    end
    return lines
end


"""
Problem 11
What is the greatest product of four adjacent numbers in the same direction (up, down, left, right, or diagonally) in the 20×20 grid?   
"""
function matrix_maxadj_product(matrix::Matrix, max_terms::Integer)
    all_lines = matrix_lines(matrix)
    return maximum(max_product_in_line.(all_lines, max_terms))
end
#= 
Problem 12
ans = 76576500
The sequence of triangle numbers is generated by adding the natural numbers. So the 7th triangle number would be 1 + 2 + 3 + 4 + 5 + 6 + 7 = 28. The first ten terms would be:

1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

Let us list the factors of the first seven triangle numbers:

 1: 1
 3: 1,3
 6: 1,2,3,6
10: 1,2,5,10
15: 1,3,5,15
21: 1,3,7,21
28: 1,2,4,7,14,28
We can see that 28 is the first triangle number to have over five divisors.

What is the value of the first triangle number to have over five hundred divisors?=#

#= 
Problem 13
ans = 5537376230
Work out the first ten digits of the sum of the following one-hundred 50-digit numbers.

37107287533902102798797998220837590246510135740250
46376937677490009712648124896970078050417018260538
74324986199524741059474233309513058123726617309629
91942213363574161572522430563301811072406154908250
23067588207539346171171980310421047513778063246676
89261670696623633820136378418383684178734361726757
28112879812849979408065481931592621691275889832738
44274228917432520321923589422876796487670272189318
47451445736001306439091167216856844588711603153276
70386486105843025439939619828917593665686757934951
62176457141856560629502157223196586755079324193331
64906352462741904929101432445813822663347944758178
92575867718337217661963751590579239728245598838407
58203565325359399008402633568948830189458628227828
80181199384826282014278194139940567587151170094390
35398664372827112653829987240784473053190104293586
86515506006295864861532075273371959191420517255829
71693888707715466499115593487603532921714970056938
54370070576826684624621495650076471787294438377604
53282654108756828443191190634694037855217779295145
36123272525000296071075082563815656710885258350721
45876576172410976447339110607218265236877223636045
17423706905851860660448207621209813287860733969412
81142660418086830619328460811191061556940512689692
51934325451728388641918047049293215058642563049483
62467221648435076201727918039944693004732956340691
15732444386908125794514089057706229429197107928209
55037687525678773091862540744969844508330393682126
18336384825330154686196124348767681297534375946515
80386287592878490201521685554828717201219257766954
78182833757993103614740356856449095527097864797581
16726320100436897842553539920931837441497806860984
48403098129077791799088218795327364475675590848030
87086987551392711854517078544161852424320693150332
59959406895756536782107074926966537676326235447210
69793950679652694742597709739166693763042633987085
41052684708299085211399427365734116182760315001271
65378607361501080857009149939512557028198746004375
35829035317434717326932123578154982629742552737307
94953759765105305946966067683156574377167401875275
88902802571733229619176668713819931811048770190271
25267680276078003013678680992525463401061632866526
36270218540497705585629946580636237993140746255962
24074486908231174977792365466257246923322810917141
91430288197103288597806669760892938638285025333403
34413065578016127815921815005561868836468420090470
23053081172816430487623791969842487255036638784583
11487696932154902810424020138335124462181441773470
63783299490636259666498587618221225225512486764533
67720186971698544312419572409913959008952310058822
95548255300263520781532296796249481641953868218774
76085327132285723110424803456124867697064507995236
37774242535411291684276865538926205024910326572967
23701913275725675285653248258265463092207058596522
29798860272258331913126375147341994889534765745501
18495701454879288984856827726077713721403798879715
38298203783031473527721580348144513491373226651381
34829543829199918180278916522431027392251122869539
40957953066405232632538044100059654939159879593635
29746152185502371307642255121183693803580388584903
41698116222072977186158236678424689157993532961922
62467957194401269043877107275048102390895523597457
23189706772547915061505504953922979530901129967519
86188088225875314529584099251203829009407770775672
11306739708304724483816533873502340845647058077308
82959174767140363198008187129011875491310547126581
97623331044818386269515456334926366572897563400500
42846280183517070527831839425882145521227251250327
55121603546981200581762165212827652751691296897789
32238195734329339946437501907836945765883352399886
75506164965184775180738168837861091527357929701337
62177842752192623401942399639168044983993173312731
32924185707147349566916674687634660915035914677504
99518671430235219628894890102423325116913619626622
73267460800591547471830798392868535206946944540724
76841822524674417161514036427982273348055556214818
97142617910342598647204516893989422179826088076852
87783646182799346313767754307809363333018982642090
10848802521674670883215120185883543223812876952786
71329612474782464538636993009049310363619763878039
62184073572399794223406235393808339651327408011116
66627891981488087797941876876144230030984490851411
60661826293682836764744779239180335110989069790714
85786944089552990653640447425576083659976645795096
66024396409905389607120198219976047599490197230297
64913982680032973156037120041377903785566085089252
16730939319872750275468906903707539413042652315011
94809377245048795150954100921645863754710598436791
78639167021187492431995700641917969777599028300699
15368713711936614952811305876380278410754449733078
40789923115535562561142322423255033685442488917353
44889911501440648020369068063960672322193204149535
41503128880339536053299340368006977710650566631954
81234880673210146739058568557934581403627822703280
82616570773948327592232845941706525094512325230608
22918802058777319719839450180888072429661980811197
77158542502016545090413245809786882778948721859617
72107838435069186155435662884062257473692284509516
20849603980134001723930671666823555245252804609722
53503534226472524250874054075591789781264330331690
=#


#= 
Problem 14
ans = 837799
The following iterative sequence is defined for the set of positive integers:

n → n/2 (n is even)
n → 3n + 1 (n is odd)

Using the rule above and starting with 13, we generate the following sequence:

13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1
It can be seen that this sequence (starting at 13 and finishing at 1) contains 10 terms. Although it has not been proved yet (Collatz Problem), it is thought that all starting numbers finish at 1.

Which starting number, under one million, produces the longest chain?

NOTE: Once the chain starts the terms are allowed to go above one million. 
=#

#= 
Problem 15
ans = 137846528820
Starting in the top left corner of a 2×2 grid, and only being able to move to the right and down, there are exactly 6 routes to the bottom right corner.


How many such routes are there through a 20×20 grid?
=#

#=
 Problem 17
If the numbers 1 to 5 are written out in words: one, two, three, four, five, then there are 3 + 3 + 5 + 4 + 4 = 19 letters used in total.

If all the numbers from 1 to 1000 (one thousand) inclusive were written out in words, how many letters would be used?


NOTE: Do not count spaces or hyphens. For example, 342 (three hundred and forty-two) contains 23 letters and 115 (one hundred and fifteen) contains 20 letters. The use of "and" when writing out numbers is in compliance with British usage.
=#


function digit_sum(number)
    num_str = string(number)
    total = 0
    for digit in num_str
        total += parse(Int, digit)
    end
    return total
end


#@time pythag_triple(322256352)
#println(pythag_triple(3279929268306))


