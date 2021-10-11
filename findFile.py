import os
file = os.listdir("./")
file_sorted = sorted(file)

for file in file_sorted:
        if file.endswith(".mkv"):
            my_file = os.path.abspath(file)
        
print(my_file)
    
