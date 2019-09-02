# Lint your LaTeX files with chktex

[chktex](https://www.nongnu.org/chktex/) is a LaTeX linter. A _linter_ is a
program that checks your work for stylistic errors. In the case of LaTeX, style
errors include soft tex-O's (which don't generate errors) and decisions that
result in rendering irregularities.

This action runs chktex on all `.tex` files in your repository.

To configure the linter, add a `.chktexrc` file to your repository. An example
is provided in this repo.
