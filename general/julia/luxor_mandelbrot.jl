using Luxor

p_width, p_height = 2000, 2000
width, height = 2.5,2
centre = (0, 0)

start_value = -0.23 + 0.74im

Drawing(p_width, p_height, "dot.png")
background("white")
sethue("black")

function in_mandel(z::Complex; c=z, iterations::Int = 50)
	z = Complex{BigFloat}(z)
	for iteration in 1:iterations
		if abs(z) > 2
			#println("$c not in mandelbrot set, broke after $iteration iterations, |z| = $(abs(z)))")
			return iteration
		end
		z = z^2 + c
	end
	#println("$c in mandelbrot set (within $iterations iterations)")	
	return true
end


function get_cartesian_coords(w,h)
    global p_width, p_height, width, height, centre
    x = (w/p_width - 0.5) 
    y = (h/p_height - 0.5)
    (x,y) = (x,y).+centre
    (x,y) = (x,y).*(width, height)
    return (x,y)
end


function tuple_lerp(A,B, p)
    return A .+ p.*(B.-A)
end

function tuple_interpolate(A,B,p,f = p->p)
    return A .+ f(p).*(B.-A)
end

function proportion_to_colour(p)
    black = (20,0,0)
    dark_red = (255, 255, 255)
    f = p->∛p
    return tuple_interpolate(dark_red, black, p, f)
end


function draw_point(w,h, color=(0,0,0))
    p = Point(w,h)
    unit = Point(0,1)
    color = color./255
    setcolor(color...)
    #print(getcolor())
    line(p, p+unit, action=:stroke) # can't figure out how to change the colour of my point each time????
end

total_iter = 60

for w in 1:p_width
    for h in 1:p_height
        x,y = get_cartesian_coords(w,h)
        z = x + im*y
        #println(z, in_mandel(z))
        iter = in_mandel(z,c=start_value, iterations=total_iter)
        if iter == true && isa(iter, Bool) # otherwise always evaluates to true
            draw_point(w,h)
        else
            colour = proportion_to_colour(iter/total_iter)
            draw_point(w,h,colour)
        end
    end
end
finish()