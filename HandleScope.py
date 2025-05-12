import os
import re
import sys

pattern = re.compile(r'(?P<scope>(?:v8::)?(?:HandleScope|EscapableHandleScope|SealHandleScope) )')

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    changed = False
    new_lines = []
    for line in content.splitlines(keepends=True):
        if 'using' in line or '//' in line or 'Debug' in line or 'Node' in line:
            new_lines.append(line)
        else:
            def replacement(m):
                text = m.group("scope")
                if text.startswith("v8::"):
                    return "node::Node" + text[4:]
                else:
                    return "node::Node" + text

            new_line = pattern.sub(replacement, line)
            if new_line != line:
                changed = True
            new_lines.append(new_line)

    new_content = ''.join(new_lines)
    if changed:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Modified: {file_path}")
        except Exception as e:
            print(f"Error writing {file_path}: {e}")

def process_directory(directory):
    blocklist = ['node.h', 'environment.cc']
    for root, dirs, files in os.walk(directory):
        for file in files:
            if (file.endswith('.cc') or file.endswith('.h')) and str(file) not in blocklist:
                file_path = os.path.join(root, file)
                process_file(file_path)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python HandleScope.py <directory>")
        sys.exit(1)
    target_directory = sys.argv[1]
    process_directory(target_directory)