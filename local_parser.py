import os
import csv
import sys

csv.field_size_limit(10**9)

def process_local_repo(repo_path, paths=[]):
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                file_content = f.read()
            relative_path = os.path.relpath(file_path, repo_path)
            extension = os.path.splitext(relative_path)[1]
            
            if extension == '.md':
                formatted_content = f"The following is a markdown document located at {relative_path}\n------\n{file_content}\n------"
            elif extension == '.rs':
                formatted_content = f"```rust:{relative_path}\n{file_content}\n```"
            elif extension == '.sh':
                formatted_content = f"```bash:{relative_path}\n{file_content}\n```"
            elif extension == '.py':
                formatted_content = f"```python:{relative_path}\n{file_content}\n```"
            elif extension == '.js':
                formatted_content = f"```javascript:{relative_path}\n{file_content}\n```"
            elif extension == '.json':
                formatted_content = f"```json:{relative_path}\n{file_content}\n```"
            elif extension == '.txt':
                formatted_content = f"The following is a plain text file located at {relative_path}\n------\n{file_content}\n------"
            elif extension == '.toml':
                formatted_content = f"```toml:{relative_path}\n{file_content}\n```"
            elif extension == '.jsx':
                formatted_content = f"```jsx:{relative_path}\n{file_content}\n```"
            elif extension == '.css':
                formatted_content = f"```css:{relative_path}\n{file_content}\n```"
            elif extension == '.java':
                formatted_content = f"```java:{relative_path}\n{file_content}\n```"
            elif extension == '.hpp':
                formatted_content = f"```hpp:{relative_path}\n{file_content}\n```"
            elif extension == '.c':
                formatted_content = f"```c:{relative_path}\n{file_content}\n```"
            elif extension == '.yml':
                formatted_content = f"```yml:{relative_path}\n{file_content}\n```"
            elif extension == '.xml':
                formatted_content = f"```xml:{relative_path}\n{file_content}\n```"
            elif extension == '.html':
                formatted_content = f"```html:{relative_path}\n{file_content}\n```"
            elif extension == '.tsx':
                formatted_content = f"```typescript:{relative_path}\n{file_content}"
            else:
                formatted_content = f"The following document is located at {relative_path}\n------\n{file_content}\n------"
            paths.append({"FormattedContent": formatted_content})
    return paths

def write_to_csv(data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow([row['FormattedContent']])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <repo_url> <output_csv_path>")
        sys.exit(1)

    repo_path = sys.argv[1]
    output_path = sys.argv[2]
    paths = process_local_repo(repo_path)
    write_to_csv(paths, output_path)
    print(f"CSV file '{output_path}' generated successfully.")
