from matplotlib import pyplot as plt

def read_data(file_name):
		# Read data from file
		# Format x0,y0
		with open(file_name, "r") as f:
				data = f.readlines()
		# Convert data to integers
		data = [i.strip() for i in data]
		x, y = [], []
		
		for i in data:
				x.append(i.split(",")[0])
				y.append(i.split(",")[1])
				
		x = [float(i) for i in x]
		y = [float(i) for i in y]
		return x, y

def main():
	err = []
	x, y = read_data("board1.txt")

	# Remove initial offset
	initial = y[0]

	for i in y:
		err.append(i - initial)

	# y[i] is suppposed to be 5000 + y[i-1]
	# Find error
	for i in range(1, len(y)):
		err[i] = y[i] - (5000 + y[i-1])



		

	# Zero line
	# plt.plot(x, [0 for i in range(len(y))], "r--")

	plt.plot(x, err)
	plt.xlabel("Time")
	plt.ylabel("Error")
	plt.show()

	


if __name__ == "__main__":
	main()
