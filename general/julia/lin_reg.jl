using GLMakie
using Polynomials
using LaTeXStrings

# Code used to demonstrate the concept of residual and 'explained' variance -  for ML course

# merge dark and latex theme
my_theme = merge(theme_dark(), theme_latexfonts())
set_theme!(my_theme)

n = 20

x = range(0, 10, n)
y = [4 * rand() for x in x]

reg_line = fit(x, y, 1)

y_mean = sum(y) / n

fig = Figure()
ax = Axis(fig[1, 1])
scatter!(ax, x, y, color = :royalblue, label = "Actual values")
plot!(ax, x, reg_line.(x), color = :tomato, label = "Regression line")
hlines!(ax, [y_mean], color = :lightblue, linestyle = :dash, label = L"$\bar{y}$")

# plot vertical lines between the data points and the regression line
for i in 1:n
	pred = reg_line(x[i])
	point_x, point_y = x[i], y[i]
	point_between = (pred >= point_y && point_y >= y_mean) || (pred <= point_y && point_y <= y_mean)
	same_side = sign(point_y - y_mean) == sign(pred - y_mean)
	if !point_between
		if !same_side
			lines!(ax, [point_x, point_x], [y_mean, point_y], color = :lightskyblue, linestyle = :dot, linewidth = 1)
		else
			lines!(ax, [point_x, point_x], [pred, point_y], color = :lightskyblue, linestyle = :dot, linewidth = 1)
		end
	end
	lines!(ax, [point_x, point_x], [pred, y_mean], color = :orange, linestyle = :dot)
end

# Create dummy plot objects for the legend
dummy_line1 = lines!(ax, [0], [0], color = :lightskyblue, linestyle = :dot, linewidth = 1, label = "residual variance")
dummy_line2 = lines!(ax, [0], [0], color = :orange, linestyle = :dot, label = "'explained' variance")

# Add legend
axislegend(ax, framevisible = true, framecolor = :gray, margin = (1, 1, 1, 1), backgroundcolor = :transparent)

fig
