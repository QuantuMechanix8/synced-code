using GameZero
using Colors

WIDTH = 1120
HEIGHT = 630
BACKGROUND = colorant"black"
FRAME = 0
POINTS = []

function draw(g::Game)
    for point in POINTS
        draw(point, colorant"white", fill=true)
    end    
end


function update(g::Game)
    new_point()
end


function new_point()
    """print("Point's x co-ord: ")
    x = parse(Int, readline())
    print("\nPoint's y co-ord: ")
    y = parse(Int, readline())
    push!(points, Circle(x,y,1))"""
    global FRAME
    x = cos(FRAME/90)
    y = sin(FRAME/90)
    x *= 0.9WIDTH/2
    y *= 0.9HEIGHT/2
    [x,y] .+= [WIDTH/2, HEIGHT/2]
    x = round(Int, x)
    y = round(Int, y)
    FRAME += 1
    push!(POINTS, Rect(x,y,1,1))
end
