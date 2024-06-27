def findNeedle(arrlist):
    for index,i in enumerate(arrlist):
        if i=="needle":
            print(f"{arrlist} --> found the needle at position {index}")
        else:
            pass
arrlist=["hay", "junk", "hay", "hay", "moreJunk","randomJunk","needle"]
findNeedle(arrlist)