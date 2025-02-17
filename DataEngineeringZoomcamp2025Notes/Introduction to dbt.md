>[!Info]
>dbt (Data build tool) is a transformation workflow that allows anyone that knows SQL to deploy analytics code following software engineering practices like modularity, portability, CI/CD, and documentation

![[DbtFlow.png]]

>How does it work?

![[HowDBTworks.png]]

* Selects the data transforms it and persists it back to data warehouse.

> How to use dbt?

![[HowtouseDBT.png]]


> Anatomy of a dbt model
* dbt models are SQL files
* We define a config with the materialization strategy
	* Table
	* View (Default)
	* Incremental
	* Ephemeral - Similar to a CTE

![[dbtAnatomyExample.png]]
![[dbtMaterializationStrategies.png]]

![[dbtFROMclause.png]]
![[dbtREFmacro.png]]

#### Macros

* Use control structures (e.g. if statements and for loops) in SQL
* User environment variables in your dbt project for production deployments
* Operate on the results of one query to generate another query
* Abstract snippets of SQL into reusable macros - These are analogous to functions in most programming languages

![[dbtMacroExamples.png]]

#### Packages

* Like libraries in other programming languages
* Standalone dbt projects, with models and macros that tackle a specific problem area.
* By adding a package to your project, the package's models and macros will become part of you own project
* Imported in packages.yml file and imported by running `dbt deps`
* A list of useful packages can be found in [dbt - Package hub](https://hub.getdbt.com/)

![[dbt_packages.png]]

#### Variables (Similar to programming variables)
* Useful for defining values that should be use across the project
* With a macro, dbt allows us to provide data to models for compilation
* To use a variable we use the `{{var('...')}}` function
* Variables can be defined in two ways:
	* In the dbt_project.yml file
	* On the command line

![[dbt_variables.png]]

#### Tests
* Assumptions that we make about our data
* Tests in dbt are essentially a `select` sql query
* These assumptions get compiled to sql that returns the amount of failing records
* Tests are defined on a column in the .yml file
* dbt provides basic tests to check if the column values are:
	* Unique
	* Not null
	* Accepted Values
	* A foreign key to another table
* You can create custom tests and queries

![[dbt_Tests.png]]

#### Documentation
![[dbt_Documentation.png]]

#### Deployment
![[dbt_Deployment.png]]

##### Running a dbt project in production
![[dbt_ProjectInProduction.png]]

##### What is Continuous Integration (CI)?
![[dbt_ContinuousIntegration.png]]

