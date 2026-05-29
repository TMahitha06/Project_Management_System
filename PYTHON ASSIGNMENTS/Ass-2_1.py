def create_counter(initial_count=9):
    count=initial_count
    def counter_function():
        nonlocal count
        count +=1
        return count
    def reset_counter():
        nonlocal count
        count=initial_count
    counter_function.reset=reset_counter
    return counter_function
count=create_counter()
print (count())
print(count())

 