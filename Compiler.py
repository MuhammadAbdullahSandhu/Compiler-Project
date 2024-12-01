from Lexer import Lexer
import argparse
import MyParser 
from errors import Errors
import optimize_tac2


## Build a Lexer from start https://www.youtube.com/watch?v=nexKgX2d7wU
## https://medium.com/@enzojade62/step-by-step-building-a-lexer-in-java-for-tokenizing-source-code-ac4f1d91326f
## https://github.com/FelipeTomazEC/Lexical-Analyzer
## https://docs.python.org/3/library/re.html

def main():
    parser = argparse.ArgumentParser(description='Process a file and print the token list or parsed components.')

    # Positional argument for the file path
    parser.add_argument('file', type=str, help='file to be processed')
    
    # Flag -L to print the entire list of tokens at once
    parser.add_argument('-L', '--list', action='store_true', help='print the entire list of tokens')

    # Flag -A to parse the code using the parser
    parser.add_argument('-A', '--parsing', action='store_true', help='parse the code using the parser')
    
    # Flag -AST toprint Abstract Symbol Table
    parser.add_argument('-AST', '--ast', action='store_true', help='print the AST of the program')

    # Flag -ST to to print Symbol Table
    parser.add_argument('-ST', '--st' ,action='store_true', help='print the Symbol Table')

    # Flag -TAC to print three address code
    parser.add_argument('-TAC', '--tac', action='store_true', help='print the 3-address code (TAC)')

    # Flag -O to print optimize three address 
    parser.add_argument('-O', '--optac', action='store_true', help='print the optimized 3-address code (TAC)')

    # Parse command-line arguments
    args = parser.parse_args()

    #pass arguments to function
    code_file(args.file, 
              token_list=args.list, 
              parse_token=args.parsing, 
              parsing = args.parsing, 
              ast = args.ast,
              symboltable = args.st,
              tac = args.tac,
              optac = args.optac
              )

# Function to read .c file and show tokens along with code
def code_file(file, token_list, parse_token, parsing, ast, symboltable, tac, optac):
    # File opening
    try:
        with open(file, 'r') as text_file:
            # File has been read
            source_code = text_file.read()
            print("-" * 40)
            # Create tokens using a Lexer class
            tokens = Lexer(source_code)
            myparser = MyParser.Parser(tokens)
            global_declarations, functions ,program, symbol_table, tac_code = myparser.parse()
            if token_list:
                for token in tokens:
                    print(token)
            elif parse_token:
                try:
                    myparser.parse()
                    print("Parsing completed successfully.")
                except SyntaxError as e:
                    print(f"Syntax error: {e}")
            elif parsing:
                try:
                    myparser.parse()
                    print("Parsing completed successfully.")
                except SyntaxError as e:
                    print(f"Syntax error: {e}")  

            #print AST        
            elif ast:
                try:
                    print(f"AST \n")
                    AST = program.to_string()
                    print(AST)
                except SyntaxError as e:
                    print(f"Syntax error: {e}")  

            # print symbol table
            elif symboltable:
                try:
                    print(f"Symbol Table \n")
                    print(symbol_table) 
                except SyntaxError as e:
                    print(f"Syntax error: {e}")  

            # print three address code
            elif tac:
                try:
                    tac_code.generate(program)
                    tac_code.print_code()
                except SyntaxError as e:
                    print(f"Syntax error: {e}")  
            elif optac:
                try:
                    tac_code.generate(program)
                    optimizer = optimize_tac2.Optimizer(tac_code.code)
                    optimizer.optimize()
                    optimizer.print_optimized_code()
                except SyntaxError as e:
                    print(f"Syntax error: {e}") 

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
