using Luxor
height, width = 950, 1100

function sierpinski(p1, p2, p3, n)
    if n == 0
        # base case, simply draw triangle
        poly([p1, p2, p3], :fill)
        return
    end
    # points are "in order traversal" i.e. top, left, right
    # compute midpoints
    mid1 = (p1+p2)/2
    mid2 = (p2+p3)/2
    mid3 = (p3+p1)/2
    
    tri1 = (p1, mid1, mid3)
    tri2 = (mid1, p2, mid2)
    tri3 = (mid3, mid2, p3)

    sierpinski(tri1..., n-1)
    sierpinski(tri2..., n-1)
    sierpinski(tri3..., n-1)
end

# initial triangle
p1 = Point(width/2, 0)
p2 = Point(0, height)
p3 = Point(width, height)

n = 0:8
for i in n
    Drawing(width, height, "fractals/sierpinski/sierpinski_$(i).svg")
    background("white")
    sierpinski(p1, p2, p3, i)
    finish()
end