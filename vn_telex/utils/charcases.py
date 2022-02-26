import sys


def print_help():
    print('Syntax: py charcases.py <path/to/input/file> <encoding> <path/to/output/file>')


def gen_case_permutations_matrix(n):
    matrix_str = [bin(x)[2:].rjust(n, '0') for x in range(2 ** n)]
    matrix = []

    for line_str in matrix_str:
        permutation = []
        for digit in line_str:
            if digit == '0':
                permutation.append(False)
            else:
                permutation.append(True)
        matrix.append(permutation)

    return matrix


def gen_case_permutations(s):
    result = []
    matrix = gen_case_permutations_matrix(len(line))
    for i in range(len(p)):
        permutation = ''
        for char_pos in range(len(line)):
            if matrix[i][char_pos]:
                permutation += line[char_pos].upper()
            else:
                permutation += line[char_pos].lower()
        result.append(permutation)

    return result


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
            for case in gen_case_permutations(line):
                outs.append(case)

        if len(sys.argv) <= 2:
            file = open(sys.argv[1], 'w', encoding=encoding)
        else:
            file = open(sys.argv[3], 'w', encoding=encoding)
        for line in outs:
            file.write(line)
            file.write('\n')
        file.close()
