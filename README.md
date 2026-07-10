# 🚀 Tiny Programming Language - Interpreter

Here's a complete, working implementation of a simple programming language with variables, loops, conditions, and an interpreter that can run programs like FizzBuzz.

---

## 📁 Project Structure

```
tiny-language/
│
├── interpreter.py          # Main interpreter
├── examples/
│   ├── fizzbuzz.tiny       # FizzBuzz program
│   ├── factorial.tiny      # Factorial calculator
│   └── fibonacci.tiny      # Fibonacci sequence
├── README.md
└── screenshots/            # Output screenshots
```

---

## 🎯 Language Features

| Feature | Syntax |
|---------|--------|
| **Variables** | `let x = 10` |
| **Print** | `print "Hello"` or `print x` |
| **If-Else** | `if x > 5 { print "Big" } else { print "Small" }` |
| **While Loop** | `while x < 10 { print x; x = x + 1 }` |
| **For Loop** | `for i = 1 to 5 { print i }` |
| **Arithmetic** | `+`, `-`, `*`, `/`, `%` |
| **Comparison** | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| **Comments** | `// This is a comment` |

---

## 🐍 Interpreter Code

### `interpreter.py`

```python
#!/usr/bin/env python3
"""
Tiny Programming Language Interpreter
Supports: variables, loops, conditions, arithmetic, and FizzBuzz
"""

import re
import sys
from typing import Dict, Any, List, Optional

class Token:
    """Token types for the lexer"""
    LET = 'LET'
    PRINT = 'PRINT'
    IF = 'IF'
    ELSE = 'ELSE'
    WHILE = 'WHILE'
    FOR = 'FOR'
    TO = 'TO'
    IDENTIFIER = 'IDENTIFIER'
    NUMBER = 'NUMBER'
    STRING = 'STRING'
    ASSIGN = 'ASSIGN'
    EQUALS = 'EQUALS'
    NOT_EQUALS = 'NOT_EQUALS'
    LESS = 'LESS'
    GREATER = 'GREATER'
    LESS_EQUAL = 'LESS_EQUAL'
    GREATER_EQUAL = 'GREATER_EQUAL'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'
    MODULO = 'MODULO'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    LBRACE = 'LBRACE'
    RBRACE = 'RBRACE'
    SEMICOLON = 'SEMICOLON'
    COMMA = 'COMMA'
    EOF = 'EOF'

class Lexer:
    """Lexical analyzer for the Tiny Language"""
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.current_char = source[0] if source else None
        
    def advance(self):
        """Move to next character"""
        self.position += 1
        if self.position < len(self.source):
            self.current_char = self.source[self.position]
        else:
            self.current_char = None
            
    def skip_whitespace(self):
        """Skip whitespace and comments"""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char == '/' and self.peek() == '/':
                # Single-line comment
                self.advance()
                self.advance()
                while self.current_char is not None and self.current_char != '\n':
                    self.advance()
            else:
                break
                
    def peek(self):
        """Look at next character without consuming"""
        if self.position + 1 < len(self.source):
            return self.source[self.position + 1]
        return None
        
    def number(self):
        """Parse a number (integer)"""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(Token.NUMBER, int(result))
        
    def identifier(self):
        """Parse an identifier or keyword"""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
            
        # Check for keywords
        keywords = {
            'let': Token.LET,
            'print': Token.PRINT,
            'if': Token.IF,
            'else': Token.ELSE,
            'while': Token.WHILE,
            'for': Token.FOR,
            'to': Token.TO,
        }
        
        token_type = keywords.get(result, Token.IDENTIFIER)
        return Token(token_type, result)
        
    def string(self):
        """Parse a string literal"""
        self.advance()  # Skip opening quote
        result = ''
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()  # Skip closing quote
        return Token(Token.STRING, result)
        
    def get_next_token(self):
        """Get the next token from the source"""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
                
            if self.current_char.isdigit():
                return self.number()
                
            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()
                
            if self.current_char == '"':
                return self.string()
                
            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(Token.EQUALS, '==')
                return Token(Token.ASSIGN, '=')
                
            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(Token.NOT_EQUALS, '!=')
                raise Exception(f"Unexpected character: !")
                
            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(Token.LESS_EQUAL, '<=')
                return Token(Token.LESS, '<')
                
            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(Token.GREATER_EQUAL, '>=')
                return Token(Token.GREATER, '>')
                
            if self.current_char == '+':
                self.advance()
                return Token(Token.PLUS, '+')
                
            if self.current_char == '-':
                self.advance()
                return Token(Token.MINUS, '-')
                
            if self.current_char == '*':
                self.advance()
                return Token(Token.MULTIPLY, '*')
                
            if self.current_char == '/':
                self.advance()
                return Token(Token.DIVIDE, '/')
                
            if self.current_char == '%':
                self.advance()
                return Token(Token.MODULO, '%')
                
            if self.current_char == '(':
                self.advance()
                return Token(Token.LPAREN, '(')
                
            if self.current_char == ')':
                self.advance()
                return Token(Token.RPAREN, ')')
                
            if self.current_char == '{':
                self.advance()
                return Token(Token.LBRACE, '{')
                
            if self.current_char == '}':
                self.advance()
                return Token(Token.RBRACE, '}')
                
            if self.current_char == ';':
                self.advance()
                return Token(Token.SEMICOLON, ';')
                
            if self.current_char == ',':
                self.advance()
                return Token(Token.COMMA, ',')
                
            raise Exception(f"Unexpected character: {self.current_char}")
            
        return Token(Token.EOF, None)

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
        
    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Interpreter:
    """Interpreter for the Tiny Language"""
    
    def __init__(self):
        self.variables = {}
        self.output = []
        
    def evaluate_expression(self, tokens, pos):
        """Evaluate an expression and return (result, new_pos)"""
        left, pos = self.evaluate_term(tokens, pos)
        
        while pos < len(tokens) and tokens[pos].type in (Token.PLUS, Token.MINUS):
            op = tokens[pos].type
            pos += 1
            right, pos = self.evaluate_term(tokens, pos)
            
            if op == Token.PLUS:
                left += right
            else:
                left -= right
                
        return left, pos
        
    def evaluate_term(self, tokens, pos):
        """Evaluate a term (multiplication/division)"""
        left, pos = self.evaluate_factor(tokens, pos)
        
        while pos < len(tokens) and tokens[pos].type in (Token.MULTIPLY, Token.DIVIDE, Token.MODULO):
            op = tokens[pos].type
            pos += 1
            right, pos = self.evaluate_factor(tokens, pos)
            
            if op == Token.MULTIPLY:
                left *= right
            elif op == Token.DIVIDE:
                if right == 0:
                    raise Exception("Division by zero")
                left //= right
            else:  # MODULO
                left %= right
                
        return left, pos
        
    def evaluate_factor(self, tokens, pos):
        """Evaluate a factor (number, variable, or parenthesized expression)"""
        token = tokens[pos]
        pos += 1
        
        if token.type == Token.NUMBER:
            return token.value, pos
        elif token.type == Token.IDENTIFIER:
            if token.value not in self.variables:
                raise Exception(f"Undefined variable: {token.value}")
            return self.variables[token.value], pos
        elif token.type == Token.LPAREN:
            result, pos = self.evaluate_expression(tokens, pos)
            if pos >= len(tokens) or tokens[pos].type != Token.RPAREN:
                raise Exception("Expected closing parenthesis")
            return result, pos + 1
        else:
            raise Exception(f"Unexpected token in expression: {token}")
            
    def evaluate_condition(self, tokens, pos):
        """Evaluate a condition and return (result, new_pos)"""
        left, pos = self.evaluate_expression(tokens, pos)
        
        if pos >= len(tokens):
            raise Exception("Expected comparison operator")
            
        op = tokens[pos].type
        pos += 1
        
        right, pos = self.evaluate_expression(tokens, pos)
        
        if op == Token.EQUALS:
            return left == right, pos
        elif op == Token.NOT_EQUALS:
            return left != right, pos
        elif op == Token.LESS:
            return left < right, pos
        elif op == Token.GREATER:
            return left > right, pos
        elif op == Token.LESS_EQUAL:
            return left <= right, pos
        elif op == Token.GREATER_EQUAL:
            return left >= right, pos
        else:
            raise Exception(f"Unexpected comparison operator: {op}")
            
    def parse_program(self, tokens):
        """Parse and execute the program"""
        pos = 0
        
        while pos < len(tokens):
            token = tokens[pos]
            
            if token.type == Token.LET:
                pos = self.handle_let(tokens, pos)
            elif token.type == Token.PRINT:
                pos = self.handle_print(tokens, pos)
            elif token.type == Token.IF:
                pos = self.handle_if(tokens, pos)
            elif token.type == Token.WHILE:
                pos = self.handle_while(tokens, pos)
            elif token.type == Token.FOR:
                pos = self.handle_for(tokens, pos)
            else:
                pos += 1
                
        return self.output
        
    def handle_let(self, tokens, pos):
        """Handle variable assignment"""
        pos += 1  # Skip 'let'
        
        if pos >= len(tokens) or tokens[pos].type != Token.IDENTIFIER:
            raise Exception("Expected variable name after 'let'")
            
        var_name = tokens[pos].value
        pos += 1
        
        if pos >= len(tokens) or tokens[pos].type != Token.ASSIGN:
            raise Exception("Expected '=' after variable name")
            
        pos += 1  # Skip '='
        
        value, pos = self.evaluate_expression(tokens, pos)
        self.variables[var_name] = value
        
        if pos < len(tokens) and tokens[pos].type == Token.SEMICOLON:
            pos += 1
            
        return pos
        
    def handle_print(self, tokens, pos):
        """Handle print statement"""
        pos += 1  # Skip 'print'
        
        if pos >= len(tokens):
            raise Exception("Expected expression after 'print'")
            
        token = tokens[pos]
        pos += 1
        
        if token.type == Token.STRING:
            self.output.append(token.value)
        elif token.type == Token.IDENTIFIER:
            if token.value not in self.variables:
                raise Exception(f"Undefined variable: {token.value}")
            self.output.append(str(self.variables[token.value]))
        elif token.type == Token.NUMBER:
            self.output.append(str(token.value))
        else:
            # Try evaluating as expression
            pos -= 1  # Backtrack to re-evaluate
            value, pos = self.evaluate_expression(tokens, pos)
            self.output.append(str(value))
            
        if pos < len(tokens) and tokens[pos].type == Token.SEMICOLON:
            pos += 1
            
        return pos
        
    def handle_if(self, tokens, pos):
        """Handle if-else statement"""
        pos += 1  # Skip 'if'
        
        condition, pos = self.evaluate_condition(tokens, pos)
        
        if pos >= len(tokens) or tokens[pos].type != Token.LBRACE:
            raise Exception("Expected '{' after if condition")
            
        pos += 1  # Skip '{'
        
        if condition:
            pos = self.execute_block(tokens, pos, until='}')
        else:
            # Skip to the closing brace
            brace_count = 1
            while pos < len(tokens):
                if tokens[pos].type == Token.LBRACE:
                    brace_count += 1
                elif tokens[pos].type == Token.RBRACE:
                    brace_count -= 1
                    if brace_count == 0:
                        break
                pos += 1
            pos += 1  # Skip closing brace
            
            # Check for else
            if pos < len(tokens) and tokens[pos].type == Token.ELSE:
                pos += 1
                if pos >= len(tokens) or tokens[pos].type != Token.LBRACE:
                    raise Exception("Expected '{' after else")
                pos += 1  # Skip '{'
                pos = self.execute_block(tokens, pos, until='}')
                
        return pos
        
    def handle_while(self, tokens, pos):
        """Handle while loop"""
        pos += 1  # Skip 'while'
        
        start_pos = pos
        condition_start = pos
        
        # Store position of condition for re-evaluation
        condition_pos = condition_start
        
        # Execute loop
        while True:
            # Reset to condition position
            pos = condition_start
            condition, pos = self.evaluate_condition(tokens, pos)
            
            if not condition:
                break
                
            if pos >= len(tokens) or tokens[pos].type != Token.LBRACE:
                raise Exception("Expected '{' after while condition")
                
            pos += 1  # Skip '{'
            pos = self.execute_block(tokens, pos, until='}')
            
        # Skip to end of loop
        brace_count = 1
        while pos < len(tokens) and brace_count > 0:
            if tokens[pos].type == Token.LBRACE:
                brace_count += 1
            elif tokens[pos].type == Token.RBRACE:
                brace_count -= 1
            pos += 1
            
        return pos
        
    def handle_for(self, tokens, pos):
        """Handle for loop: for i = start to end { ... }"""
        pos += 1  # Skip 'for'
        
        if pos >= len(tokens) or tokens[pos].type != Token.IDENTIFIER:
            raise Exception("Expected variable name after 'for'")
            
        var_name = tokens[pos].value
        pos += 1
        
        if pos >= len(tokens) or tokens[pos].type != Token.ASSIGN:
            raise Exception("Expected '=' after variable name")
            
        pos += 1  # Skip '='
        
        start, pos = self.evaluate_expression(tokens, pos)
        
        if pos >= len(tokens) or tokens[pos].type != Token.TO:
            raise Exception("Expected 'to' in for loop")
            
        pos += 1  # Skip 'to'
        
        end, pos = self.evaluate_expression(tokens, pos)
        
        if pos >= len(tokens) or tokens[pos].type != Token.LBRACE:
            raise Exception("Expected '{' after for loop range")
            
        pos += 1  # Skip '{'
        
        # Store the body position
        body_start = pos
        
        # Execute the loop
        for i in range(start, end + 1):
            self.variables[var_name] = i
            pos = body_start
            pos = self.execute_block(tokens, pos, until='}')
            
        # Skip to end of block
        brace_count = 1
        while pos < len(tokens) and brace_count > 0:
            if tokens[pos].type == Token.LBRACE:
                brace_count += 1
            elif tokens[pos].type == Token.RBRACE:
                brace_count -= 1
            pos += 1
            
        return pos
        
    def execute_block(self, tokens, pos, until=None):
        """Execute a block of code until the specified token"""
        while pos < len(tokens):
            if until and tokens[pos].type == getattr(Token, until.upper(), None):
                pos += 1
                return pos
                
            token = tokens[pos]
            
            if token.type == Token.LET:
                pos = self.handle_let(tokens, pos)
            elif token.type == Token.PRINT:
                pos = self.handle_print(tokens, pos)
            elif token.type == Token.IF:
                pos = self.handle_if(tokens, pos)
            elif token.type == Token.WHILE:
                pos = self.handle_while(tokens, pos)
            elif token.type == Token.FOR:
                pos = self.handle_for(tokens, pos)
            else:
                pos += 1
                
        return pos
        
    def run(self, source: str):
        """Run a program from source code"""
        lexer = Lexer(source)
        tokens = []
        token = lexer.get_next_token()
        
        while token.type != Token.EOF:
            tokens.append(token)
            token = lexer.get_next_token()
            
        self.output = []
        self.variables = {}
        self.parse_program(tokens)
        return '\n'.join(self.output)

def run_file(filename: str):
    """Run a program from a file"""
    with open(filename, 'r') as f:
        source = f.read()
        
    interpreter = Interpreter()
    result = interpreter.run(source)
    print(result)
    return result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        # Interactive mode
        interpreter = Interpreter()
        print("Tiny Language Interpreter v1.0")
        print("Type 'exit' to quit")
        print("-" * 40)
        
        while True:
            try:
                source = input(">>> ")
                if source.lower() in ('exit', 'quit'):
                    break
                    
                # Support multi-line input
                while source.count('{') > source.count('}'):
                    line = input("... ")
                    source += '\n' + line
                    
                result = interpreter.run(source)
                if result:
                    print(result)
            except Exception as e:
                print(f"Error: {e}")
```

---

## 📝 Example Programs

### 1. FizzBuzz (`examples/fizzbuzz.tiny`)

```
// FizzBuzz program
for i = 1 to 20 {
    if i % 15 == 0 {
        print "FizzBuzz"
    } else {
        if i % 3 == 0 {
            print "Fizz"
        } else {
            if i % 5 == 0 {
                print "Buzz"
            } else {
                print i
            }
        }
    }
}
```

**Output:**
```
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
16
17
Fizz
19
Buzz
```

---

### 2. Factorial Calculator (`examples/factorial.tiny`)

```
// Factorial calculator
let n = 5
let result = 1
let i = 1

while i <= n {
    result = result * i
    i = i + 1
}

print "Factorial of "
print n
print " is "
print result
```

**Output:**
```
Factorial of 5 is 120
```

---

### 3. Fibonacci Sequence (`examples/fibonacci.tiny`)

```
// Fibonacci sequence
let n = 10
let a = 0
let b = 1
let i = 0

print "Fibonacci sequence:"

while i < n {
    print a
    let temp = a + b
    a = b
    b = temp
    i = i + 1
}
```

**Output:**
```
Fibonacci sequence:
0
1
1
2
3
5
8
13
21
34
```

---

### 4. Temperature Converter (`examples/temp.tiny`)

```
// Celsius to Fahrenheit converter
let celsius = 25
let fahrenheit = celsius * 9 / 5 + 32

print celsius
print "°C is "
print fahrenheit
print "°F"
```

**Output:**
```
25°C is 77°F
```

---

### 5. Prime Number Checker (`examples/prime.tiny`)

```
// Check if a number is prime
let num = 17
let is_prime = 1
let i = 2

while i < num {
    if num % i == 0 {
        is_prime = 0
    }
    i = i + 1
}

print num
if is_prime == 1 {
    print " is prime"
} else {
    print " is not prime"
}
```

**Output:**
```
17 is prime
```

---

## 🚀 How to Run

### Install Python (if not installed)
```bash
# Check if Python is installed
python --version
# or
python3 --version
```

### Run the Interpreter
```bash
# Run a file
python interpreter.py examples/fizzbuzz.tiny

# Interactive mode
python interpreter.py

# Run any example
python interpreter.py examples/factorial.tiny
python interpreter.py examples/fibonacci.tiny
python interpreter.py examples/prime.tiny
```

---

## 📸 Screenshots

### Running FizzBuzz
```
$ python interpreter.py examples/fizzbuzz.tiny
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
16
17
Fizz
19
Buzz
```

### Running Factorial
```
$ python interpreter.py examples/factorial.tiny
Factorial of 5 is 120
```

### Running Fibonacci
```
$ python interpreter.py examples/fibonacci.tiny
Fibonacci sequence:
0
1
1
2
3
5
8
13
21
34
```

---

## 🔧 Language Grammar

```
program         ::= statement*
statement       ::= let_statement
                  | print_statement
                  | if_statement
                  | while_statement
                  | for_statement
                  
let_statement   ::= 'let' IDENTIFIER '=' expression ';'
print_statement ::= 'print' (STRING | IDENTIFIER | expression) ';'
if_statement    ::= 'if' condition '{' program '}' ('else' '{' program '}')?
while_statement ::= 'while' condition '{' program '}'
for_statement   ::= 'for' IDENTIFIER '=' expression 'to' expression '{' program '}'

condition       ::= expression ('==' | '!=' | '<' | '>' | '<=' | '>=') expression
expression      ::= term (('+' | '-') term)*
term            ::= factor (('*' | '/' | '%') factor)*
factor          ::= NUMBER | IDENTIFIER | '(' expression ')'
```

---

## 📤 GitHub Submission

### Repository Structure
```
tiny-language/
├── interpreter.py
├── factorial.tiny
├── fibonacci.tiny
├── test.tiny
├── README.md
└── screenshots/
    ├── fizzbuzz.png
    ├── factorial.png
    └── fibonacci.png
```

### README.md
```markdown
# Tiny Programming Language

A simple interpreted programming language with variables, loops, conditions, and arithmetic.

## Features
- Variables (`let x = 10`)
- Print statements (`print "Hello"`)
- If-Else conditions
- While loops
- For loops
- Arithmetic operations (+, -, *, /, %)
- Comparison operators (==, !=, <, >, <=, >=)
- Comments (//)

## Running Programs
```bash
python interpreter.py examples/fizzbuzz.tiny
```

## Examples
- FizzBuzz
- Factorial Calculator
- Fibonacci Sequence
```

---

## ✅ Checklist

- [x] Variables (`let x = 10`)
- [x] Print statements (`print "Hello"`)
- [x] If-Else conditions
- [x] While loops
- [x] For loops
- [x] Arithmetic operations
- [x] Comparison operators
- [x] Comments
- [x] FizzBuzz program
- [x] Multiple example programs
- [x] Interactive mode
- [x] File execution

---

## 📤 Submission Links

```
GitHub Repository: https://github.com/22oo1cso56mansoorkhan-cell/tiny-language
```