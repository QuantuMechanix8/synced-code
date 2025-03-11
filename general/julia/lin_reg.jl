using GLMakie
using Polynomials
using LaTeXStrings

# Code used to demonstrate the concept of residual and 'explained' variance -  for ML course

# merge dark and latex theme
my_theme = merge(theme_dark(), theme_latexfonts())
set_theme!(my_theme)

n = 20

x = range(0, 10, n)
y = [5-x/2 + 4*rand() for x in x]

reg_line = fit(x, y, 1)

y_mean = sum(y) / n

fig = Figure()
ax = Axis(fig[1, 1])
scatter!(ax, x, y, color = :royalblue, label = "Actual values")
plot!(ax, x, reg_line.(x), color = :tomato, label = "Regression line")
hlines!(ax, [y_mean], color = :lightblue, linestyle = :dash, label = L"$\bar{y}$")

# plot vertical lines between the data points and the regression line
for i in 1:n
	lines!(ax, [x[i], x[i]], [y[i], reg_line(x[i])], color = :lightskyblue, linestyle = :dot, linewidth = 1)
	lines!(ax, [x[i], x[i]], [reg_line(x[i]), y_mean], color = :orange, linestyle = :dot)
end

# Create dummy plot objects for the legend
dummy_line1 = lines!(ax, [0], [0], color = :lightskyblue, linestyle = :dot, linewidth = 1, label = "residual variance")
dummy_line2 = lines!(ax, [0], [0], color = :orange, linestyle = :dot, label = "'explained' variance")

# Add legend
axislegend(ax, framevisible = true, framecolor = :gray, margin = (1, 1, 1, 1), backgroundcolor = :transparent)

fig
