
### Processing data types:
#### Batch:
You have data and you process it and create a new database for example. Most jobs are batch jobs.

**Advantages:**
* Easy to manage
* Can be re-executed if a problem occurs
* Easier to scale
**Disadvantages:**
* Delay (Caused by individual scripts/steps)
#### Streaming:
The processing happens in real-time with data coming and being processed at the same time

### Batch Jobs

* Weekly
* **Daily**
* **Hourly**
* 3 Times per hour
* Every 5 minutes

Technologies:
* Python Scripts
* SQL
* Spark
* Flink

A common workflow could be:
We can orchestrate this using Airflow for example or Kestra.

![[BatchJobWorkflowExample.png]]
