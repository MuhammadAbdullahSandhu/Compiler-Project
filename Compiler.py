from Lexer import lexer

def main():
    print("Lexical Analyzer")
    input_string = input("Enter Code: ")
    tokens = lexer(input_string)
    for token in tokens:
        print(token)

if __name__ == "__main__":
    main()
