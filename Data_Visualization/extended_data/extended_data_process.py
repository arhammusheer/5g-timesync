# Example Data : 1707847910474; Signal Strength: 58; IP Addr: 10.165.112.163; APN: globaldata.iot; SIM ICCID: 8931681011103547569; IMEI: 351901936542939; IMSI: 204080743148100; Modem FW Ver: mfw_nrf9160_1.3.5; Cell ID: 00ED4711

# Splits data first in to a list of strings seperated by ";" then it extracts k-v pairs from the list of strings and stores them in a dictionary

def extract_data(data):
		data = data.split(";")
		data = [i.strip() for i in data]
		data = [extract_kv_pairs(i) for i in data]
		return data

def extract_kv_pairs(data):
		d = data.split(":")

		if len(d) != 2:
				k = "Time"
				return {k:data}

		k = d[0].strip()
		v = d[1].strip()

		return {k:v}

def get_data(file_name):
		with open(file_name, "r") as f:
				data = f.readlines()
		data = [i.strip() for i in data]
		return data

def main():
		data = get_data("data.txt")
		data = [extract_data(i) for i in data]
		
		# Save data to file
		with open("data.json", "w") as f:
				f.write(str(data))


if __name__ == "__main__":
	main()
