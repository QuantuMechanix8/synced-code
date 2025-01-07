# solving specific 4 case of combinatoric problem - permutations without fixed points
using Combinatorics


function generate_permutations(n = 4)
    return collect(permutations(1:n))
end


function check_fixed_points(perm)
    for i in 1:length(perm)
        if perm[i] == i
            return false
        end
    end
    return true
end


function count_fixed_points(n = 4)
    
end