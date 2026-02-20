#1 Sort strings by length:
words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)

#2
students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

#3
numbers = [5, 2, 9, 1]

result = sorted(numbers, key=lambda x: x)

print(result)

#4
words = ["apple", "kiwi", "banana", "fig"]

result = sorted(words, key=lambda w: len(w))

print(result)

#5 Sort strings by last character
words = ["cat", "dog", "elephant", "ant"]

result = sorted(words, key=lambda w: w[-1])

print(result)