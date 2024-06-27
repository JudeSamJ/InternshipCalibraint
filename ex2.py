def func(score1,score2,score3):
    score = (score1+score2+score3)/3
    if 90 <= score <= 100:
        print("A")
    elif 80 <= score < 90:
        print("B")
    elif 70 <= score < 80:
        print("C")
    elif 60 <= score < 70:
        print("D")
    else:
        print("F")
score1=int(input("Enter your first subject mark:"))
score2=int(input("Enter your second subject mark:"))
score3=int(input("Enter your third subject mark:"))
func(score1, score2, score3)