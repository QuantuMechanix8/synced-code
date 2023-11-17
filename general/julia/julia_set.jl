using Plots
using Unzip


τ = 2π
start_value = -0.23 + 0.75im
marker_size = 0.3

function in_mandelbrot(z, c = z; max_iterations=800)
    for n ∈ 1:max_iterations
        if abs(z) >= 2
            return false
        end
        z = z^2 + c
    end
    return true
end

a_values = -2:0.005:1.5
b_values = -1.5:0.005:1.2

mandelbrot_set = [(a,b) for a ∈ a_values for b ∈ b_values if in_mandelbrot(a+b*im, start_value)]
real_mandelbrot_values, imaginary_mandelbrot_values = unzip(mandelbrot_set)

scatter(real_mandelbrot_values, imaginary_mandelbrot_values, markersize=marker_size, color="black")


