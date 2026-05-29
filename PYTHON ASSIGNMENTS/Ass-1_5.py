def create_or_update_item(items_dict, key, value=None):
    if value is None:
        if key in items_dict:
          del items_dict[key]
    else:
       items_dict[key]=value
    return items_dict
My_dict={'a':1,'b':2,'c':3}
create_or_update_item(My_dict,'b',10)
create_or_update_item(My_dict,'d',4)
print("After updates:",My_dict)
create_or_update_item(My_dict,'c',None)
print("After delete:",My_dict)
create_or_update_item(My_dict,'x',None)
print("After deleting no-existent:",My_dict)

