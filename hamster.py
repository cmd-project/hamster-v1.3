import time
import re
import sys
import os

class HamsterInterpreter:
    def __init__(self):
        self.variables = {}
        self.styles = {
            'red': '31',
            'green': '32',
            'blue': '34',
            'yellow': '33',
        }
        self.input_values = {}
        self.print_styles = {}
        self.execution_flag = False  # Track if any `if` or `else` block has been executed

    def execute(self, code):
        lines = code.split('\n')
        self.execution_flag = False
        for line in lines:
            line = line.strip()
            if not self.execution_flag:
                if line.startswith('print_text'):
                    self.handle_print_text(line)
                elif line.startswith('time.s'):
                    self.handle_time_s(line)
                elif line.startswith('print_text_var'):
                    self.handle_print_text_var(line)
                elif line.startswith('time_print'):
                    self.handle_time_print(line)
                elif line.startswith('var'):
                    self.handle_variable_declaration(line)
                elif line.startswith('typeof?var'):
                    self.handle_typeof_var(line)
                elif line.startswith('style.color.'):
                    self.handle_style_color(line)
                elif line.startswith('m '):
                    self.handle_m(line)
                elif re.match(r'.* = input\(\)', line):
                    self.handle_myinput(line)
                elif re.match(r'.* @if', line):
                    self.handle_if(line)
                elif re.match(r'.* @else', line):
                    self.handle_else(line)
                elif line.startswith('/*') and line.endswith('*/'):
                    pass  # Comment, ignore it

    def handle_print_text(self, line):
        match = re.match(r'print_text\["(.*)"\]', line)
        if match:
            print(match.group(1))

    def handle_time_s(self, line):
        match = re.match(r'time\.s\(n\("(\d+)"\)\)', line)
        if match:
            seconds = int(match.group(1))
            time.sleep(seconds)

    def handle_print_text_var(self, line):
        match = re.match(r'print_text_var(?:\(id="(.*?)"\))? => #(.*)', line)
        if match:
            var_id = match.group(1)
            var_name = f'#{match.group(2)}'
            value = self.variables.get(var_name, '')
            color_code = self.print_styles.get(var_id, '0')  # Default color
            print(f'\033[{color_code}m{value}\033[0m')

    def handle_time_print(self, line):
        match = re.match(r'time_print(?:\(id="(.*?)"\))?', line)
        if match:
            print(time.strftime("%Y-%m-%d %H:%M:%S"))

    def handle_variable_declaration(self, line):
        match = re.match(r'var #(\w+) === "(.*)"', line)
        if match:
            var_name = f'#{match.group(1)}'
            value = match.group(2)
            self.variables[var_name] = value

    def handle_typeof_var(self, line):
        match = re.match(r'typeof\?var\(var = #(.*); print_typeof_text\)', line)
        if match:
            var_name = f'#{match.group(1)}'
            value = self.variables.get(var_name)
            if value is not None:
                if value.isdigit():
                    print("number")
                else:
                    print("text")

    def handle_style_color(self, line):
        match = re.match(r'style\.color\.(\w+)\((red|yellow|green|blue)\)', line)
        if match:
            print_name = match.group(1)
            color_name = match.group(2)
            color_code = self.styles.get(color_name, '0')  # Default to no color
            self.print_styles[print_name] = color_code

    def handle_m(self, line):
        match = re.match(r'm\s+"(.*)";', line)
        if match:
            print(match.group(1))

    def handle_myinput(self, line):
        match = re.match(r'(\w+)\s*=\s*input\(\)', line)
        if match:
            input_id = match.group(1)
            value = input("Enter input: ")
            self.input_values[input_id] = value

    def handle_if(self, line):
        if self.execution_flag:
            return  # Skip if any `if` or `else` block has already been executed

        match = re.match(r'(\w+) @if\s*=>\s*user="(.*?)",\s*\{(.+?)\}', line, re.DOTALL)
        if match:
            input_id = match.group(1)
            expected_value = match.group(2)
            code_block = match.group(3).strip()
            user_input = self.input_values.get(input_id, '')
            if user_input == expected_value:
                self.execution_flag = True  # Set flag to true
                self.execute(code_block)

    def handle_else(self, line):
        if self.execution_flag:
            return  # Skip if any `if` block has been executed

        match = re.match(r'(\w+) @else\s*\{(.+?)\}', line, re.DOTALL)
        if match:
            input_id = match.group(1)
            code_block = match.group(2).strip()
            user_input = self.input_values.get(input_id, '')
            if user_input != "":
                self.execution_flag = True  # Set flag to true
                self.execute(code_block)

def run_hamster_file(file_path):
    if not file_path.endswith('.hamster'):
        print("Error: The file must have a '.hamster' extension.")
        return

    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    with open(file_path, 'r') as file:
        code = file.read()

    interpreter = HamsterInterpreter()
    interpreter.execute(code)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python hamster200.py <filename.hamster>")
        print("version hamster: v1.3")
    else:
        filename = sys.argv[1]
        run_hamster_file(filename)
              
