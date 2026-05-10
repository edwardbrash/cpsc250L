temperatures = []

file = open("../data/june_temperatures.txt", "r")

for line in file:
    line = line.strip()

    if line != "":
        temperatures.append(int(line))

file.close()

total = 0

for value in temperatures:
    total = total + value

average = total / len(temperatures)

maximum = temperatures[0]

for value in temperatures:
    if value > maximum:
        maximum = value

minimum = temperatures[0]

for value in temperatures:
    if value < minimum:
        minimum = value

count = 0

for value in temperatures:
    if value > 80:
        count = count + 1

print("Temperature Report")
print("------------------")
print("Average temperature:", average)
print("Maximum temperature:", maximum)
print("Minimum temperature:", minimum)
print("Temperatures above 80:", count)
