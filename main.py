from Lexer3 import Lexer
import argparse

## https://docs.python.org/3/library/re.html#re.RegexFlag

# read .c file and show tokens
def code_file(file_path, show_tokens):
    # Read the contents of the .c file
    with open(file_path, 'r') as file:
        code = file.read()

    # Print the original code
    print(f"Processing file'{file_path}':\n")
    lexer = Lexer(code)

    if show_tokens:
        # show the regular code tokens
        print("\n Regular Tokens:")
        regular_tokens = lexer.tokenize()
        for tokens in regular_tokens:
            print(tokens)

        # show the preprocessor tokens
        print("\n Preprocessor Tokens:")
        preprocessor_tokens = lexer.tokenize_preprocessors()
        for p_pro_tokens in preprocessor_tokens:
            print(p_pro_tokens)

# Main function to handle command-line arguments
def main():
    # Set up argparse to handle the -L flag and file input
    parser = argparse.ArgumentParser(description="Process a file and print the token list.")
    parser.add_argument("file", help="file to be processed")
    parser.add_argument("-L", "--list", action="store_true", help="print the entire list of tokens)")
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Process the file and pass in the list flag
    code_file(args.file, show_tokens=args.list)


if __name__ == '__main__':
    main()
