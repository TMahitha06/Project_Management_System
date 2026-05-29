def get_student_info():
    students=[
        (1, "Likhith", (89,90,76)),
        (2, "Meghana", (90,78,88)),
        (3, "Sneha" , (78,67,56)),
        (4, "sindhu", (89,99,67)),
        (5, "shoheb", (89,95,90))
    ]
    return students
All_students=get_student_info()
for student_id,name,(score1,score2,score3)in All_students:
    average=(score1+score2+score3)/3
    print(f"ID :{student_id}")
    print(f"student:{name}")
    print(f"scores :{score1},{score2},{score3}")
    print(f"average:{average :.2f}")
    print("-"*40)


