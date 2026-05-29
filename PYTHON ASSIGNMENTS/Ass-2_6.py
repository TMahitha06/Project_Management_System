def custom_enumerate_filter(iterable, start=0, step=1, predicate=None):
    current=start
    for item in iterable:
        if predicate is None or predicate(item):
            yield(current,item)
        current+=step
numbers=[1,2,3,4,5]
for index, val in custom_enumerate_filter(numbers, start=10, step=2, predicate=lambda x:x%2==0):
   print(index,val)