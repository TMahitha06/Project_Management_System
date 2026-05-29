def invert_dictionary(d):
    inverted={}
    for key,value in d.items():
        if value not in inverted:
            inverted[value]= []
        inverted[value].append(key)
    return inverted
d = {'a': 1, 'b': 2, 'c': 1, 'd': 3}
final_result=invert_dictionary(d)
print(final_result)