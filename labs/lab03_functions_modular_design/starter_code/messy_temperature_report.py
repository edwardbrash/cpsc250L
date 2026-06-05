# create an empty list to hold temps
temperatures = []

# open the file and attach to a socket called file
file = open("../data/june_temperatures.txt", "r")

# loop over each line in the file
for line in file:
    # strip off the \n at the end of the line
    line = line.strip()

    # if the line is not empty, convert to int and add to list
    if line != "":
        temperatures.append(int(line))

# close the file
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
