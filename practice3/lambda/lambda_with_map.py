#1
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)

#2
numbers = [1, 2, 3, 4]

result = list(map(lambda x: x ** 2, numbers))

print(result)

#3
words = ["cat", "dog", "tiger"]

result = list(map(lambda w: w.upper(), words))

print(result)

#4
words = ["apple", "banana", "kiwi"]

result = list(map(lambda w: len(w), words))

print(result)

#5
numbers = [5, 7, 9]

result = list(map(lambda x: x + 10, numbers))

print(result)