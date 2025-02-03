# separate since for this case we have r(θ) in our domain - so can't easily use my generalized function in polar_surface_plot.jl

using GLMakie
my_theme = merge(theme_dark(), theme_latexfonts())
set_theme!(my_theme)

f(r, θ) = -log(r) # logarithm of 1/r - for better plotting

# Define the range for r and theta

points = 100
angle_ub = π / 2 - 0.05 # to avoid division by zero
angle_lb = -π / 2 + 0.05 # to avoid division by zero

angles = range(angle_lb, angle_ub, points) # Angle from 0.1 to 2π radians

domain = [[(r,θ) for r in range(0.01, 2cos(θ), points)] for θ in angles]
mat_domain = hcat(domain...) # flatten domain into matrix

radii = [d[1] for d in mat_domain] # r values
angles = [d[2] for d in mat_domain] # θ values
# Create the function
z = f.(radii, angles) # flatten results into vector
# Convert polar to Cartesian coordinates for plotting
x = radii .* cos.(angles) # x values
y = radii .* sin.(angles) # y values

# Create the surface plot
fig = Figure()

ax = Axis3(fig[1, 1], title = L"Surface Plot of $f(r,θ) = 1/r$", xlabel = L"$x$", ylabel = L"$y$", zlabel = L"$\text{ln}\,f(r,θ)$")
surface_plot = surface!(ax, x, y, z, colormap = :viridis, label = "Surface Plot")

# plot flat projection to show domain
flat = zeros(size(z)) .- 1
flat_plot = surface!(ax, x, y, flat, colormap = [:gray], label = "Domain")

display(fig)
