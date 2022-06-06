import pprint





def write_grid(grid):
    with open('output.csv', 'w') as f:
        s = ""
        for line in grid:
            s += f"{','.join([str(int(x)) for x in line])}\n"
        print(s)
        f.write(s)


def solve_Couples(grid):
    x = 1
    for line in grid:
        for i in range(1, len(line)):
            if line[i] == line[i - 1] and not line[i] is None:
                if i != len(line) - 1:
                    line[i + 1] = not line[i]
                if i != 1:
                    line[i - 2] = not line[i]

            if line[i] == line[i - 2] and not line[i] is None and i != 1:
                line[i - 1] = not line[i]

        zeroComplete = line.count(0) == 3
        oneComplete = line.count(1) == 3

        if zeroComplete or oneComplete:  # line = [False if x is None else x for x in line] list comp cause deep copy
            for i in range(len(line)):
                if line[i] is None:
                    newVal = True if zeroComplete else False
                    line[i] = newVal
    return grid


def finished(grid):
    for line in grid:
        for cell in line:
            if cell is None:
                return False
    return True


def check(grid):

    rotGrid = tuple(zip(*reversed(grid)))

    # All rows different and all cols different
    if len(grid) != len(set(grid)) or len(rotGrid) != len(set(rotGrid)):
        return False

    for row in grid:
        if None in row:
            return False

        if row.count(True) != row.count(False) != 3:
            return False



    return True

def solve(grid):
    print("Input")
    pprint.pprint(grid)
    print()

    while not check(grid):
        grid = solve_Couples(grid.copy())

        print('Horizontal')
        pprint.pprint(grid)
        print()

        grid = [list(x) for x in zip(*reversed(grid))]
        grid = solve_Couples(grid.copy())
        grid = [list(x) for x in reversed(list(zip(*grid)))]

        print("Vertical")
        pprint.pprint(grid)
        print()

    print("Solved")
    pprint.pprint(grid)

    return grid


if __name__ == "__main__":
    write_grid(solve(get_grid()))
