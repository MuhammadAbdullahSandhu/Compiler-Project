
class Errors:

    def invalid_toke(current_char,line_number):
        print(f"Error: Invalid token '{current_char}' at line {line_number}")
    
    def successful(text):
        print(f"Successful!")
