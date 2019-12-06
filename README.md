# ECE 60872  Project
The goal of this code is to compare code from Github and try and utilize a database of available bugs to explore the possibility of cross language bug detection.
## Table of Contents
- [Read Before Using](#Read-Before-Using)
- [Current Objective](#Current-Objective)
- [File Descriptions](#File-Descriptions)
- [Documentation](#Documentation)
## Read Before Using
This requires that you make your own file called keys.yaml
It should contain:
moss_key: #
github_key: #
Which are your access keys for moss and github respectively.
## Current Objective
Currently trying to fill out database properly and find best attributes to compare.
## File Descriptions

resources:
- angr-doc:
    - This contains pull request information from the angr-doc repo as well as the diff patches.

src:
- scrape.py - This requests and saves pull requests from Github repos
- compare.py - This utilizes moss to compares batches of files

## Documentation
<a href="https://drive.google.com/drive/folders/1_tWJnuwvGK4Sipk9GKJuF0c3zbFcgULW?usp=sharing" target="_blank">**Google Drive**</a>
