def list_str_to_int(l):
    res = []
    for i in l:
        res.append(int(i))
    return res

def list_str_to_float(l):
    res = []
    for i in l:
        res.append(float(i))
    return res

MENU = [
    "1. Add matrices",
    "2. Multiply matrix by a constant",
    "3. Multiply matrices",
    "4. Transpose matrix",
    "5. Calculate a determinant",
    "6. Inverse matrix",
    "0. Exit"
]

TRANSPOSE = [
    "1. Main diagonal",
    "2. Side diagonal",
    "3. Vertical line",
    "4. Horizontal line"
]

def menu():
    print(*MENU, sep="\n")

def t_menu():
    print(*TRANSPOSE, sep="\n")

def print_matrix(matrix):
    print("The result is: ")
    print('\n'.join(' '.join(['{}'.format(round(item, 2)) for item in row]) for row in matrix))


def read_matrix(n="first", constant=False):
    if not constant:
        metadata = list_str_to_int(input("Enter size of {} matrix: ".format(n)).strip().split(" "))
    else:
        metadata = list_str_to_int(input("Enter size of matrix: ").strip().split(" "))
    row, column = metadata[0], metadata[1]
    m = [[0 for x in range(column)] for y in range(row)]
    if not constant:
        print("Enter {} matrix: ".format(n))
    else:
        print("Enter matrix: ")
    for i in range(0, row):
        input_row = list_str_to_float(input().strip().split(" "))
        for j in range(0, column):
            m[i][j] = input_row[j]
    return m

def equal(matrix1, matrix2):
    return True if len(matrix1) == len(matrix2) and len(matrix1[0]) == len(matrix2[0]) else False

def add(matrix1, matrix2):
    if equal(matrix1, matrix2):
        matrix_sum = [[matrix1[i][j] + matrix2[i][j] for j in range(len(matrix1[0]))] for i in range(len(matrix1))]
        print_matrix(matrix_sum)
    else:
        print('The operation cannot be performed.')


def multiple_constant(matrix, scalar):
    matrix_multiple = [[matrix[i][j] * scalar for j in range(len(matrix[0]))] for i in range(len(matrix))]
    print_matrix(matrix_multiple)


def column(matrix, idx):
    ret = []
    for n in matrix:
        ret.append(n[idx])
    return ret

def multiple_matrices(matrix1, matrix2):
    if len(matrix1[0])  == len(matrix2):
        m = [[0 for x in range(len(matrix2[0]))] for y in range(len(matrix1))]
        # iterate through rows of X
        for i in range(len(matrix1)):
           # iterate through columns of Y
           for j in range(len(matrix2[0])):
               # iterate through rows of Y
               for k in range(len(matrix2)):
                   m[i][j] += matrix1[i][k] * matrix2[k][j]
        print_matrix(m)
    else:
        print('The operation cannot be performed.')


def transpose(matrix, diagonal=1):
    ret = [[0 for x in range(len(matrix))] for y in range(len(matrix[0]))]
    if diagonal == 1:
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                ret[j][i] = matrix[i][j]
        return ret
    elif diagonal == 2:
        for i in range(len(matrix)-1, -1, -1):
            for j in range(len(matrix[i])-1, -1, -1):
                ret[len(matrix[i]) - 1 - j][len(matrix) - 1 - i] = matrix[i][j]
        return ret
    elif diagonal == 3:
        for i in range(len(matrix)):
            for j in range(len(matrix[i]) - 1, -1, -1):
                ret[i][len(matrix[i]) - 1 - j] = matrix[i][j]
        return ret
    elif diagonal == 4:
        for i in range(len(matrix) - 1, -1, -1):
            for j in range(len(matrix[i])):
                ret[len(matrix) -1 - i][j] = matrix[i][j]
        return ret

def determinant(A, total=0):
    # Section 1: store indices in list for row referencing
    indices = list(range(len(A)))

    # Section 2: when at 2x2 submatrices recursive calls end
    if len(A) == 1 and len(A[0]) == 1:
        return A[0][0]

    if len(A) == 2 and len(A[0]) == 2:
        val = A[0][0] * A[1][1] - A[1][0] * A[0][1]
        return val

    # Section 3: define submatrix for focus column and
    #      call this function
    for fc in indices: # A) for each focus column, ...
        # find the submatrix ...
        As = A # B) make a copy, and ...
        As = As[1:] # ... C) remove the first row
        height = len(As) # D)

        for i in range(height):
            # E) for each remaining row of submatrix ...
            #     remove the focus column elements
            As[i] = As[i][0:fc] + As[i][fc+1:]

        sign = (-1) ** (fc % 2) # F)
        # G) pass submatrix recursively
        sub_det = determinant(As)
        # H) total all returns from recursion
        total += sign * A[0][fc] * sub_det

    return total

def inverse(matrix):
    det_matrix = determinant(matrix)
    if det_matrix == 0:
        print("This matrix doesn't have an inverse.")
    dim = len(matrix)
    adj_matrix = []
    for k in range(dim):
        adj_matrix.append([])
        for j in range(dim):
            minor_matrix = []
            cofactor = (-1) ** (j + k)
            a_elem = matrix[j][k]
            for i in range(dim):
                if i != j:
                    minor_matrix.append(matrix[i][0:k] + matrix[i][k+1:dim])
            det_minor = cofactor * determinant(minor_matrix)
            adj_matrix[k].append(det_minor)
    print_matrix(adj_matrix)
    multiple_constant(adj_matrix, 1 / det_matrix)

while True:
    menu()
    choice = input("Your choice: ").strip()
    if choice == "1":
        add(read_matrix(n="first"), read_matrix(n="second"))
    elif choice == "2":
        multiple_constant(read_matrix(constant=True), float(input("Enter constant: ").strip()))
    elif choice == "3":
        multiple_matrices(read_matrix(n="first"), read_matrix(n="second"))
    elif choice == "4":
        t_menu()
        choice = input("Your choice: ").strip()
        if choice == "1":
            print_matrix(transpose(read_matrix(constant=True), 1))
        elif choice == "2":
            print_matrix(transpose(read_matrix(constant=True), 2))
        elif choice == "3":
            print_matrix(transpose(read_matrix(constant=True), 3))
        elif choice == "4":
            print_matrix(transpose(read_matrix(constant=True), 4))
    elif choice == "5":
        d = determinant(read_matrix(constant=True))
        print("The result is: \n{}".format(d))
    elif choice == "6":
        inverse(read_matrix(constant=True))
    elif choice == "0":
        break
