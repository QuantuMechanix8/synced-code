with open("/home/saulivor/Desktop/Work/Coding/Python/OtherPrograms/Project Euler/LargeSum.txt") as f:
    sum = 0
    for line in f.readlines():
        sum += int(line)
    print(sum)