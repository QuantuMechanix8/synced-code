using BenchmarkTools
using PlotThemes
theme(:dracula)

function insertion_sort(A, n)
	for i ∈ 2:n
		key = A[i]
		j = i - 1
		while (j > 0) && (A[j] > key)
			A[j+1] = A[j]
			j -= 1
		end
		A[j+1] = key
	end
end

sizes = (1:30) .* 5000 # sizes of arrays to sort


# plot graph of time complexity
using Plots

times = []
for n in sizes
	# run insertion_sort on random array of size n and record time
	A = rand(1:100, n)
	time_dist = @elapsed insertion_sort(A, n)
	#eval_time = median(time_dist).time
	push!(times, time_dist)
end

plot(sizes, times, label = "insertion_sort", xaxis = "n", yaxis = "time (s)")
