def sheep(arrList):
    presentsheep = []
    for i in arrList:
        if i==true:
            presentsheep.append(i)
        else:
            pass
    count = len(presentsheep)
    print(count)
true = "present"
false = "absent"
arrList=[true,  true,  true,  false,
  true,  true,  true,  true ,
  true,  false, true,  false,
  true,  false, false, true ,
  true,  true,  true,  true ,
  false, false, true,  true]
sheep(arrList)