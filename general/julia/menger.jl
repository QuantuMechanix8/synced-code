using Luxor

function menger(corners, n)
    if n == 0
        poly(corners, :fill)
        return
    end
    # compute middle square co-ords and draw it, then perform recursion on all 8 sub-squares
    subsquares = get_subsquares(corners, 3)
    mid_square = 5
    for subsquare in [subsquares[1:mid_square-1]; subsquares[mid_square+1:end]] # don't draw mid square 
        menger(subsquare, n-1)
    end
end


function get_subsquares(corners, sf = 3)
    subsquares = []
    q1, q2, q3, q4 = corners # from top-left clockwise
    width = q2.x - q1.x
    height = q3.y - q2.y
    width_step = (width / sf)
    height_step = (height / sf)

    for columns in 0:sf-1
        for rows in 0:sf-1
            top_left = q1 + (width_step * rows, height_step*columns)
            top_right = top_left + (width_step, 0)
            bottom_left = top_left + (0, height_step)
            bottom_right = top_left + (width_step, height_step)
            subsquare = [top_left, top_right, bottom_right, bottom_left]
            push!(subsquares, subsquare) 
        end
    end
    return subsquares
end

width = 1000

# initial square
p1 = Point(0, 0)
p2 = Point(width, 0)
p3 = Point(width, width)
p4 = Point(0, width)
initial_square = [p1,p2,p3,p4]


n = 0:6
for i in n
    Drawing(width, width, "fractals/menger/menger_$(i).svg")
    background("white")
    sethue("black")
    menger(initial_square, i)
    finish()
end

