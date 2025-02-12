
These Notes are directly connected to the ![[DTalks-DataEng-Data Warehouse.pdf]]

**OLTP vs OLAP:**

* OLTP is usually used in backend services where you want to group a couple of SQL queries together and you want to fall/roll back if one of them fails
* OLAP is used for putting a lot of data in and discovering insights. Mainly used for analytical purposes by data analysts/scientists.

**What is a Data Warehouse?**

>It is an OLAP solution used for reporting and data analysis.

Consists of:
* Raw Data
* Meta Data
* Summary

BigQuery Additional Info:
* Generally can start a warehouse with GBs of data and scale to PBs without any issues.
* Can use Partitioning (Partition tables for example by date) to run faster queries and load less data every time. For partitioning you can choose between:
	* Time-unit column
	* Ingestion time (_PARTITIONTIME)
	* Integer range partitioning
* Can use Clustering to improve our cost and query performance as well.
* Partitioning and Clustering can be used together and can reduce the amount of processed data even more.

**Partitioning:**
> can choose between:
* Time-unit column
* Ingestion time (_PARTITIONTIME)
* Integer range partitioning
*Maximum number of partition limit is 4000

> For time-unit or ingestion time can choose from:
* Daily
* Hourly -> If you have a huge amount of data and want to process based on hour (Should consider the maximum partition limit - Expire Partitioning Strategy)
* Monthly or Yearly

**Clustering**
* All info supplied in the slides.
 
>[!Warning]
>If data size < 1GB Partitioniing and Clustering may not improve performance but add additional cost because they incur metadate reads and metadata maintenance. Might make more sense to not use them in these cases.


**BigQuery Internals:**

* Stores our data into a separate storage called 'Colossus'
	* Colossus stores data in a columnar format and is generally cheap storage
	* Big advantage because compute is separated from storage and has significantly less cost
* The most costly part while reading data or running queries (Essentially compute)
> How do these two communicate?
* Jupiter Network used inside BigQuery datacenters and provides ~1TB/s network speed
* This allows compute and storage to be in separate hardware and can communicate without delays over Jupiter Network

>Dremel is the Query Execution engine.
* Divides your query into tree structure and separates it such that each node can execute an individual subset of the query.
* Leaf nodes are the ones that actually query and talk to the Colossus database - Fetch data, execute appropriate operations, and return data back to mixers, and then return to root servers, then aggregated and returned to the results.
* The distribution of workers is what makes BigQuery so fast.
![[DremelServingTree-Example.png]]



>Two type of storage:
* Record-oriented
	* Similar to structures like CSV
	* Easy to process and understand
* Column-oriented
	* Used by BigQuery
	* Provides better aggregations