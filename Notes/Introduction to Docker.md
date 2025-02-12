Delivers software in packages called containers and the containers are isolated.

Advantages 
* Can have multiple containers with different tools.
	* For example we can have a container with Ubuntu,Python,Pandas etc. and another container with Postgress for our database.
* Reproducibility because the docker images are identical
* Local experiments
* Integration Tests (CI/CD)
* Running pipelines on the cloud (AWS Batch, Kubernetes jobs)
* Spark - Can specify the dependencies in Spark with docker.
* Serverless - Define environment as docker image (AWS Lambda)

Example docker images/containers:
![[Pasted image 20250203163130.png]]

