using GLMakie
my_theme = merge(theme_dark(), theme_latexfonts())
set_theme!(my_theme)

"""
Takes a polar function f(r, θ) and plots it as a surface plot in Cartesian coordinates
KWARGS:
	points::Int: The number of points to plot (default = 20)
	r_l::Int: The lower bound of the radius (default = 0)
	r_u::Int: The upper bound of the radius (default = 1)
	θ_l::Int: The lower bound of the angle (default = -π/2)
	θ_u::Int: The upper bound of the angle (default = π/2)
    flat_proj::Bool: Whether to plot a flat projection of the domain (default = false)
"""
function polar_surface(f::Function; points::Int = 20, r_l = 0, r_u = 1, θ_l = -π / 2, θ_u = π / 2, flat_proj = false)
	radii = range(r_l, r_u, points)
	angles = range(θ_l, θ_u, points)

	z = [f(r, θ) for r in radii, θ in angles] 
	
    # Convert polar to Cartesian coordinates for plotting
	domain = [(r * cos(θ), r * sin(θ)) for r in radii, θ in angles] # domain is matrix of tuples (x,y)
	x = [d[1] for d in domain] # matrix of x values
	y = [d[2] for d in domain] # matrix of y values

	# Create the surface plot
	fig = Figure()

	ax = Axis3(fig[1, 1], title = L"Surface Plot of $f(r,θ)$", xlabel = L"$x$", ylabel = L"$y$", zlabel = L"$f(r,θ)$", aspect = :data)
	surface_plot = surface!(ax, x, y, z, colormap = :viridis, label = "Surface Plot", aspect = :data)

	# plot flat projection to show domain
	if flat_proj
		flat = zeros(size(z))
		flat_plot = surface!(ax, x, y, flat, colormap = [:gray], label = "Domain")
	end
	return fig
end
