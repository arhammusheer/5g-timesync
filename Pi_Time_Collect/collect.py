import serial
import threading
import time
import signal

BAUDRATE = 115200

# Read every ACM port
ports = ["/dev/ttyACM" + str(i) for i in range(10)]

# Check which ports are available
available_ports = []

for port in ports:
	try:
		print("Trying port " + port + "... ")
		ser = serial.Serial(port, BAUDRATE)
		available_ports.append(ser)
	except:
		pass

# Print available ports
print("Available ports:")
for port in available_ports:
	print(port.name)

if len(available_ports) == 0:
	print("No ports available")
	exit()

# Open ports
ser = [serial.Serial(port.name, BAUDRATE) for port in available_ports]

# Read data in parallel
def read_data(ser):
	while True:
		print("Reading data from " + ser.name + "... ")
		data = ser.readline().decode("utf-8").strip()

		# Name of port is the folder name
		name = ser.name.split("/")[-1]

				

		# Save data to file of same name as port

		# Write format: timestamp, data
		timestamp = time.time()
		with open(name + ".txt", "a") as f:
			f.write(str(timestamp) + "," + data + "\n")
	

# Initialize threads
threads = [threading.Thread(target=read_data, args=(ser[i],)) for i in range(len(ser))]

# Start threads
for thread in threads:
	thread.start()

# Wait for threads to finish
for thread in threads:
	thread.join()



# Close ports
for port in ser:
	port.close()