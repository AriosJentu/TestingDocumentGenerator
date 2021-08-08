# Simple Testing Document Generator
A simple script that allows you to create documents based on document patterns and a custom tasks list.

# Table of contents
[TOC]

# Overview
Simple Testing Document Generator is a project for generating documents based on moduling system. Any module that meets the design requirements of the project can be used to create documents that satisfy certain user-defined layouts. 
Information about module design can be found on wiki-page about Modules.

# Usage
To use this project, need just to download *Zip* archive from the repository, and write your own module. There is main file for execute: `main.py`.  By default, arguments defined with class `Parser.Generator`. Usage of the script with default arguments:
```shell
python main.py [module-name] [key][indicies] [entries-location/entry-element] {[entry-group] [-a] [-s]}
```
**Arguments are:**
- `module-name` - name of the module.
- `key` - single letter of the assignment name.
- `indicies` - one index, list of indicies or indicies range with assignment numbers (can be `1`, `1,2` or `1-4`).
Pair `[key][indicies]` can be separated with `;` symbol.
- `entries-location` - location of the file where entries will be loaded.
- `entry-element` - string of the entry name.
Entries also can be multiple values, separated with `;` symbol.
- `entry-group` - argument with group-name of entries. If using `entries-location`, this name must be in first line of the file.
- `-a` - argument for debug, generates all tasks in one document to check the correctness of their display.
- `-s` - argument for separating same-type assignments in different files. 
By default (without this argument) it combine same assignments in one file.

**Example of usage:**
```shell
py main.py test t1,2 "Student 1;Student 2" "Group name"
```
will generate assignments `test1` and `test2` for students `Student 1` and `Student 2` (in one file) from `Group name`

You can also write your own parsing arguments script in special form.

# Requirements
- Python 3