## dedoop

[![Build Status](https://secure.travis-ci.org/edsu/dedoop.png)](http://travis-ci.org/edsu/dedoop)

In [digital preservation] work you sometimes may find yourself accepting a disk
or random assortment of files, and want to examine all of them looking for
duplicates and copy them to a new location in a uniform way, while preserving
the original paths as metadata to help you process the data. I know, I know,
this sounds pretty esoteric, and it really, really is. Never the less, this is
the use case that *dedoop* was created for.

*dedoop* will recursively read a source directory of files and write them out to
a new target directory with the filenames numbered sequentially after
de-duplicating them. If a given file occurs more than once in the source
directory it will only be written once to the target directory. A JSON file will
also be written to the target directory which includes the target filename as
well as all the path(s) used in the source directory. The files are compared by
computing a sha256 digest.

## Install

Install Python 3 and:

```
% pip install dedoop
```

## Usage 

```
% dedoop path/to/source path/to/target
```

So for example if the source directory looks like this:

```
source
├── a.jpg
├── a.png
├── b.jpg
└── c
    ├── a.jpg
    └── b.jpg
```

The resulting target will look like:

```
target
├── 1e89b90b5973baad2e6c3294ffe648ff53ab0b9d75188e9fbb8b38deb9ba3341.png
├── 45d257c93e59ec35187c6a34c8e62e72c3e9cfbb548984d6f6e8deb84bac41f4.jpg
└── b6df8058fa818acfd91759edffa27e473f2308d5a6fca1e07a79189b95879953.jpg
```

## Options

You can give the *--extensions* command line option a comma separated list of
file extensions to duplicate. All non-matching files (case insensitive) will
be ignored.

```
% dedoop --extensions jpg,png path/to/source path/to/target
```

If you use *--verbose* you will see log messages on the console about what is
happening. You can optionally send these messages to a log file of your choosing
using the *--log* option.

[digital preservation]: https://en.wikipedia.org/wiki/Digital_preservation
