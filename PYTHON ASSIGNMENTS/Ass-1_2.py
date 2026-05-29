def group_by_key(tuples_list):
    result={}
    for key, value in tuples_list:
        if key not in result:
            result[key]=[]
        result[key].append(value)
    return result
data=[("redballs",7),("blueballs",8),("yellowballs",5),("blueballs",7),("yellowballs",8)]
final_dict=group_by_key(data)
print(final_dict)

