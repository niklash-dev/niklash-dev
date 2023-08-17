import os, re
from github import Github

REPO_NAME = "YOUR_GITHUB_USERNAME/YOUR_REPO_NAME"
README_PATH = "README.md"

def fetch_gists(token):
    g = Github(token)
    user = g.get_user()
    return user.get_gists()

def update_readme(gists, readme_path):
    with open(readme_path, 'r', encoding='utf-8') as file:
        content = file.read()

    pattern = r"### Latest GitHub Gists.*?Feel free to check them out and provide any feedback!"
    replacement = "### Latest GitHub Gists\n\n"

    for gist in gists:

        if not gist.public:
            continue

        filename = list(gist.files.keys())[0]
        replacement += f"- [**{filename}**]({gist.html_url}) {(': ' + gist.description) if gist.description else ''}\n"

    replacement += "\nFeel free to check them out and provide any feedback!"

    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(readme_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

def main():
    token = os.environ['ACCESS_TOKEN']
    gists = fetch_gists(token)
    update_readme(gists, README_PATH)

if __name__ == "__main__":
    main()
