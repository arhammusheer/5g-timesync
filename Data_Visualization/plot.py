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
    experiment_number = 0

    x0, y0 = read_data(f"board0_experiment{experiment_number}.txt")
    x1, y1 = read_data(f"board1_experiment{experiment_number}.txt")

    # Zero line
    _0 = [0 for _ in range(len(y0))]
    # Zero line
    plt.plot(_0, "r--")


    err0 = []
    err1 = []

    for i in range(1, len(y0)):
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
