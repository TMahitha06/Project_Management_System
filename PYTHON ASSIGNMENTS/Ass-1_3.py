def merge_and_sum(dict1,dict2):
   result={}
   for key in dict1:
      result[key]=dict1[key]
   for key in dict2:
      if key in dict1:
         result[key]=dict1[key]+dict2[key]
      else:
         result[key]=dict2[key]
   return result
dict1 = {'a': 10, 'b': 20, 'c': 30}
dict2 = {'b': 5, 'c': 15, 'd': 40}
merged_dict=merge_and_sum(dict1,dict2)
print(merged_dict)

