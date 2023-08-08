import Distributions
import Dates


"""
`function rand_adult_birthday_normal()::Dates.Date`

return random adult birthday (18yr+) using rough normal approximation of ages - N(μ=30, σ=15)

#Examples
rand_adult_birthday_normal() -> 1975-09->23
"""
function rand_adult_birthday_normal()
    today = Dates.today()
    age_dist = Distributions.truncated(Distributions.Normal(30, 15), lower = 18) # age normal distribution with 18 as lower bound
    rand_age = rand(age_dist)
    rand_age_days = round(Int, rand_age%1 * Dates.daysinyear(today))
    rand_age = round(Int, rand_age)
    return today - Dates.Year(rand_age) - Dates.Day(rand_age_days)
end


"""
`function rand_adult_birthday_uniform()::Dates.Date`

return random adult birthday (18yr+) using a uniform distribution 

#Examples
rand_adult_birthday_normal() -> 1975-09->23
"""
function rand_adult_birthday_uniform()
    today = Dates.today()
    youngest_adult_birthday = today - Dates.Year(18)
    oldest_adult_birthday = today - Dates.Year(122) # oldest human was 122 so used as Upper bound
    return rand(oldest_adult_birthday:Dates.Day(1):youngest_adult_birthday) # older dates are considered smaller so come first
end

