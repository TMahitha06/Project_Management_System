def convert_to_custom_base(num, base):
    if num==0:
        return "0"
    digits="0123456789ABCDEF"
    result=""
    while num>0:
        result=digits[num%base]+result
        num//=base
    return result
print(convert_to_custom_base(255,16))
print(convert_to_custom_base(100,2))
print(convert_to_custom_base(42,8))