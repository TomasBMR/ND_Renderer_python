    print("[", end="")
    for face in facesDims:
        print("[", end="")
        for i in face:
            print(i, ",")
        print("],")
    print("]")