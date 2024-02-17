from matplotlib import pyplot as plt

# def read_data(file_name):
#     # Read data from file
#     # Format x0,y0
#     with open(file_name, "r") as f:
#         data = f.readlines()
#     # Convert data to integers
#     data = [i.strip() for i in data]
#     x, y = [], []
    
#     for i in data:
#         x.append(i.split(",")[0])
#         y.append(i.split(",")[1])
        
#     x = [float(i) for i in x]
#     y = [float(i) for i in y]
#     return x, y

def read_data(file_name):
    with open(file_name, "r") as f:
        data = f.readlines()

    x, y = [], []
    
    for line in data:
        parts = line.split(",")  # Splitting by comma
        if len(parts) > 1:
            first_number = float(parts[0].strip())  # First number before comma
            # print("x =",first_number)

            # Extracting the second number which follows "Time:"
            time_str = parts[1].split(";")[0].strip()  # Isolating the part with "Time:"
            second_number_str = time_str.split("Time:")[1].strip() if "Time:" in time_str else None
            # print(second_number_str)
            if second_number_str:
                second_number = float(second_number_str)
            # print("y =",second_number)

            x.append(first_number)
            y.append(second_number)
    
    return x, y






def main():
    experiment_number = 5

    x0, y0 = read_data(f"board0_experiment{experiment_number}.txt")
    x1, y1 = read_data(f"board1_experiment{experiment_number}.txt")

    # Zero line
    _0 = [0 for _ in range(len(y0))]
    # Zero line
    plt.plot(_0, "r--")


    err0 = []
    err1 = []

    data_range = min(len(y0),len(x0))
    
    print("y[-1]=%f , x[-1]=%fy0 , y[-1]-x[-1]*1000=%f"%(y0[data_range-1],x0[data_range-1],y0[data_range-1]-x0[data_range-1]*1000))


    # for i in range(1, len(y0)):
    for i in range(1,data_range):
        err0.append(y0[i] - x0[i]*1000)
        err1.append(y1[i] - x1[i]*1000)


    plt.plot(err0, label="Board 0")
    plt.plot(err1, label="Board 1")

    
    plt.xlabel("Time")
    plt.ylabel("Error")
    plt.legend()
    plt.savefig(f"experiment{experiment_number}.png")
    
    


if __name__ == "__main__":
    main()
