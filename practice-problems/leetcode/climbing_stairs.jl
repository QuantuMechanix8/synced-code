#= 
You are climbing a staircase, it takes n steps to reach the top
each time you can either climb 1 or 2 steps 
How many distinct ways can you reach the top?
=# 

function climb_stairs(n::Int)
    if n == 1
        return 1
    elseif n == 2
        return 2
    else
        return climb_stairs(n-1) + climb_stairs(n-2) # very fibonacci
    end
end


function iterative_climb_stairs(n::Int)
    ϕ::Float64 = (1+√5)/2
    n+=1
    return floor(Int, (ϕ^n - (-ϕ)^(-n)) / √5)
end