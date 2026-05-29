def  find_common_elements(list1, list2):
    return list(set([element for element in list1 if element in list2]))
def find_common_elements(list1, list2):
    return list(set([x for x in list1 if x in list2]))
list1=[1,2,3,4,5,6,7,3,4,2,3,4]
list2=[2,4,5,6,7,7,8,3,5,6,1,1,7]
result=find_common_elements(list1, list2)
print(result)