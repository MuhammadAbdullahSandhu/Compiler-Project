from Lexer2 import Lexer
import argparse

def main():
    parser = argparse.ArgumentParser(description='Process a file print the token list.')
    # Positional argument for the file path
    parser.add_argument('file', type=str, help='file to be processed')
    # Optional flag -L to print the entire list of tokens at once
    parser.add_argument('-L', '--list', action='store_true', help='print the entire list of tokens at once')
    parser.add_argument('-C', '--parser', action='store_true', help='print the string')
    
    args = parser.parse_args()
    file = args.file
    token_list = args.list 
    parser_list = args.parser 
    try:
        with open(file, 'r') as t_f:
            source_code = t_f.read()
            print("-" * 40)
            tokens = Lexer(source_code)
            if token_list:
                for token in tokens:
                    print(token) 
            elif parser_list:
                    print('Parser') 
            else:
                print('next fuction.....')
                    
    except FileNotFoundError:
        print(f"Error: the file '{file}' was not found")
    except IOError as e:
        print(f"Error: An I/O error occurred: {e}")
        
if __name__ == "__main__":
    main()
