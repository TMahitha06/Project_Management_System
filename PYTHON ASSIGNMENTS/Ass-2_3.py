def get_status_message(value,is_active,limit):
            return (
                    "High Alert" if (is_active and value>limit)else  
                    "Moderate" if (is_active and value<=limit)else
                    "Inactive"if (is_active and value<0)else
                    "Idle"
                    )
print("===Testing status Messages===\n")
result1=get_status_message(100,True,50)
print(f"case1: value=100,is_active=True,limit=50 {result1}")
result2 = get_status_message(30, True, 50)
print(f"Case 2: value=30, is_active=True, limit=50 {result2}")
result3 = get_status_message(-5, False, 50)
print(f"Case 3: value=-5, is_active=False, limit=50 {result3}")
result4 = get_status_message(10, False, 50)
print(f"Case 4: value=10, is_active=False, limit=50 {result4}")
result5 = get_status_message(50, True, 50)
print(f"Case 5: value=50, is_active=True, limit=50 {result5}")
result6 = get_status_message(0, False, 50)
print(f"Case 6: value=0, is_active=False, limit=50 {result6}")
