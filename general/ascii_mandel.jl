function input(text; as_float = false)
	println(text)
	if as_float
		return parse(Float16, readline())
	end
	return readline()
end


function in_mandel(c::Complex; iterations::Int = 50)
	z = Complex{BigFloat}(c)
	for iteration in 1:iterations
		if abs(z) > 2
			#println("$c not in mandelbrot set, broke after $iteration iterations, |z| = $(abs(z)))")
			return false
		end
		z = z^2 + c
	end
	#println("$c in mandelbrot set (within $iterations iterations)")	
	return true
end


function in_julia(z::Complex, c::Complex; iterations::Int = 50)
	for interation in 1:iterations
		if abs(z) > 10
			return false
		end
		z = z^2 + c
	end
	return true 
end


function ascii_pixels(Rlower_bound, Rupper_bound, Rstep, Ilower_bound, Iupper_bound, Istep, c; iterations = 20)
           for I in Iupper_bound:-Istep:Ilower_bound
               for R in Rlower_bound:Rstep:Rupper_bound
                   if I == 0 && R == 0
                       print("O")
                   elseif I == 0
                       print("-")
                   elseif R == 0
                       print("|")
                   else
                       z = Complex(R, I)
                       set_element = in_julia(z, c)
                       if set_element
                           print("#")
                       elseif !set_element
                           print(" ")
                       end
                   end
               end
               println()
           end
       end

c = parse(Complex{Float16}, input("value of c:"))

Rlower_bound = input("Lower bound for reals:", as_float = true)
Rupper_bound = input("Upper bound for reals:", as_float = true)
Rstep = input("step size for reals:", as_float = true)

Ilower_bound = input("Lower bound for imaginary:", as_float = true)
Iupper_bound = input("Upper bound for imaginary:", as_float = true)
Istep = input("step size for imaginary:", as_float = true)

num_iterations = input("how many iterations:", as_float = true)

ascii_pixels(Rlower_bound, Rupper_bound, Rstep, Ilower_bound, Iupper_bound, Istep, c; iterations = num_iterations)
