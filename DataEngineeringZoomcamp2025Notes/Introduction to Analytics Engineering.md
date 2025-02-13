![[DataTeamRoles.png]]

![[DataTooling.png]]

### Data Modelling Concepts

![[ETLvsELT.png]]

#### <ins>Kimball's Dimensional Modelling</ins>

>Objective:
* Deliver data understandable to the business users
* Deliver fast query performance

>Approach:
> Prioritize user understandability and query performance over non redundant data (Third Normal Form - 3NF)

>Other Approaches:
* Bill Inmon
* Data vault

### Elements of Dimensional Modeling

>[!Info]
>This is know as a star schema

![[StarSchema.png]]



> Facts Tables
*  Measurements, metrics or facts
* Corresponds to a business process
* "verbs"

> Dimension Tables
* Corresponds to a business entity
* Provides context to a business process
* "nouns"

#### Architecture of Dimensional Modelling
##### The Restaurant Analogy

Stage Area -> The Food (Raw Data)
Processing Area -> The Kitchen - The cooks will take the data and cook it (or make data models)
Presentation Area -> The Dining room

![[ArchitectureOfDimModelling.png]]
