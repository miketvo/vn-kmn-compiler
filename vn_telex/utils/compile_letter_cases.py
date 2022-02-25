import sys


def print_help():
    print('Syntax: py compile_letter_cases.py <path/to/input/file> <encoding> <path/to/output/file>')


def case_permutations(n):
    permutations_string = [bin(x)[2:].rjust(n, '0') for x in range(2 ** n)]
    permutations = []

    for permutation_string in permutations_string:
        permutation = []
        for digit in permutation_string:
            if digit == '0':
                permutation.append(False)
            else:
                permutation.append(True)
        permutations.append(permutation)

    return permutations


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print_help()
    else:
        encoding = 'utf-8'
        if len(sys.argv) > 2:
            encoding = sys.argv[2]

        lines = []
        file = open(sys.argv[1], 'r', encoding=encoding)
        for line in file:
            line = line.strip()
            lines.append(line)
        file.close()

        outs = []
        for line in lines:
            p = case_permutations(len(line))
            for i in range(len(p)):
                out = ''
                for char_pos in range(len(line)):
                    if p[i][char_pos]:
                        out += line[char_pos].upper()
                    else:
                        out += line[char_pos].lower()
                outs.append(out)

        if len(sys.argv) <= 2:
            file = open(sys.argv[1], 'w', encoding=encoding)
        else:
            file = open(sys.argv[3], 'w', encoding=encoding)
        for line in outs:
            file.write(line)
            file.write('\n')
        file.close()
