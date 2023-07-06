<img src="./img/logo.png" width=300>


</br>
</br>
</br>


# Why this project?

As a Power BI developer I found my self in truble when I had to change a measure in a very large project. Why? Because I lost track of where that measre is used, so I'm not sure if I can modify it without breaking something. Anoter problem was when I lost track of which measures are actually used and which I can instead delete because are not usefull anymore. 

Unfortunately all the tools that I found are not helping me in solving this problem, so I decided to give it a try and create one my self.

# What aspires to be this project?

The initial goal is to create a Power BI dasboard which shows in a visual and immediate whay where each measure/column/table is used inside a Power BI report. 

# How I plan to do it?

After reading about how the Power BI files are structured, I found out that all the information that is needed to solve my problem it can be recovered from parsing the file itself.

# Firs use case

I have a Power BI file called `use_case.pbix` and I would like to know for each measure, column and table in which page is used. 

## Algorithm 

1. Export the `use_case.pbix` file as a Power BI template file (`.pbit` extension)
2. Convert the `.pbix` file in a `.zip` file
3. Change the extension of the `DataModelSchema` and `Layout` files to `.json`
4. Parse the `DataModelSchema.json` file to get all the measures, columns and tables that are used inside the file
5. Parese the `Layout.json` file to get informations about what measures, columns and tables are used in which pages
