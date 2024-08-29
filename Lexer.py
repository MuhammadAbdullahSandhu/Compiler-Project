string = "Muhammad Abdullah"

text = input("Enter Alphabet")
index = string.find(text)
if index != -1:
    print("The character 'A' is at: ", index)
else:
    print('Not present')