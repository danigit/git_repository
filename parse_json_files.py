"""
    # This file parse the json files DataModel and Layout, and extracts
    # the tables, measures and columns that are used in each page of the
    # Power BI file    
"""

# importing libraries
import re
import json
import os
import sys


# defining the regex
PAGE_NAME_REGEX = r'"displayName"\s*:\s*"([^"]*)'
TABLE_NAME_REGEX = r'Entity[^:]+:[^"]"([^\\"|^"]+)'
COLUMN_OR_MEASURE_NAME_REGEX = r'Property[^:]+:[^"]"([^(\\"|")]+)'


#### TODO - here there is a problem, the json files are saved as a single line string
####        and it is also malformed, so we cannot parse it as a json objec
####        the problem is that if we run the regex on a single line string we cannot
####        separate the elements from the single pages, so firs I have to format it
####        I have to find a better way of doing this without opening the file three times
####        If I read and write in the same scope the problem is that it would be saved as
####        utf-16-le which is not ok
def parsing_layot_file(file_path="", file_name="Layout.json"):
    """
    Function that parses the Layout.json file and produces a file which has
    for each page inside the report, which tables, columns and measures are used
    Args:
        file_path (str, optional): The path where the Layout.json file is situated. Defaults to "".
        file_name (str, optional): The file name to be parsed. Defaults to "Layout.json".
    """
    
    if not isinstance(file_path, str) or file_path == "":
        print("Path not valid")

    # formating the json file
    data_model_path = os.path.join(file_path, file_name)
    with open(data_model_path, "r") as file:  # , encoding="UTF-16-le") as file:
        file_json = json.load(file)
        formated_json = json.dumps(file_json, indent=2)

    # saving the formated file
    with open(data_model_path, "w") as file:
        file.truncate(0)
        file.write(formated_json)

    search_result = [{"page_name": "All pages", "table_name": [], "column_name": []}]
    page_number = 0

    # finding the elements in the file
    with open(data_model_path, "r") as file:
        for line in file:
            #### searching for pages
            page_regex = re.search(PAGE_NAME_REGEX, line)
            if page_regex:
                search_result.append(
                    {"page_name": page_regex.group(1), "tables": [], "columns": []}
                )
                page_number += 1

            #### searching for tables
            table_regex = re.findall(TABLE_NAME_REGEX, line)
            if table_regex:
                #### controlling if I already find a page, if not it means that I found the columns
                #### and measures that are applied as filters to all pages
                for match in table_regex:
                    search_result[page_number]["tables"].append({"table_name": match})

            #### searching for columns and measures
            column_or_measure_regex = re.findall(COLUMN_OR_MEASURE_NAME_REGEX, line)
            if column_or_measure_regex:
                for match in column_or_measure_regex:
                    search_result[page_number]["tables"].append({"column_name": match})

        #### saving the result to a file
        #### TODO - remove the duplicates tables and columns that are in the same page
        output_data_path = file_path + "/mapping.json"
        with open(output_data_path, "w") as file:
            file.write(json.dumps(search_result))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        parsing_layot_file(
            file_path,
        )
    else:
        print(
            "You have to pass as argument the folder where the pbit files are stored!"
        )
