## deduper

*deduper* will recursively read a directory of files and write them out to a new
directory with the filenames numbered sequentially after de-duplicating them.  
If a file occurs more than once in the source directory it will only be written
once to the target directory. A JSON file for each file will also be written to
the target directory which includes the target filename as well as the path(s)
for the original data.

## Usage 

```
% deduper path/to/source path/to/target
```

If the source looks like:

```
source
├── a.jpg
├── a.png
├── b.jpg
├── c
│   ├── a.jpg
│   └── b.jpg
└── c.jpg
    └── a.jpg
```

The resulting target will look like:

```
target
├── 1.png
├── 2.jpg
├── 3.jpg
└── data.json
```

and the *data.json* file will look like:

```json
```
