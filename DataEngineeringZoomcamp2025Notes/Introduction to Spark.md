
>[!Definition]
>Spark is a Data Processing Engine.
>Spark pulls data to its executors, processes it and outputs it again to a data lake or data warehouse.
>Processing happens in Spark (Because it is an engine).
>Normally used for Batch processing but can also be used for streaming.

>**When to use Spark:**
>Used when your data is used in a Data Lake (S3 or GCS). Spark typically would pull the data from the data lake, process and it put it back in the data lake.
>Alexey recommends that if you can express something with SQL you should go with that (using Athena or Presto) and if you cannot (Too complicated) you can go with Spark.


# Spark SQL and Dataframes

Better to have a bunch of smaller files when processing them in the Spark Cluster since the Executors can pick up those smaller files instead of being idle until a single executor processes one large file.

![[SparkInternals-ExecutorsandFiles.png]]

## Actions vs Transformations
### Transformations:
> This are not executed right away (Lazy)
* Selecting Columns
* Filtering
* Joins
* Group by
* ...

### Actions:
> These are executed right away (Eager)
* Show() is an action for example
* .take()
* .head()
* Write commands
* ...


## Spark Internals

### Spark Cluster
`.master("local[*]")` Creates a local cluster on the machine

>[!Way it works]
>* Create a script in Python, Scala etc. in a driver (Local or Airflow Operator or other)
>* Driver submits the script to the Spark Master (WebUi usually port 4040)
>* The master coordinates between the executors and what they will execute
>* Executors generally pull and process the data - For example each executor pulls a partition from a DF and complete a certain task.
>* This DFs usually live in S3 or GCS buckets.

![[SparkInternals_Cluster.png]]

### GroupBy in Spark

>[! How it works]
>* If we have partitions, each executor is grouping by within a specific partition.
>* **Stage 1:** For each partition we have temporary files called `Intermediate Results`
>* **Stage 2:** Results are combined in a process called `Reshuffling`  using a process called `External Merge Sort`
>* Reshuffling can be seen as `Exchange` in Spark.
>* Usually we want to reshuffle as little data as possible since it is an expensive operation


![[SparkInternals_GroupBy_Stage1.png]]

![[SparkInternals_GroupBy_Stage2.png]]


### Joins in Spark

>[! How it works]
> * For each record we create complex records (Key, Record e.g. (K1,Y1))
> * Then similar to the GROUP BY we reshuffle such that same Keys go to the same partition
> * Lastly records in these partitions are joined into one record.
> * If it is an inner join records with Nulls will not be outputed.

![[SparkInternals_Joins.png]]

>[!Info]
 >This is the case when we have 2 relatively large tables.
> If one table is large and the other is small, each executor gets a copy of the small DF (In other words the DF is broadcasted) and no reshuffling is needed.

![[SparkInternals_BroadcastJoin.png]]

