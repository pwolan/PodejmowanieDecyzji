def geometric_mean(vector: list[int|float]):
    if len(vector) == 0:
        return -1
    product = 1

    for num in vector:
        product *= num

    geometric_mean = product**(1/len(vector))
    return geometric_mean

def geometric_mean_matrix(matrix: list[list[int|float]]):
    if len(matrix) == 0 or len(matrix[0]) == 0:
        return -1
    product = [1 for _ in range(len(matrix))]
    
    for i in range(len(matrix)):
        product[i] = geometric_mean(matrix[i])

    #geometric_mean_matrix = [product[i]**(1/len(matrix[i])) for i in range(len(matrix))]
    return product

def geometric_mean_N_vectors(vectors: list[list[int|float]]):
    if len(vectors) == 0 or len(vectors[0]) == 0:
        return -1
    product = [1 for _ in range(len(vectors[0]))]

    for i in range(len(vectors[0])):
        for j in range(len(vectors)):
            product[i] *= vectors[j][i]

    result = [product[i]**(1/len(vectors)) for i in range(len(vectors[0]))]
    return result

#TESTY
# print(geometric_mean([]))
# print(geometric_mean([1]))
# print(geometric_mean([1,2]))
# print(geometric_mean([0.1,0.1,3,4,5]))

# print(geometric_mean_matrix([[1,2,4,5,2],
#                              [2,1,2,3,2],
#                              [4,2,1,5,5],
#                              [5,3,5,1,4],
#                              [2,2,5,4,1]]))

# print(geometric_mean_N_vectors([[1,2,4,5,2],
#                                 [2,1,2,3,2],
#                                 [4,2,1,5,5],
#                                 [5,3,5,1,4],
#                                 [2,2,5,4,1]]))