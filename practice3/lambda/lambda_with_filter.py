#1
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)

#2
numbers = [5, 12, 7, 20, 3]
result = list(filter(lambda x: x > 10, numbers))
print(result)

#3
numbers = [-3, 5, -1, 7, -8]
result = list(filter(lambda x: x < 0, numbers))
print(result)

#4
words = ["cat", "elephant", "dog", "tiger"]
result = list(filter(lambda w: len(w) > 4, words))
print(result)

#5
numbers = [1, 2, 3, 4, 5, 6]
result = list(filter(lambda x: x % 2 == 0, numbers))
print(result)