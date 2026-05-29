def  is_palindrome_slicing(data):
    return data==data[::-1]
print(is_palindrome_slicing(["madam"]))
print(is_palindrome_slicing([1,2,1]))