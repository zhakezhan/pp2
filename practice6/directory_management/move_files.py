import shutil, os

os.makedirs("dest", exist_ok=True)

if os.path.exists("sample.txt"):
    shutil.move("sample.txt", "dest/sample.txt")

if os.path.exists("dest/sample.txt"):
    shutil.copy("dest/sample.txt", "copy.txt")