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
Which are your access keys for moss and github respectively. Note that the pull request saves the information about the
github token that was used to access it so if you are planning to make your repo public I
suggest that you delete that token from the files or delete the token itself. 
## Current Objective
Currently we have built a script to build a database and send it to MOSS. This was
unsuccessful so we are looking to machine learning approaches.
## File Descriptions
resources:
- The resource folders here contain bug patches from many different large github projects
as well as their pull request information. 

src:
- scrape.py - This requests and saves pull requests from Github repos
- compare.py - This utilizes moss to compares batches of files

labeled_repos.yaml:
- This file should be filled out with repo names and the label you are looking for. After
you supply that information it will automatically build a database for you.

## Documentation
<a href="https://drive.google.com/drive/folders/1_tWJnuwvGK4Sipk9GKJuF0c3zbFcgULW?usp=sharing" target="_blank">**Google Drive**</a>
