if __name__ == '__main__':

    with open('/home/desk/Desktop/minimap/1.txt') as f:
        for line in f:
            line = line.rstrip().split("\t")
            print(
                line[0],
                int(line[1]),
                int(line[2]),
                int(line[3]),
                line[4],
                line[5],
                int(line[6]),
                int(line[7]),
                int(line[8]),
                int(line[9]),
                int(line[10]),
                int(line[11])
            )

