import requests
import csv
import argparse

GITHUB_TOKEN = "github_pat" #Add your github token

def get_github_contents(repo_url):
    parts = repo_url.rstrip('/').split('/')

    if len(parts) < 5 or parts[2] != "github.com":
        raise ValueError("Invalid GitHub URL. Ensure the URL is in the format: https://github.com/user/repo/tree/branch/path")

    user = parts[3]
    repo = parts[4]

    if "tree" in parts:
        branch = parts[6]
        subpath = '/'.join(parts[7:]) if len(parts) > 7 else ''
        api_url = f"https://api.github.com/repos/{user}/{repo}/contents/{subpath}?ref={branch}"
    else:
        api_url = f"https://api.github.com/repos/{user}/{repo}/contents/"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response.json()

def process_contents(contents, paths=[], parent_path="", exclude_folders=[]):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }
    for item in contents:
        path = parent_path + item['name']

        if item['type'] == 'dir' and item['name'] in exclude_folders:
            print(f"Skipping folder: {path}")
            continue

        print(f"Processing: {path}")

        if item['type'] == 'dir':
            dir_response = requests.get(item['url'], headers=headers)
            dir_response.raise_for_status()
            dir_contents = dir_response.json()
            process_contents(dir_contents, paths, path + "/", exclude_folders)
        elif item['type'] == 'file' and path.endswith('.py'):
            file_response = requests.get(item['download_url'], headers=headers)
            file_response.raise_for_status()
            file_content = file_response.text
            formatted_content = f"The following is a python document located at {path}\n------\n{file_content}\n------"
            paths.append(formatted_content)

    print(f"Found {len(paths)} python files.")
    return paths


def write_to_csv(data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow([row])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch markdown files from a GitHub repository and save to a CSV file.")
    parser.add_argument("repo_url", help="URL of the GitHub repository (e.g., https://github.com/user/repo/tree/branch)")
    parser.add_argument("output_path", help="Path to the output CSV file")
    parser.add_argument("--exclude", nargs='*', default=[], help="List of folder names to exclude")

    args = parser.parse_args()

    try:
        print(f"Starting script for repository: {args.repo_url}")
        contents = get_github_contents(args.repo_url)
        paths = process_contents(contents, exclude_folders=args.exclude)
        write_to_csv(paths, args.output_path)
        print(f"CSV file '{args.output_path}' generated successfully.")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
