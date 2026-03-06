#1
import re
pattern = r"ab*"
text = input()
if re.fullmatch(pattern, text):
    print("match found")
else:
    print("no match")

#2
import re
pattern = r"ab{2,3}"
text = input()
if re.fullmatch(pattern, text):
    print("match found")
else:
    print("no match")

#3
import re
pattern = r"[a-z]+_[a-z]+"
text = input()
if re.fullmatch(pattern, text):
    print("match found")
else:
    print("no match")

#4
import re
pattern = r"[A-Z][a-z]+"
text = input()
if re.fullmatch(pattern, text):
    print("match found")
else:
    print("no match")

#5
import re
pattern = r"a.*b"
text = input()
if re.fullmatch(pattern, text):
    print("match found")
else:
    print("no match")

#6
import re
text = input("Enter a string: ")
result = re.sub(r"[ ,\.]", ":", text)
print(result)

#7
snake_str = input()
words = snake_str.split('_') 
camel_str = words[0] + ''.join(word.capitalize() for word in words[1:])
print(camel_str)

#8
import re
s = input()
up_s = s.split(re.fullmatch(r"[A-Z][a-z]*", s))
print(up_s)

#9
import re
text = input()
result = re.sub(r'(?<!^)(?=[A-Z])', ' ', text)
print(result)

#10
import re
camel = input()
snake = re.sub(r'(?<!^)(?=[A-Z])', '_', camel).lower()
print(snake)