#!/usr/bin/env python3
"""
Tiny Language Interpreter - PROPER IF-ELSE FIXED
"""

import sys
import os

class Interpreter:
    def __init__(self):
        self.vars = {}
        self.output = []
        
    def run(self, code):
        """Run the program from code string"""
        lines = code.split('\n')
        self.vars = {}
        self.output = []
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('//'):
                i += 1
                continue
            
            # Handle let statement
            if line.startswith('let '):
                line = line[4:]
                parts = line.split('=')
                var_name = parts[0].strip()
                expr = parts[1].strip().rstrip(';')
                value = self.eval_expr(expr)
                self.vars[var_name] = value
                i += 1
                
            # Handle variable assignment without 'let'
            elif '=' in line and not any(line.startswith(x) for x in ['while', 'for', 'if', 'print']):
                parts = line.split('=')
                var_name = parts[0].strip()
                expr = parts[1].strip().rstrip(';')
                value = self.eval_expr(expr)
                self.vars[var_name] = value
                i += 1
                
            # Handle print statement
            elif line.startswith('print '):
                expr = line[6:].strip().rstrip(';')
                if expr.startswith('"') and expr.endswith('"'):
                    self.output.append(expr[1:-1])
                else:
                    value = self.eval_expr(expr)
                    self.output.append(str(value))
                i += 1
                
            # Handle if statement - FIXED
            elif line.startswith('if '):
                # Extract condition
                condition = line[3:].strip()
                has_same_line_brace = condition.endswith('{')
                if has_same_line_brace:
                    condition = condition[:-1].strip()
                
                # Find the if body
                body_lines = []
                j = i + 1
                brace_count = 1 if has_same_line_brace else 0
                
                while j < len(lines):
                    body_line = lines[j].strip()
                    if '{' in body_line:
                        brace_count += body_line.count('{')
                    if '}' in body_line:
                        brace_count -= body_line.count('}')
                        if brace_count == 0:
                            break
                    if body_line and (brace_count > 0 or has_same_line_brace):
                        clean_line = body_line.replace('{', '').replace('}', '').strip()
                        if clean_line:
                            body_lines.append(clean_line)
                    j += 1
                
                # Evaluate condition
                condition_result = self.eval_condition(condition)
                
                # Execute if body if condition is true
                if condition_result:
                    for body_line in body_lines:
                        self.execute_line(body_line)
                
                # Check for else
                k = j + 1
                if k < len(lines) and lines[k].strip().startswith('else'):
                    # Find else body
                    else_lines = []
                    j = k + 1
                    brace_count = 0
                    
                    while j < len(lines):
                        body_line = lines[j].strip()
                        if '{' in body_line:
                            brace_count += body_line.count('{')
                        if '}' in body_line:
                            brace_count -= body_line.count('}')
                            if brace_count == 0:
                                break
                        if body_line and (brace_count > 0 or has_same_line_brace):
                            clean_line = body_line.replace('{', '').replace('}', '').strip()
                            if clean_line:
                                else_lines.append(clean_line)
                        j += 1
                    
                    # Execute else body if condition is false
                    if not condition_result:
                        for body_line in else_lines:
                            self.execute_line(body_line)
                    
                    i = j + 1
                else:
                    i = j + 1
                
            # Handle while loop
            elif line.startswith('while '):
                condition = line[6:].strip()
                has_same_line_brace = condition.endswith('{')
                if has_same_line_brace:
                    condition = condition[:-1].strip()
                
                # Find the body
                body_lines = []
                j = i + 1
                brace_count = 1 if has_same_line_brace else 0
                
                while j < len(lines):
                    body_line = lines[j].strip()
                    if '{' in body_line:
                        brace_count += body_line.count('{')
                    if '}' in body_line:
                        brace_count -= body_line.count('}')
                        if brace_count == 0:
                            break
                    if body_line and (brace_count > 0 or has_same_line_brace):
                        clean_line = body_line.replace('{', '').replace('}', '').strip()
                        if clean_line:
                            body_lines.append(clean_line)
                    j += 1
                
                # Execute the loop
                while True:
                    if not self.eval_condition(condition):
                        break
                    for body_line in body_lines:
                        self.execute_line(body_line)
                
                i = j + 1
                
            # Handle for loop
            elif line.startswith('for '):
                parts = line[4:].split()
                var_name = parts[0]
                start_val = int(parts[2])
                end_val = int(parts[4])
                
                # Find the body
                body_lines = []
                j = i + 1
                brace_count = 0
                
                while j < len(lines):
                    body_line = lines[j].strip()
                    if '{' in body_line:
                        brace_count += body_line.count('{')
                    if '}' in body_line:
                        brace_count -= body_line.count('}')
                        if brace_count == 0:
                            break
                    if body_line and brace_count >= 0:
                        clean_line = body_line.replace('{', '').replace('}', '').strip()
                        if clean_line:
                            body_lines.append(clean_line)
                    j += 1
                
                # Execute the loop
                for val in range(start_val, end_val + 1):
                    self.vars[var_name] = val
                    for body_line in body_lines:
                        self.execute_line(body_line)
                
                i = j + 1
                
            else:
                i += 1
                
        return '\n'.join(self.output)
    
    def execute_line(self, line):
        """Execute a single line of code"""
        line = line.strip()
        if not line:
            return
            
        if line.startswith('let '):
            line = line[4:]
            parts = line.split('=')
            var_name = parts[0].strip()
            expr = parts[1].strip().rstrip(';')
            value = self.eval_expr(expr)
            self.vars[var_name] = value
            
        elif '=' in line and not any(line.startswith(x) for x in ['while', 'for', 'if', 'print']):
            parts = line.split('=')
            var_name = parts[0].strip()
            expr = parts[1].strip().rstrip(';')
            value = self.eval_expr(expr)
            self.vars[var_name] = value
            
        elif line.startswith('print '):
            expr = line[6:].strip().rstrip(';')
            if expr.startswith('"') and expr.endswith('"'):
                self.output.append(expr[1:-1])
            else:
                value = self.eval_expr(expr)
                self.output.append(str(value))
    
    def eval_expr(self, expr):
        """Evaluate a simple expression"""
        expr = expr.strip()
        
        # Handle parentheses
        while '(' in expr:
            start = expr.rfind('(')
            end = expr.find(')', start)
            if end != -1:
                sub_expr = expr[start+1:end]
                sub_val = self.eval_expr(sub_expr)
                expr = expr[:start] + str(sub_val) + expr[end+1:]
        
        # Handle multiplication, division, modulo
        for op in ['*', '/', '%']:
            while op in expr:
                parts = expr.split(op)
                for i in range(len(parts)):
                    if op in parts[i]:
                        continue
                    if i < len(parts) - 1:
                        left = parts[i].strip()
                        right = parts[i+1].strip()
                        
                        left_parts = left.split()
                        token_l = left_parts[-1] if left_parts else left
                        left_val = int(token_l) if token_l.isdigit() else self.vars.get(token_l, 0)
                        
                        right_parts = right.split()
                        token_r = right_parts[0] if right_parts else right
                        right_val = int(token_r) if token_r.isdigit() else self.vars.get(token_r, 0)
                        
                        if op == '*': result = left_val * right_val
                        elif op == '/': result = left_val // right_val
                        else: result = left_val % right_val
                        
                        left_part = ' '.join(left_parts[:-1]) if len(left_parts) > 1 else ''
                        right_part = ' '.join(right_parts[1:]) if len(right_parts) > 1 else ''
                        expr = left_part + " " + str(result) + " " + right_part
                        break
                break
        
        # Handle addition and subtraction
        for op in ['+', '-']:
            while op in expr:
                parts = expr.split(op)
                for i in range(len(parts)):
                    if op in parts[i]:
                        continue
                    if i < len(parts) - 1:
                        left = parts[i].strip()
                        right = parts[i+1].strip()
                        
                        left_parts = left.split()
                        token_l = left_parts[-1] if left_parts else left
                        left_val = int(token_l) if token_l.isdigit() else self.vars.get(token_l, 0)
                        
                        right_parts = right.split()
                        token_r = right_parts[0] if right_parts else right
                        right_val = int(token_r) if token_r.isdigit() else self.vars.get(token_r, 0)
                        
                        result = left_val + right_val if op == '+' else left_val - right_val
                        
                        left_part = ' '.join(left_parts[:-1]) if len(left_parts) > 1 else ''
                        right_part = ' '.join(right_parts[1:]) if len(right_parts) > 1 else ''
                        expr = left_part + " " + str(result) + " " + right_part
                        break
                break
        
        # Return result
        if expr.strip().isdigit():
            return int(expr.strip())
        return self.vars.get(expr.strip(), 0)
    
    def eval_condition(self, condition):
        """Evaluate a condition"""
        condition = condition.strip()
        ops = ['<=', '>=', '==', '!=', '<', '>']
        for op in ops:
            if op in condition:
                parts = condition.split(op)
                left_val = self.eval_expr(parts[0].strip())
                right_val = self.eval_expr(parts[1].strip())
                
                if op == '<=': return left_val <= right_val
                elif op == '>=': return left_val >= right_val
                elif op == '==': return left_val == right_val
                elif op == '!=': return left_val != right_val
                elif op == '<': return left_val < right_val
                elif op == '>': return left_val > right_val
        return bool(self.eval_expr(condition))


def run_file(filename):
    """Run a program from a file"""
    try:
        if not os.path.exists(filename):
            print(f"❌ ERROR: File '{filename}' not found!")
            return
        
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        
        interpreter = Interpreter()
        result = interpreter.run(code)
        
        if result:
            print(result)
        else:
            print("(Program executed successfully with no output)")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        print("🔧 Tiny Language Interpreter")
        print("=" * 40)
        print("Usage: python interpreter.py <filename>")
        print("Example: python interpreter.py test.tiny")
        print("=" * 40)
        
        default_code = """
let x = 1
let sum = 0

while x <= 5 {
    sum = sum + x
    x = x + 1
}

print "Sum is "
print sum
"""
        interpreter = Interpreter()
        result = interpreter.run(default_code)
        print("\n📝 Default Test Output:")
        print("-" * 40)
        print(result)
        print("-" * 40)