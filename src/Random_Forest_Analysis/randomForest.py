import os
from os.path import join
from glob import glob
from random import randint
import numpy as np
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer


RESOURCES_DIR = '../resources/'
ML_DATA_DIR = '../ML_data/'

# Add the folder names of any projects you'd like to have included here.
# Must be in RESOURCES_DIR. Will not re-add a project unless name removed from projects_added.txt
PROJECTS = ['Arduino', 'ardupilot', 'elasticsearch', 'grpc', 'Marlin', 'numpy', 
            'opencv', 'php-src', 'RxJava']


def add_files_from_folder(folder_name, trainPercent):
    """
    Goes through all of the files in the given folder and converts each .diff file
    into a before and after version. Selects a given percent of the files to be
    used for training or testing the ML model.
    """
    
    printedMessage = False
    
    # Finds all sub folders inside the given folder
    paths = glob(join(RESOURCES_DIR, folder_name, "*"))
    
    # Itterates through these folders to find diff files and convert them
    for path in paths:     
        diff_file = join(path, 'pull_request.diff')
        
        # Determine the ID number for the file
        if os.name == 'nt':                     # For a Windows machine
            pr_number = path.split('\\')[-1]
        else:                                   # For Unix
            pr_number = path.split('/')[-1]            
            

        # Generate a random integer to decide if a specific peice of data will be training or testing
        i = randint(1, 100)
        if i <= trainPercent:
            newPath = join(ML_DATA_DIR, 'training/')
        else:
            newPath = join(ML_DATA_DIR, 'testing/')
            
        # Checks if the given paths exist and creates them if they do not
        if not os.path.exists(newPath):
            os.makedirs(newPath)
            
        # Old version gets labeled as .bugged, new version as .fixed
        old_code = join(newPath, folder_name + str(pr_number) + '.bugged')
        new_code = join(newPath, folder_name + str(pr_number) + '.fixed')
        
            
        # Erase unncessary lines and create new files
        try:
            # Checks to see if data already exists 
            # Disabling this causes files to be written in both training and testing folders and will invalidate testing
            for folder in ('training/', 'testing/'):
                if os.path.exists(join(ML_DATA_DIR, folder, folder_name + str(pr_number) + '.bugged')):
                    if not printedMessage:
                        print("\tWARNING: \n\tSome files have not been overwritten in folder ", folder_name, ". \n\tIf you'd like to rewrite data, please delete both old versions (.bugged and .fixed) and try again. \n\tYou can ignore this if you're only adding new data.", sep='')
                        printedMessage = True
                        
            # Open original file
            with open(diff_file, 'r') as df:      
                # Open both new files
                nc = open(new_code, 'w')
                oc = open(old_code, 'w')

                # Itterate through lines
                line = df.readline()
                while line:
                    # Excludes descriptions of data
                    if (line[0:4] != 'diff' and line[0:5] != 'index' and 
                        line[0:3] != '---' and line[0:3] != '+++' and line[0:2] != '@@' and
                        line[0:13] == 'new file mode' and line[0:17] == 'deleted file mode'):
                        
                        # Identify which lines are new, which were deleted, and which are old but not deleted and write to appropriate file(s).
                        if line[0] == '+':
                            nc.write(line[1:])
                        elif line[0] == '-':
                            oc.write(line[1:])
                        else:
                            nc.write(line[1:])
                            oc.write(line[1:])
                        
                    line = df.readline()
                    
            nc.close()
            oc.close()
        except (UnicodeDecodeError) as e:
            pass

    # List which projects have been added already    
    projectsAdded = open(join(ML_DATA_DIR, 'projects_added.txt'), 'a')
    print(folder_name, file=projectsAdded)
    projectsAdded.close()
    return()

def data_prep(trainPercent): 
    """
    Manages machine learning database. Will add new projects and prevent overwriting of existing ones.
    Returns nothing, since the other functions use the files it creates directly.
    """
    newProjects = PROJECTS
    
    # lists projects already added to training/testing data, if there are any and removes them from newProjects list
    try:
        with open(join(ML_DATA_DIR, 'projects_added.txt'), 'r') as existingProjects:
            line = existingProjects.readline()
            while line:       
                print(line[:-1], end=', ')
                newProjects.remove(line[:-1])
                line = existingProjects.readline()
            print('have already been successfully added to the training/testing data.')
    except FileNotFoundError:
        pass
    
    # if there's still items in the newProjects list, these are actual new projects. Informs user they will be added.
    if newProjects == []:
        print('Nothing more', end=' ')
    for items in newProjects:
        print(items, end=', ')    
    print('will be added. \nIf you wish to add any additional data, please add to PROJECTS variable.')
    print('--------------------------------------------------------------------------------------------')
         
    
    # Takes raw dataq from resources file, parses it, cleans it up, and adds it to training and testing folders
    for name in newProjects:
        print('- Begining to parse', name, 'data. . . ', end='\t')
        add_files_from_folder(name, trainPercent)
        print('-', name, 'has completed.')
        
    return()

def train_randomForest(numTrees):
    """
    Goes through the files in the ML database's training folder and then loads them into a 
    list of lists, randomizes them, and saves the data labels for training. 
    Then tokenizes and vectorizes the data and uses it to feed the random forest
    ML model.
    Returns the model object, the feature names, and labels.
    Also returns the the training dataset in case user wants it.
    """
    training_dataset = []
    training_labels = []
    
    # Collects the paths of all the training data
    trainingPaths = glob(join(ML_DATA_DIR, 'training/', "*"))
    # shuffle the dataset so the ML model receives it in a random order.        
    random.shuffle(trainingPaths)
    
    print("Setting up input...\t", end='')
    # reopens the training data and turns it into a list of lists containing every line of code
    for file in trainingPaths:    
        data = ''
        label = file.split('.')[-1]
        if label == 'bugged':
            training_labels.append(1)
        else:
            training_labels.append(0)
        with open(file, 'r') as f:
            l = f.readline()
            while l:
                data += '\n' + l
                l = f.readline()
    
            training_dataset.append(data) 
    print("Done.")
    
    print("Training randomForrestClassification model with", len(training_dataset), "files...\t", end='')
    # Tokenizes the data. See scikit's documentation on TfidfVectorizer() for more info.
    vectorizer = TfidfVectorizer()
    training_data = vectorizer.fit_transform(training_dataset)
    
    # Trains the randomForestClassifier model
    randomForest = RandomForestClassifier(n_estimators = numTrees, n_jobs=3)
    randomForest.fit(training_data, training_labels)
    # Save the feature names and pass them to testing function so that it vectorizes that data correctly.
    feature_names = vectorizer.get_feature_names()
    
    print("Done.")
    return(randomForest,feature_names , training_dataset, training_data, training_labels)  
    
    
def test_randomForest(randomForest, feature_names):
    """
    Opens the files from the training folder in the machine learning database.
    Uses the same features from before to vectorize the data and then feed it 
    into the ML model to get predictions. R
    """
    testing_dataset = []
    testing_labels = []

    testingPaths = glob(join(ML_DATA_DIR, 'testing/', "*"))
    # shuffle the dataset so the ML model receives it in a random order.        
    random.shuffle(testingPaths)
    
    for file in testingPaths:    
        data = ''
        label = file.split('.')[-1]
        if label == 'bugged':
            testing_labels.append(1)
        else:
            testing_labels.append(0)
        with open(file, 'r') as f:
            l = f.readline()
            while l:
                data += '\n' + l
                l = f.readline()
            
            testing_dataset.append(data) 

    print("Testing randomForrestClassification model with", len(testing_dataset), "files...\t", end='')
    vectorizer = TfidfVectorizer(vocabulary =feature_names)
    testing_data = vectorizer.fit_transform(testing_dataset)
    
    predictions = randomForest.predict(testing_data)
    
    print("Done.")
    
    return(predictions, testing_labels, testing_data)
    
def main():
    # Percent of data used to train ML model
    trainPercent = 75
    
    # The number of trees to use in the randomForest model 
    numTrees = 100
    
    # Calls function to set up ML database from .diff files
    data_prep(trainPercent)
    
    # Trains the randomForestClassification ML model
    randomForest, feature_names , training_dataset, training_data, training_labels = train_randomForest(numTrees)
    
    # Tests the performance of the model
    predictions, testing_labels, testing_data = test_randomForest(randomForest, feature_names )
    
    
    trainingRsquared = randomForest.score(training_data, training_labels)
    print("The accuracy in for the training dataset is: \t", trainingRsquared * 100, "%", sep='')
    
    
    # Calculates the accuracy and types of resutls
    i = 0
    correctPositives, correctNegatives, falsePositives, falseNegatives = 0,0,0,0
    
    for prediction in predictions:
        if testing_labels[i] == prediction:
            if prediction ==1:
                correctPositives += 1
            else:
               correctNegatives += 1
        elif prediction == 1:
            falsePositives += 1
        elif prediction == 0:
            falseNegatives += 1
        i += 1
    
    accuracy = (correctPositives + correctNegatives) / len(predictions)
    print("The accuracy for the testing data is: \t\t", accuracy * 100, "%", sep='')
    print("The data showed", falsePositives, "false positives and", falseNegatives, "false negatives." )
    
    return()


if __name__ == "__main__":
    main()