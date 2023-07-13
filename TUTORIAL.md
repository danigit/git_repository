<img src="./img/logo.png" width=300>


</br>
</br>
</br>


## Step 1 - Download the Power BI file 

</br>

### From terminal using `curl'

</br>

Open a terminal window, go in the folder where you want to download the file, and paste the following command: 
```
curl -o power_bi_inspector.pbix https://github.com/danigit/power_bi_inspector/blob/master/power_bi_inspector.pbix
```

</br>

### From GitHub

</br>

Go to the following GitHub page https://github.com/danigit/power_bi_inspector/blob/master/power_bi_inspector.pbix and click on `View raw` and the file will start downloading.

<img src="./img/raw_data.png">

</br>

## Step 2 - Create configuration file

</br>

Create a json configuration file in a directory you choose and paste inside the following:

```
[
    {"param_name": "pbit_path", "param_value":"path\to\the\pbix\file\that\you\want\to\inspect"},
    {"param_name": "pbit_file_name", "param_value": "<name_of_the_file>"}
]
```

Remember to change the `path\to\the\pbix\file\that\you\want\to\inspect` with the path where your `.pbix` file is, and the `<name_of_the_file>` with the actual name of the file you wanto to inspect.

</br>

## Step 3 - Set up the variables

</br>

In the `power_bi_inspector.pbix` file which you open in Power BI go to Power Query Editor, on the left you find a parameter called `config_path`. Set the value of this parameter with the path where the config file which you created above is saved. The click on the `Close & Apply` button to close save and close Power Query Editor.

<img src="./img/config_path.png">

</br>

## Step 4 - Load the data

</br>

Now refresh first the `JSON_DATA` table by right clicking on it and selection `Resfres data`, then refresh the `TABLES_AND_COLUMNS` table.

<img src="./img/refresh.png">

</br>

## Step 5 - Inspect your file

</br>

Done you can now inspect the loaded file and see where your tables, columns and measures are used.

<img src="./img/full_page.png">

## Load another file

</br>

To load another file for the inspection all you have to do is to change the path and name of the file in the config file, and then load again the tables (Step 4).