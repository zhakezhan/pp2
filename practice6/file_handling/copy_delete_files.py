import shutil, os

shutil.copy("sample.txt", "copy.txt")
shutil.copy2("sample.txt", "backup.txt")

if os.path.exists("copy.txt"):
    os.remove("copy.txt")