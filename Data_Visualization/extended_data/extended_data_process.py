# 1707851067.2369373,1707851110040; Signal Strength: 69; IP Addr: 10.165.234.37; APN: globaldata.iot; SIM ICCID: 8931681011103550381; IMEI: 351901936540628; IMSI: 204080743148382; Modem FW Ver: mfw_nrf9160_1.3.5; Cell ID: 00ED4711

import os
import json

# Extract data from string
def extract_data(data):
		# Extract pi
		data = data.split(",", 1)

		pi = data[0].strip()

		# Remove pi from data
		data = data[1]

		# Remaing data after pi		
		data = data.split(";")
		data = [i.strip() for i in data]
		data = [extract_kv_pairs(i) for i in data]

		# Add pi to data
		data.append({"pi":pi})

		

		# Merge all dictionaries
		data = {k:v for i in data for k,v in i.items()}
		
		return data

def extract_kv_pairs(data):
		d = data.split(":")

		if len(d) != 2:
				k = "time"
				return {k:data}

		
		k = d[0].strip()
		# replace space with underscore
		k = k.replace(" ", "_")
		# To lower case
		k = k.lower()

		v = d[1].strip()
		return {k:v}

def get_data(file_name):
		with open(file_name, "r") as f:
				data = f.readlines()
		data = [i.strip() for i in data]
		return data


def save_to_file(data, file_name):
		with open(file_name, "w") as f:
				json.dump(data, f)

def main():
		directory = "data/"
		save_directory = "processed_data/"
		files = os.listdir(directory)

		# Create save directory if it does not exist
		if not os.path.exists(save_directory):
				os.makedirs(save_directory)

		for file in files:
				file_name = directory + file
				save_name = save_directory + file + ".json"
				data = get_data(file_name)
				data = [extract_data(i) for i in data]
				save_to_file(data, save_name)


		

if __name__ == "__main__":
		main()
