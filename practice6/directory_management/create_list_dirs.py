import os

os.mkdir("test")
os.makedirs("a/b", exist_ok=True)

print(os.listdir())
print(os.getcwd())

for f in os.listdir():
    if f.endswith(".txt"):
        print(f)

if os.path.exists("test"):
    os.rmdir("test")