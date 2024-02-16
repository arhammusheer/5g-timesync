import json
import matplotlib.pyplot as plt
import os

def load_processed_files(directory):
		# Load all files
		files = os.listdir(directory)
		data = []
		for file in files:
				file_name = directory + file
				with open(file_name, "r") as f:
						data.append(json.load(f))
		return data

		
def plot_data(data):
		fil1 = data[0]
		fil2 = data[1]

		cell_ids = []

		for (i, v) in enumerate(fil1):
				try:
					cell_ids.append(v["Cell ID"])
				except:
					cell_ids.append("Missing")

		# Save cell ids
		with open("cell_ids.json", "w") as f:
				json.dump(cell_ids, f)

		# Get change in cell ids
		changes = []
		for (i, v) in enumerate(fil2):
				try:
					changes.append(v["Cell ID"] != cell_ids[i])
				except:
					changes.append("Missing")

		# Plot changes
		plt.plot(changes)
		plt.show()





		
		




		
def main():
		directory = "processed_data/"
		data = load_processed_files(directory)
		plot_data(data)

if __name__ == "__main__":
		main()