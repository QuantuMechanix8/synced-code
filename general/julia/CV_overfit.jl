using Random
using LinearAlgebra
using Statistics
using Plots
using PlotThemes

# Set theme
theme(:dracula)

# Set seed for reproducibility
Random.seed!(43)

# Generate synthetic data
function generate_data(n = 60)
	x = LinRange(-1, 1, n)
	y = 0.3 .* x .^ 3 .+ 0.2 .* x .^ 5 .+ 0.1 .* sin.(10x) .+ 0.1 * randn(n)  # Underlying pattern + noise
	return x, y
end

# the underlying pattern is a quintic polynomial with some noise

# Polynomial features
function polynomial_features(x, degree)
	X = hcat([x .^ d for d in 0:degree]...)
	return X
end

# Fit polynomial regression
function fit_polynomial(x, y, degree)
	X = polynomial_features(x, degree)
	β = X \ y  # Least squares solution
	return β
end

# Predict using polynomial model
function predict_polynomial(x, β, degree)
	X = polynomial_features(x, degree)
	return X * β
end

# Mean squared error
function mse(y_true, y_pred)
	return mean((y_true .- y_pred) .^ 2)
end

# K-fold cross-validation to determine the best polynomial degree
function k_fold_validation(x, y, deg, k = 5)
	n = length(x)
	fold_size = Int(floor(n / k))
	scores = zeros(k)

	for i in 1:k
		# Split data
		indices = (i-1)*fold_size.+1:i*fold_size
		x_test, y_test = x[indices], y[indices]
		x_train, y_train = vcat(x[1:indices[1]-1], x[indices[end]+1:end]), vcat(y[1:indices[1]-1], y[indices[end]+1:end])

		# Fit and evaluate
		β = fit_polynomial(x_train, y_train, deg)
		y_pred = predict_polynomial(x_test, β, deg)
		scores[i] = mse(y_test, y_pred)
	end

	return mean(scores)
end

function holdout_regression(x, y, deg, test_size = 0.2)
	Random.seed!(42) # for reproducibility

	n = length(x)
	n_test = Int(round(test_size * n))
	test_indices = randperm(n)[1:n_test]
	train_indices = setdiff(1:n, test_indices)

	# Split data
	x_train, y_train = x[train_indices], y[train_indices]
	x_test, y_test = x[test_indices], y[test_indices]

	# Fit and evaluate
	β = fit_polynomial(x_train, y_train, deg)
	y_pred = predict_polynomial(x_test, β, deg)

	println("MSE $(deg): ", mse(y_test, y_pred))

	# plot results
	scatter(x_train, y_train, label = "Train", xlabel = "x", ylabel = "y", title = "Holdout Validation", legend = :topleft, color = :blue)
	scatter!(x_test, y_test, label = "Test", color = :red)
	# plot the regression line
	x_plot = LinRange(-1, 1, 100)
	y_plot = predict_polynomial(x_plot, β, deg)
	plot!(x_plot, y_plot, label = "Regression", color = :green, linewidth = 2)
	display(current())
end

# Main script
function main()
	# Generate data
	x, y = generate_data(100)

	# Evaluate models of different degrees
	degrees = 1:10
	cv_scores = [kfold_cv(x, y, d) for d in degrees]
	holdout_scores = [holdout_validation(x, y, d) for d in degrees]

	# Plot results
	plot(degrees, cv_scores, label = "CV Score", xlabel = "Polynomial Degree", ylabel = "MSE", title = "CV vs Holdout", linewidth = 2)
	plot!(degrees, holdout_scores, label = "Holdout Score", linewidth = 2)
end

# Run the script
main()
