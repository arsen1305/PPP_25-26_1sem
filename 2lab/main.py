

if __name__ == "__main__":

def check_brackets(s):
    
    stack = [] 
    bracket_map = {')': '(', ']': '[', '}': '{'} 

    for i, char in enumerate(s):
        if char in bracket_map.values(): 
            stack.append((char, i)) 
        elif char in bracket_map: 
            if not stack: 
                return i + 1 
            top, top_index = stack.pop()
            if bracket_map[char] != top: 
                return i + 1 
    if stack: 
        top, top_index = stack.pop()
        return top_index + 1 
    return "ok" 


input_string = input("Введите строку со скобками: ")
result = check_brackets(input_string)
print(result) 
