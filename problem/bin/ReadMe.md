
# scripts

This directory holds a few scripts I have personally
found  useful over the years.
They are [MIT licensed](https://opensource.org/licenses/MIT).

## env_report.py

`cd` to where we find an `activate`d conda environment.yml,
and run this to identify downrev deps.
It is very simple, parsing out
[SemVer](https://semver.org/)
constraints of the form

    - some-dep >= 1.2.3

It might alert you that e.g. 1.2.5 or 1.3.1 is now available.
After you've edited the .yml with the more modern
constraint, the alert disappears. It's a bit like `make` --
keep re-running till it reports there's nothing left to do.

The intent of such constraints is to

    1. Remain on modern code with modern bug fixes.
    2. Remain on collection of deps that resembles what upstream developers used.
    3. Tell the conda solver to not spend time considering ancient combinations.

Beyond its simplicity, there is also a minor gotcha that
a package can be installed by both conda and pip.
For example we might see foo-1.2 and foo-1.1 respectively.
Last one (pip) wins.
Best course of action is usually to convince pip that the
one conda installed is "good enough", to avoid duplication.

## find.sh

When visiting a new project, this can be a convenient way
to focus on the "important" files, that is, the source code.
Also, unlike raw `find`, it offers filenames in
predictable sorted order.

## grep-find.sh

Wrapped around `find.sh`, this `grep`s a code base
for a regular expression.

A bit of care is sometimes needed to avoid grep'ing
files like "dictionary.txt" or minified javascript.
