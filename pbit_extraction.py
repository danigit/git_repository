"""
    # This file extracts the pbit files that are  passed as a parameter and changes
    # the extension of the DataModelSchema and Layout files to json
    
"""

#### importing necessary lybraries
import os
import shutil
import zipfile
import sys


#### defining the main function
def pbit_manipulation(folder_path):
    """
    Function that search for pbit files at the location passed as parameter,
    converts them to zip files, extracts them and inside each extracted folder
    changes the extension of the DAtaModelSchema and Layout files to json
    Args:
        folder_path (string): the path where the pbit files are stored
        file_name (list): the name of the pbit files
    """

    #### getting all the files in the dyrectory
    for file in os.scandir(folder_path):
        #### controlling if the file is a pbit file
        if os.path.isfile(file.path) and file.name.endswith(".pbit"):
            #### changing the extension
            zip_path = file.path.replace(".pbit", ".zip")
            if os.path.exists(zip_path):
                os.remove(zip_path)

            print("Creating zip file ...")
            os.rename(file.path, zip_path)
            print("Zip file created")

            #### extracting the zip file
            extraction_path = file.path.replace(".pbit", "")
            if os.path.exists(extraction_path):
                shutil.rmtree(extraction_path)
            os.mkdir(extraction_path)

            print("Extracting zip file ...")
            with zipfile.ZipFile(zip_path, "r") as zip_file:
                zip_file.extractall(extraction_path)
            print("Zip file extracted")

            #### changing extensions
            print("Changing extensions ...")
            data_model_path = os.path.join(extraction_path, "DataModelSchema")
            os.rename(data_model_path, data_model_path + ".json")

            layout_path = os.path.join(extraction_path, "Report/Layout")
            os.rename(layout_path, layout_path + ".json")
            print("Extensions changed")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
        pbit_manipulation(folder_path)
    else:
        print(
            "You have to pass as argument the folder where the pbit files are stored!"
        )
