def process_matrix(matrix):
    total=0
    for row in matrix:
        for num in row:
            if num>10:
                break
            if num%2==0:
                continue
            total+=num
    return total
matrix1=[[1,2,3],
        [4,5,6],
        [7,8,9]]
print(f"matrix 1 Total:{process_matrix(matrix1)}")