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
TABLE_NAME_REGEX = r'Entity[^:]+:[^"]*"([^\\"|"]+)'
COLUMN_OR_MEASURE_NAME_REGEX = r'Property[^:]+:[^"]*"([^(\\"|")]+)'
VISUAL_TYPE_REGEX = r'visualType[^:]+:[^"]*"([^(\\"|")]+)'

#### TODO - here there is a problem, the json files are saved as a single line string
####        and it is also malformed, so we cannot parse it as a json objec
####        the problem is that if we run the regex on a single line string we cannot
####        separate the elements from the single pages, so firs I have to format it
####        I have to find a better way of doing this without opening the file three times
####        If I read and write in the same scope the problem is that it would be saved as
####        utf-16-le which is not ok

search_result = []


def find_tables_and_columns(data):
    """
        Function that search in the string passed as parameter the tables, columns and
        measures that are present in it. A table is identified by the "Entity" keyword,
        a column and measure is identified by the "Property" keyord.

    Args:
        data (dict): The object in which to search the tables and columns

    Returns:
        array, array: Return two arrays, one containing the tables and the othe containing
        the columns and measures
    """

    tables = []
    columns = []

    #### searching for tables
    table_regex = re.findall(TABLE_NAME_REGEX, str(data))
    if table_regex:
        for match in list(dict.fromkeys(table_regex)):
            tables.append({"table_name": match})

    #### searching for columns and measures
    column_or_measure_regex = re.findall(COLUMN_OR_MEASURE_NAME_REGEX, str(data))
    if column_or_measure_regex:
        for match in list(dict.fromkeys(column_or_measure_regex)):
            columns.append({"column_name": match})

    ## removing duplicates from tables
    if len(tables) == 0:
        tables = list(dict.fromkeys(tables))

    ## removing duplicates from columns
    if len(columns) == 0:
        tables = list(dict.fromkeys(columns))

    return tables, columns


def parse_json_component(component_content):
    """
        Function that parse each component pased as a parameter. A component
        is a visual element present in the page

    Args:
        component_content (dict): The component to be parsed

    Returns:
        dict: A dictionary containing the component tye and the tables and
        columns/measures associated with the component
    """
    visual_type = ""

    ## getting the visual type
    if "config" in component_content:
        visual_type_regex = re.search(
            VISUAL_TYPE_REGEX, str(component_content["config"])
        )
        if visual_type_regex:
            visual_type = visual_type_regex.group(1)

    ## getting the tables and columns associated witht he visual
    tables, columns = find_tables_and_columns(str(component_content))

    return {"visual_type": visual_type, "tables": tables, "columns": columns}


def parse_json_page(page_content, page_number):
    """
        Function that parses the page passed as parameter. The page represents a
        Power BI page and the objective of the function is to find the elements,
        the tables and the columns/measures used in the page

    Args:
        page_content (dict): The page to be parsed
        page_number (int): The page number
    """

    display_name = ""
    tables = []
    columns = []

    if "displayName" in page_content:
        display_name = page_content["displayName"]

    if "filters" in page_content:
        tables, columns = find_tables_and_columns(page_content["filters"])

    if "config" in page_content:
        config_tables, config_columns = find_tables_and_columns(page_content["config"])

        tables.extend(config_tables)
        columns.extend(config_columns)

    if len(tables) == 0:
        tables = list(dict.fromkeys(tables))

    if len(columns) == 0:
        columns = list(dict.fromkeys(tables))

    search_result.append(
        {
            "page_name": display_name,
            "visuals": [
                {"visual_type": "Page filters", "tables": tables, "columns": columns}
            ],
        }
    )

    if "visualContainers" in page_content:
        for index, elem in enumerate(page_content["visualContainers"]):
            visual_info = parse_json_component(elem)
            search_result[page_number]["visuals"].append(visual_info)


def parse_layout_file(file_path="", file_name="Layout.json"):
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
    data_layout_file = os.path.join(file_path, file_name)
    with open(data_layout_file, "r", encoding="UTF-16-LE") as file:
        file_data = file.read()
        json_data = json.loads(file_data)

        if "filters" in json_data:
            all_pages_tables, all_pages_columns = find_tables_and_columns(
                json_data["filters"]
            )
            search_result.append(
                {
                    "page_name": "All pages",
                    "visuals": [
                        {
                            "visual_type": "All pages filters",
                            "tables": all_pages_tables,
                            "columns": all_pages_columns,
                        }
                    ],
                }
            )
        else:
            search_result.append(
                {
                    "page_name": "All pages",
                    "visuals": [
                        {
                            "visual_type": "All Pages filters",
                            "tables": [],
                            "columns": [],
                        }
                    ],
                }
            )

        if "sections" in json_data:
            for index, elem in enumerate(json_data["sections"]):
                parse_json_page(elem, index + 1)

        #### saving the result to a file
        #### TODO - remove the duplicates tables and columns that are in the same page
        output_data_path = file_path + "/mapping.json"
        with open(output_data_path, "w") as file:
            file.write(json.dumps(search_result))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        parse_layout_file(file_path)
    else:
        print(
            "You have to pass as argument the folder where the pbit files are stored!"
        )
