def check_mixed_input(data1, data2, data3):
    if data1:
     if not data2:
        if data3:
           return "stage 1A: data1 true,data2 false,data3 true"
        return "stage 1B: data1 true,data2 false,data3 false"
     return "stage 1C: data1 true,data2 true"
    else:
       if not data3:
          if data2:
             return "stage 2A: data1 false,data3 false,data2 true"
          return "stage 2B: data1 false,data3 false,data2 false"
       return "stage 2C: data1 false,data3 true"

print(check_mixed_input("hello", [], True))     
print(check_mixed_input([1], None, False))     
print(check_mixed_input(1, "world", []))        
print(check_mixed_input(0, "active", 1))    
print(check_mixed_input(None, "", 0))           
print(check_mixed_input(False, [1, 2], None))   

