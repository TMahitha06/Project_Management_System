def flatten_list(nested_list):
    return [element for sublist in nested_list for element in sublist]
list=[[1,2,3 ],[4,5,6],[7,8,9]]
flat_numbers=flatten_list(list)
print(flat_numbers)
