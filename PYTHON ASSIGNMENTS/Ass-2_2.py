def dynamic_calculator(operation,*numbers,**options):
    if operation in ['add','subtract']:
       default_initial=0
    else:
        default_initial=1
    initial=options.get('initial_value',default_initial)
    round_result=options.get('round_result',False)
    safe_division=options.get('safe_division',True)
    if not numbers:
        return initial
    result=initial
    if operation=="add":
        result=sum(numbers)+initial
    elif operation=='subtract':
        for num in numbers:
            result-=num
    elif operation=='multiply':
        for num in numbers:
            result*=num
    elif operation=='divide':
        for num in numbers:
            if safe_division and num==0:
                return "Error:Division by zero"
            result/=num
    else:
        return f"Error:Unknown operation'{operation}'"
    return round(result,2) if round_result else result
print("=== Testing dynamic_calcualtor===\n")
result1=dynamic_calculator("add",1,2,3)
print(f"add 1+2+3= {result1}")
result2=dynamic_calculator("subtract",2,3,6,9,initial_value=4)
print(f"subtract 4-2-3-6-9= {result2}")
result3=dynamic_calculator("multiply",3,4,5,6,initial_value=8)
print(f"multiply 8*3*4*5*6= {result3}")
result4=dynamic_calculator("divide",6,7,initial_value=5,round_result=True)
print(f"divide 5/6/7= {result4}")
result5=dynamic_calculator('add')
print(f"add with no numbers={result5}")