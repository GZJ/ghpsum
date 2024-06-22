# ghpsum

`ghpsum` is a tool to generate a summary file of all projects and descriptions for a given GitHub user.

## Quickstart

```sh
python ghpsum.py --username GZJ --output-format csv
python ghpsum.py --username GZJ --output-format json
python ghpsum.py --username GZJ --output-format html

#filter fork projects and github pages
python ghpsum.py --username GZJ --filter-fork --output-format json
python ghpsum.py --username GZJ --filter-fork --filter-github-io --output-format json
```
