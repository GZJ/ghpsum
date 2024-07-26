import requests
import pandas as pd
import argparse
import json
from string import Template


def get_repositories(username, filter_fork, filter_github_io):
    api_url = f"https://api.github.com/users/{username}/repos"

    response = requests.get(api_url)
    repos = response.json()

    if response.status_code != 200:
        print(f"Failed to retrieve repositories: {response.status_code}")
        exit()

    repo_data = []
    for repo in repos:
        if filter_fork and repo["fork"]:
            continue
        if filter_github_io and "github.io" in repo["name"]:
            continue
        repo_name = repo["name"]
        repo_url = repo["html_url"]
        repo_description = (
            repo["description"] if repo["description"] else "No description"
        )
        repo_data.append(
            {"Name": repo_name, "URL": repo_url, "Description": repo_description}
        )

    return repo_data


def generate_html_table(data, output_file):
    table_template = Template("""
    <html>
    <head>
        <title>GitHub Repositories</title>
    </head>
    <body>
        <h1>GitHub Repositories</h1>
        <table border="1">
            <tr>
                <th>Name</th>
                <th>Description</th>
            </tr>
            $table_rows
        </table>
    </body>
    </html>
    """)

    row_template = Template("""
            <tr>
                <td><a href="$repo_url">$repo_name</a></td>
                <td>$repo_description</td>
            </tr>
    """)

    table_rows = ""
    for repo in data:
        table_rows += row_template.substitute(
            repo_name=repo["Name"],
            repo_url=repo["URL"],
            repo_description=repo["Description"],
        )

    html_content = table_template.substitute(table_rows=table_rows)

    with open(output_file, "w") as file:
        file.write(html_content)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch GitHub repositories and their descriptions."
    )
    parser.add_argument("--username", type=str, required=True, help="GitHub username")
    parser.add_argument(
        "--filter-fork", action="store_true", help="Filter out forked repositories"
    )
    parser.add_argument(
        "--filter-github-io",
        action="store_true",
        help="Filter out repositories containing github.io",
    )
    parser.add_argument(
        "--output-name", type=str, default="ghpsum", help="Output file name"
    )
    parser.add_argument(
        "--output-format",
        type=str,
        choices=["csv", "json", "html"],
        required=True,
        help="Output file format: csv, json or html",
    )

    args = parser.parse_args()

    repo_data = get_repositories(args.username, args.filter_fork, args.filter_github_io)

    output_file = f"{args.output_name}.{args.output_format}"
    if args.output_format == "csv":
        df = pd.DataFrame(repo_data)
        df.to_csv(output_file, index=False)
        print(
            f"Repository names and descriptions of {args.username}'s projects have been saved to {output_file}"
        )
    elif args.output_format == "json":
        with open(output_file, "w") as f:
            json.dump(repo_data, f, indent=4)
        print(
            f"Repository names and descriptions of {args.username}'s projects have been saved to {output_file}"
        )
    elif args.output_format == "html":
        generate_html_table(repo_data, output_file)
        print(
            f"Repository names and descriptions of {args.username}'s projects have been saved to {output_file}"
        )


if __name__ == "__main__":
    main()
