with open("sample.txt", "w") as f:
    f.write("Hello\nPython\n")

# append
with open("sample.txt", "a") as f:
    f.write("New line\n")

# x mode
try:
    open("new.txt", "x")
except:
    print("File exists")