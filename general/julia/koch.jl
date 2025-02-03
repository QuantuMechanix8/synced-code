using Luxor

triangle_width = 1000 # sidelength
triangle_height = triangle_width * √3 / 2
koch_height = triangle_width * 2√3 / 3 # fractal is taller than base triangle
koch_width = triangle_width

function lerp(p1, p2, λ)
    return p1 + (p2-p1)*λ
end


function koch_points(p1, p2)
    # assign q1, q2, q3, q4, q5
    q1 = p1
    q5 = p2
    q2 = lerp(p1, p2, 1/3)
    q4 = lerp(p1,p2, 2/3)
    # q3 is the difficult one - top of triangle
    mid = (q4-q2)/2
    rotated_mid = Point(-mid.y, mid.x)
    q3 = q2 + mid + (rotated_mid * √3)

    return [q1,q2,q3,q4,q5]
end


function koch_line(p1, p2, n)
    if n==0
        line(p1, p2, action = :stroke)
        return
    else
        points = koch_points(p1,p2)
        for i in 1:length(points)-1
            koch_line(points[i], points[i+1], n-1)
        end
    end
end


function koch_snowflake(p1, p2, p3, n)
    koch_line(p1, p2, n)
    koch_line(p2, p3, n)
    koch_line(p3, p1, n)
end

width = 1000
Drawing(width*12/10, width*13/10, "koch.svg")
background("white")
sethue("black")
p1 = Point(koch_width/2, 0)
p2 = Point(0, triangle_height)
p3 = Point(koch_width, triangle_height)

n = 0:7
for i in n
    Drawing(koch_width, koch_height, "fractals/koch/koch_snowflake_$(i).svg")
    background("white")
    setline(3/(i+1))
    koch_snowflake(p1, p2, p3, i)
    finish()
end
