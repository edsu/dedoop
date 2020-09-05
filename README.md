## dedoop

[![Build Status](https://secure.travis-ci.org/edsu/dedoop.png)](http://travis-ci.org/edsu/dedoop)

In [digital preservation] work you sometimes may find yourself accepting a disk
or random assortment of files, and want to examine all of them looking for
duplicates and copy them to a new location in a uniform way, while preserving
the original paths as metadata to help you process the data. Ok, maybe this is a
bit of niche use case, but this is what *dedoop* was created for.

*dedoop* will recursively read a source directory of files and write them out to
a new target directory or bucket in the cloud using the files's SHA256 checksum
as the filename. If a given file occurs more than once in the source
directory it will only be written once to the target location. File metadata
such as the media type and original file name will be persisted in a JSON file
that is output at the end of the process. In the case of writing to the cloud,
object metadata will be used to store this information.

## Install

Install Python 3 and:

```
% pip3 install dedoop
```

## Usage 

### Add to Storage

To add a directory of data to the storage location you can:

    % dedoop add path/to/source path/to/target

So for example if the source directory looks like this:

    source
    ├── a.jpg
    ├── a.png
    ├── b.jpg
    └── c
        ├── a.jpg
        └── b.jpg

The resulting target could look like this (assuming the files of the same name
had the same contents that hashed to these values):

    target
    ├── 1e89b90b5973baad2e6c3294ffe648ff53ab0b9d75188e9fbb8b38deb9ba3341.png
    ├── 45d257c93e59ec35187c6a34c8e62e72c3e9cfbb548984d6f6e8deb84bac41f4.jpg
    └── b6df8058fa818acfd91759edffa27e473f2308d5a6fca1e07a79189b95879953.jpg

## Add to the Cloud

You can also write files to any cloud storage provider that is [supported] by [libcloud],
such as Amazon S3, Google Cloud Storage, etc.

## Limit by File Extension

If you like you can limit the types of files that are added by using the
*--extensions* command line option and giving it a comma separated list of file
extensions to include. All non-matching files (case insensitive) will be
ignored.

    % dedoop add --extensions jpg,png path/to/source path/to/target

## List Cloud Files

Its easy to list files on the file system. But its more difficult to see what's
in the cloud--especially with the  metadata dedoop has attached to each object.
The *list* command will do that for you.

    % dedoop ls s3://my-storage-location/

## Logging

If you use *--verbose* you will see log messages on the console about what is
happening. You can optionally send these messages to a log file of your choosing
using the *--log* option.

[digital preservation]: https://en.wikipedia.org/wiki/Digital_preservation
[libcloud]: https://libcloud.readthedocs.io
[supported]: https://libcloud.readthedocs.io/en/stable/storage/supported_providers.html
