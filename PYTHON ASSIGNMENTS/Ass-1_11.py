def process_names(names):
    return list(filter(lambda name:len(name)>=4,map(str.capitalize,names)))
print(process_names(["ada","grace","charles","tim","alan"]))