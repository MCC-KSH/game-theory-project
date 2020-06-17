def parsing(filename, params, line_number, mode, flag):
    prefix = "./result2/"
    open_filename = prefix + "[" + str(params[0]) + "][" + str(params[1]) + "][" + str(params[2]) + "][" + str(params[3]) + "] simulation_result.txt"
    f = open(open_filename)
    lines = f.readlines()
    f.close()

    types = ["[OVER]", "[RATE]", "[GAIN]", "[SWIT]", "[CONV]"]

    cnt = 0
    data = lines[line_number + (mode*50)*flag].split()
    for j in range(5):
        write_filename = prefix + types[j] + filename
        f = open(write_filename, 'a')
        for i in range(5):
            f.write(data[i*5 + j] + "\t")
        f.close()

def newline(filename):
    prefix = "./result2/"
    types = ["[OVER]", "[RATE]", "[GAIN]", "[SWIT]", "[CONV]"]
    for j in range(5):
        write_filename = prefix + types[j] + filename
        f = open(write_filename, 'a')
        f.write("\n")
        f.close()

if __name__ == "__main__":
    list_NUMBER_OF_UE = [100, 150, 200, 250, 300]
    list_NUMBER_OF_SUBCARRIER = [10, 15, 20, 25, 30]
    list_UE_TX_POWER = [50, 100, 150, 200, 250, 300]
    list_F_N = [0.5*10**9, 1.0*10**9, 1.5*10**9, 2.0*10**9, 2.5*10**9, 3.0*10**9]

    default_NUMBER_OF_UE = 200
    default_NUMBER_OF_SUBCARRIER = 20
    default_UE_TX_POWER = 100
    defualt_F_N = 1.0*10**9

    for line in range(50):
        for ue in list_NUMBER_OF_UE:
            params = [ue, default_NUMBER_OF_SUBCARRIER, default_UE_TX_POWER, defualt_F_N]
            if ue == default_NUMBER_OF_UE:
                parsing("[UE] result.txt", params, line, 0, 1)
            else:
                parsing("[UE] result.txt", params, line, 0, 0)
        newline("[UE] result.txt")
    
    for line in range(50):
        for sc in list_NUMBER_OF_SUBCARRIER:
            params = [default_NUMBER_OF_UE, sc, default_UE_TX_POWER, defualt_F_N]
            if ue == default_NUMBER_OF_UE:
                parsing("[SC] result.txt", params, line, 1, 1)
            else:
                parsing("[SC] result.txt", params, line, 1, 0)
        newline("[SC] result.txt")

    for line in range(50):
        for power in list_UE_TX_POWER:
            params = [default_NUMBER_OF_UE, default_NUMBER_OF_SUBCARRIER, power, defualt_F_N]
            if ue == default_NUMBER_OF_UE:
                parsing("[PW] result.txt", params, line, 2, 1)
            else:
                parsing("[PW] result.txt", params, line, 2, 0)
        newline("[PW] result.txt")

    for line in range(50):
        for fn in list_F_N:
            params = [default_NUMBER_OF_UE, default_NUMBER_OF_SUBCARRIER, default_UE_TX_POWER, fn]
            if ue == default_NUMBER_OF_UE:
                parsing("[FN] result.txt", params, line, 3, 1)
            else:
                parsing("[FN] result.txt", params, line, 3, 0)
        newline("[FN] result.txt")