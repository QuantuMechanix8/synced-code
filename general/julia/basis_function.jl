using GLMakie
using LaTeXStrings

my_theme = merge(theme_dark(), theme_latexfonts())
set_theme!(my_theme)


# we define the follwing basis functions - for a 2d input (x₁, x₂)
ϕ₁(x) = x[1]
ϕ₂(x) = x[2]
ϕ₃(x) = x[1] * x[2]

f(x) = 1 - 2ϕ₁(x) - 2ϕ₂(x) + 4ϕ₃(x) # regression function in transformed space
# plot this in 3d

#setup figure/axis
fig = Figure(fontsize = 30, figure_padding = 10, transparency = true);
ax = Axis3(fig[1, 1], xlabel = L"x_1", ylabel = L"x_2", zlabel = L"z = f(x_1, x_2)", title = L"f(\textbf{x}) := 1 - 2\phi_1(\textbf{x}) - 2\phi_2(\textbf{x} ) + 4\phi_3(\textbf{x})")

# generate data
x₁ = LinRange(-1, 2, 60)
x₂ = LinRange(-1, 2, 60)
z = [f([x₁, x₂]) for x₁ in x₁, x₂ in x₂]

# plot region where f(x) = 0 - i.e. plane z=0 - in transparent gray
flat = zeros(60, 60)
flat_surface = surface!(ax, x₁, x₂, flat, color = Pattern('#'), transparency = true, label = L"z = 0")
#surface!(ax, x₁, x₂, flat, color=(:yellow, 0.5), transparency=true)

surface_plot = surface!(ax, x₁, x₂, z, colormap = :viridis, transparency = false, label = L"f(\textbf{x})")

intersection_line = contour!(ax, x₁, x₂, z, levels = [0], linewidth = 5, color = :red, label = "f(\textbf{x}) = 0")

# surface plot legend entry
viridis_median_color = cgrad(:viridis)[0.5];
surface_plot_legend = PolyElement(color=viridis_median_color, strokecolor=:black, strokewidth=1)
# flat surface legend entry
flat_surface_legend = PolyElement(color=Pattern('#'), strokecolor=:black, strokewidth=1)
# intersection line legend entry
intersection_line_legend = LineElement(color=:red, strokecolor=:black, strokewidth=5)

# add a legend, with surface plot (colorblock), flat plane (hatching) and intersection line (red)

Legend(fig[1, 2],
    [surface_plot_legend, flat_surface_legend, intersection_line_legend],
	[L"f(\textbf{x})", L"z = 0", L"f(\textbf{x}) = 0"],
    patchsize=(30, 30))


# Can't get layout to work GRRR
fig
