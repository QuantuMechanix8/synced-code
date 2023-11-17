using GameZero
using Colors

#Globals
WIDTH = 600
HEIGHT = 600
CENTER = [WIDTH÷2, HEIGHT÷2]
X_RANGE = 5 # always centred on origin
Y_RANGE = 5
BACKGROUND = colorant"grey"


"""Function to plot a single pixel on the screen at a given position"""
function plot_point(x, y)
    point = Rect(x, y, 1, 1)
    draw(point)
end


function coord_to_cartesian(x, y)
    x_df = (WIDTH/X_RANGE) # 'dividing factor' for x and y
    y_df = (HEIGHT/Y_RANGE)
    x,y = [x, y] .- CENTER
    y = -y #flip vertical so that +ve is upwardsj
    return [x,y] ./ [x_df, y_df]
end


function cartesian_to_coord(x,y)
    x_sf = WIDTH/X_RANGE
    y_sf = HEIGHT/Y_RANGE
    x, y = [x,y] .* [x_sf, y_sf]
    y = -y
    x, y = map(x->round(Int,x), [x,y])
    return [x, y] .+ CENTER
end
    

function plot_func(x_arr::Vector{<:Real}, f::Function)
    global X_RANGE = 2*maximum(map(x->abs(x), x_arr))
    y_arr = map(f, x_arr)
    global Y_RANGE = 2*maximum(map(x->abs(x), x_arr))
    all_points = zip(x_arr, y_arr)
    for point ∈ all_points
        plot_point(point...)
    end 
end


"""generates random complex number to uniform distribution centred at 0 with provided radius (of complex square from which points are taken)"""
function random_complex(radius)
    random = rand(ComplexF64)
    random -= 0.5 + 0.5im
    return random*2radius
end

#start_seed = random_complex(3)
#value = start_seed

function draw(g::Game)
    f(x) = x^2
    plot_func([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5], f)
    #value = value^2 + value
end