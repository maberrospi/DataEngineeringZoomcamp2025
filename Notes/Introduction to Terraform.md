>[!DEFINITION]
>HashiCorp Terraform is an infrastructure as code tool that lets you define both cloud and on-prem resources in human-readable configuration files that you can version, reuse and share. You can then use a consistent workflow to provision and manage all of your infrastructure throughout its lifecycle.

>[!INFO]
>What it actually does:
> You take a cloud platform (or local) and set up infrastructure where your code can live and infrastructure run


**Why Terraform?**

* Simplicity in keeping track of infrastructure
* Easier collaboration (Sort of like Git)
* Reproducibility -> You build a dev env (terraform file) and you can recreate it easily
* Ensure resources are removed -> Remove all of the test resources that aren't needed simply

**What Terraform is NOT:**
* Does not manage and update code and infrastructure
* Does not give you the ability to change immutable resources (like VM type)
* Not used to manage resources not defines in your terraform files

**What is Terraform?**
*INFRASTRUCTURE AS CODE*

Diagram of how it works:![[TerraformDiagram.png]]

Define the provider in the terraform file and terraform will pull that provider and use it.

>What are providers?
>Code that allows terraform to communicate to manage resources

Possible choices:
* AWS
* Azure
* GCP
* Kubernetes
* VSphere
* Alibaba Cloud
* Oracle Cloud Infrastructure
* Active Directory

>Key Terraform commands:

* Init - *Get me the providers I need*. Get the provider code to the local machie
* Plan - *What am I about to do?* Shows the resources that will be created
* Apply - *Do what is in the tf files*
* Destroy - Remove everything defined in the tf files.


# Terraform Overview

[Video](https://www.youtube.com/watch?v=18jIzE41fJ4&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=2)

### Concepts

#### Introduction

1. What is [Terraform](https://www.terraform.io)?
   * open-source tool by [HashiCorp](https://www.hashicorp.com), used for provisioning infrastructure resources
   * supports DevOps best practices for change management
   * Managing configuration files in source control to maintain an ideal provisioning state 
     for testing and production environments
2. What is IaC?
   * Infrastructure-as-Code
   * build, change, and manage your infrastructure in a safe, consistent, and repeatable way 
     by defining resource configurations that you can version, reuse, and share.
3. Some advantages
   * Infrastructure lifecycle management
   * Version control commits
   * Very useful for stack-based deployments, and with cloud providers such as AWS, GCP, Azure, K8S…
   * State-based approach to track resource changes throughout deployments


#### Files

* `main.tf`
* `variables.tf`
* Optional: `resources.tf`, `output.tf`
* `.tfstate`

#### Declarations
* `terraform`: configure basic Terraform settings to provision your infrastructure
   * `required_version`: minimum Terraform version to apply to your configuration
   * `backend`: stores Terraform's "state" snapshots, to map real-world resources to your configuration.
      * `local`: stores state file locally as `terraform.tfstate`
   * `required_providers`: specifies the providers required by the current module
* `provider`:
   * adds a set of resource types and/or data sources that Terraform can manage
   * The Terraform Registry is the main directory of publicly available providers from most major infrastructure platforms.
* `resource`
  * blocks to define components of your infrastructure
  * Project modules/resources: google_storage_bucket, google_bigquery_dataset, google_bigquery_table
* `variable` & `locals`
  * runtime arguments and constants


#### Execution steps
4. `terraform init`: 
    * Initializes & configures the backend, installs plugins/providers, & checks out an existing configuration from a version control 
5. `terraform plan`:
    * Matches/previews local changes against a remote state, and proposes an Execution Plan.
6. `terraform apply`: 
    * Asks for approval to the proposed plan, and applies changes to cloud
7. `terraform destroy`
    * Removes your stack from the Cloud


### References
https://learn.hashicorp.com/collections/terraform/gcp-get-started