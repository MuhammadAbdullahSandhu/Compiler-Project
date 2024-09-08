from Lexer2 import Lexer
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python lexer_script.py <source_file.c>")
        sys.exit(1)
    file_path = sys.argv[1]
    try:
        with open(file_path, 'r') as file:
            source_code = file.read()
            print("**" * 20)
            tokens = Lexer(source_code)
            for token in tokens:
                print(token)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
