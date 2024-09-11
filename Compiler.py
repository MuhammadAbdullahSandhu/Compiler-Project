from Lexer import Lexer
import argparse

## Build a Lexer from start https://www.youtube.com/watch?v=nexKgX2d7wU
## https://medium.com/@enzojade62/step-by-step-building-a-lexer-in-java-for-tokenizing-source-code-ac4f1d91326f
## https://github.com/FelipeTomazEC/Lexical-Analyzer
## https://docs.python.org/3/library/re.html

def main():
    parser = argparse.ArgumentParser(description='Process a file and print the token list.')

    # Positional argument for the file path
    parser.add_argument('file', type=str, help='file to be processed')
    
    # Flag -L to print the entire list of tokens at once
    parser.add_argument('-L', '--list', action='store_true', help='print the entire list of tokens')

    # Parse command-line arguments
    args = parser.parse_args()

    #pass arguments to function
    code_file(args.file, token_list=args.list)

# Function to read .c file and show tokens along with code
def code_file(file, token_list):
    # File opening
    try:
        with open(file, 'r') as text_file:
            # File has been read
            source_code = text_file.read()
            print("-" * 40)
            # Create tokens using a Lexer class
            tokens = Lexer(source_code)
            if token_list:
                for token in tokens:
                    print(token)
            else:
                print('Next function...')
    # Handle file if not found 
    except FileNotFoundError:
        print(f"Error: The file '{file}' was not found.")
        
    # Handle any other I/O error
    except IOError as e:
        print(f"Error: An I/O error occurred: {e}")


if __name__ == "__main__":
    main()
