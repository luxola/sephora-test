# Data Warehouse Architect Position at Sephora SEA

You can write your code in the language of your choice. But we have preferences for the language of our stack:

- Go (Highly recommended)
- Python
- NodeJS

Please organise your code, document it and write relevant unit tests.
Please also inform on any specific setup which is required to make your code run.

## Context

At Sephora SEA, we are building business schemas on top of the e-commerce databases.
For instance, we have a __products__ table which is a consolidation of 30 other tables.
It contains information for each of our products (ids, descriptions, categories...).

Our tables are organised in datasets (folders), _eg._ `final`, `raw`, `tmp`.

The __products__ table is created from a chain of dependent SQL scripts. The process is as follows:

1. Dump the e-commerce databases into a raw dataset (`raw` folder)
2. Clean and consolidate the data on top of these raw tables using SQL scripts stored in the `tmp` folder. For instance, the result of the `tmp/inventory_items.sql` script will be stored in the `tmp.inventory_items` table.
3. Create the `final.products` table (from the `final/products.sql` script)

## Your task

Your task is to build parts of the tool that will orchestrate the aforementioned process, in order to create the `final.products` table:

1. Write a function that shows the dependencies between all the sql scripts (from scratch, no specialized library!) _eg._ showing that `tmp/item_purchase_prices.sql` depends on `raw.purchase_line_items` and `raw.purchase_items`.
We are expecting some kind of simple visualization (graph, tree, ...) 

2. Write a function that, using the previous question, runs the sql scripts in the correct order. Please provide documentation as of how you are proceeding.

*Going further, we would like to parallelize the execution of few of these scripts. If you think of the dependencies as a tree: scripts from different nodes can work simultaneously, but, still, must not be executed before its children's tasks are done.*

3. Write a function that paralellizes the execution of the SQL scripts, ensuring they respect their dependencies. Please provide documentation as of how you are proceeding.



## Notes


*The files in the `raw` folder represents the available raw data tables in the `raw` dataset.


*For point 1, parsing the query will be necessary. We can assume the shape of the tables in the scripts will always be `dataset_name.table_name`

*Your code should be flexible enough so that it will still work properly if more scripts are added in any folder


*You can use the following dummy function as a placeholder for the function actually running the sql scripts (in go):

```go
func() {
 // This is execution time of the tmp.inventory_items script
 time.Sleep(time.Second * 3)
}
```
 
