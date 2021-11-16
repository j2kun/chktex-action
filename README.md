# Lint your LaTeX files with chktex

[chktex](https://www.nongnu.org/chktex/) is a LaTeX linter. A _linter_ is a
program that checks your work for stylistic errors. In the case of LaTeX, style
errors include soft tex-O's (which don't generate errors) and decisions that
result in rendering irregularities.

This action runs chktex on all `.tex` files in your repository.

To configure the linter, add a `.chktexrc` file to your repository. An example
is provided in this repo.

Example configuration: https://gist.github.com/j2kun/aa4a768150d423f581b758103b2b020c

```
# in .github/workflows/lint.yml

name: Lint

on: 
  push:
    branches:
      - main
  pull_request:
    branches:
      - main


jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v1
    - name: LaTeX linter (chktex)
      uses: j2kun/chktex-action@main
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
