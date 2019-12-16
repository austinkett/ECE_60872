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
The current iteration of this is complete. We are looking into future improvements to be made to our analysis which
will likely take place over the next month.

Plans include:
- Doing an analysis on N-Version programs
- Doing an analysis on files written to perform the same task but in different languages
- Trying out other machine learning models for bug classification
- Trying out other machine learning models for classifying which bugs are reproducible
 
## File Descriptions
resources:
- The resource folders here contain bug patches from many different large github projects
as well as their pull request information. 
- defects4J_JacksonDatabind - A list of reproducible bug issues from JacksonDatabind

src:
- scrape.py - This requests and saves pull requests from Github repos
- compare.py - This utilizes moss to compares batches of files
- ml_text_classification - This runs a naive Bayes classifier on a set of reproducible and non-reproducible bugs
- scrape_issue - A module built to scrape issues from JacksonDatabind

labeled_repos.yaml:
- This file should be filled out with repo names and the label you are looking for. After
you supply that information it will automatically build a database for you.

## Documentation
<a href="https://drive.google.com/drive/folders/1_tWJnuwvGK4Sipk9GKJuF0c3zbFcgULW?usp=sharing" target="_blank">**Google Drive**</a>
