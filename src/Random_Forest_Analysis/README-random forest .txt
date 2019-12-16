Run randomForest.py in src directory. Requires scikit learn and numpy modules.

Written and tested in Spyder on Windows 10. Should work with Unix systems, but not tested.  

Builds a folder called ML_data and fills it with data from the resources file. Currently setup to include all the github projects analyzed for this project. Additional ones may be added by modifying PROJECTS variable at top of file.

The number of trees and the percent of data to use for training vs testing can also be set in main().

Rerunning the script will NOT overwrite ML_data. If user wants to rewrite it, they'll need to delete the data and modify the projects_added.txt file in the ML_data folder. 
To add new data for a certain project that has already been added, delete name from projects_added.txt. Again, this will not rewrite data, but will add new files.

Larger files can be deleted from ML_data if there are memory issues. 