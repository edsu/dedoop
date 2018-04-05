## dedoop

*dedoop* will recursively read a directory of files and write them out to a new
directory with the filenames numbered sequentially after de-duplicating them.  
If a file occurs more than once in the source directory it will only be written
once to the target directory. A JSON file for each file will also be written to
the target directory which includes the target filename as well as the path(s)
for the original data.

## Usage 

```
% dedoop path/to/source path/to/target
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
{
  "items": [
    {
      "path": "1.png",
      "sha256": "1e89b90b5973baad2e6c3294ffe648ff53ab0b9d75188e9fbb8b38deb9ba3341",
      "original_paths": [
        "test-data/a.png"
      ]
    },
    {
      "path": "2.jpg",
      "sha256": "45d257c93e59ec35187c6a34c8e62e72c3e9cfbb548984d6f6e8deb84bac41f4",
      "original_paths": [
        "test-data/b.jpg",
        "test-data/c/b.jpg"
      ]
    },
    {
      "path": "3.jpg",
      "sha256": "b6df8058fa818acfd91759edffa27e473f2308d5a6fca1e07a79189b95879953",
      "original_paths": [
        "test-data/a.jpg",
        "test-data/c/a.jpg"
      ]
    }
  ]
}
```

and a CSV that looks like:

```csv
path,original_paths,sha256
1.png,test-data/a.png,1e89b90b5973baad2e6c3294ffe648ff53ab0b9d75188e9fbb8b38deb9ba3341
2.jpg,"""test-data/b.jpg"",""test-data/c/b.jpg""",45d257c93e59ec35187c6a34c8e62e72c3e9cfbb548984d6f6e8deb84bac41f4
3.jpg,"""test-data/a.jpg"",""test-data/c/a.jpg""",b6df8058fa818acfd91759edffa27e473f2308d5a6fca1e07a79189b95879953
```
