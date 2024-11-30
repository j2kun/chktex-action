# ChkTeX Action

## _Lint your LaTeX files with ChkTeX_

[ChkTeX](https://www.nongnu.org/chktex/) is a LaTeX linter.
A _linter_ is a program that checks your work for stylistic errors.
In the case of LaTeX, style errors include soft tex-O's (which don't generate errors) and decisions that result in
rendering irregularities.

This action runs ChkTeX on all `.tex` files in your repository.

To configure the ChkTeX, add a `.chktexrc` file to your repository.
An example is provided in this repo.
If no local repository `.chktexrc` file can be found, the action will use the global ChkTeX configuration distributed as
part of the ChkTeX software that runs in the Action container.

To use this action in your repository, add it to your custom workflow.
See an example below:

```yml
name: Lint
on:
  push:
jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Run ChkTeX
        uses: j2kun/chktex-action@main
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
