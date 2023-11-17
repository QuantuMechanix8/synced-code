# The aim of this program is to provide all valid change for a given amount of money

DENOMINATIONS = (5, 10, 20, 50, 1_00, 2_00, 5_00, 10_00, 20_00, 50_00) # standard currency denominations

function get_change(amount; denominations=DENOMINATIONS, pounds=false)
    #println("amount is $(pounds ? "£$(amount)" : "$(amount)p")")
    current_amount = amount
    smallest_denomination = minimum(denominations)
    change = []
    while current_amount >= smallest_denomination
        valid_denominations = [denomination for denomination in denominations if (denomination <= current_amount)]
        largest_next_change = maximum(valid_denominations)
        push!(change, largest_next_change)
        current_amount -= largest_next_change
        if current_amount == 0
            return change
        end
    end
    println("Imperfect change")
    return change
end

#get_change(2.50, pounds=true)
println(get_change(121, pounds=false))
println(get_change(292, pounds=false))
println(get_change(360, pounds=false))