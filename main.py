i=2
ij =1
while i<1000:
    i=i+1
    with open(f"folder/maj{i}.txt", "w") as file:
        while ij< 100000000:
            file.write("11111111111111111 \n")
            ij= ij + 1
    ij=1


