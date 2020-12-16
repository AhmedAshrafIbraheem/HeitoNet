# HeitoNet

## Design Diagram

* ### First Query (MongoDB) 

=> *Given a disease id, what is its name, what are drug names that can treat or palliate this disease, what are gene names that cause this disease, and where this disease occurs? Obtain and output this information in a single query.*

Collection Names [{“_id”: “node_id”, “name”: “node_name”} ...]

Collection Diseases [{“_id”: “disease_id”, “name”: “disease_name”, “Drugs” : [], “Genes” : [], “Anatomy”: []} ...]

MongoDB provides an index upon the “_id” attribute. So searching for Diseases by their ID will be fast. And since we are storing all the data needed into the document of each disease, so only one document will be fetched containing all the data required.
By the way, we didn’t store all the data. For example, there are lots of edges that have no effect on our query. So we just disregard those edges. 



* ### Second Query (Neo4j)

=> *We assume that a compound can treat a disease if the compound or its resembled compound up-regulates/down-regulates a gene, but the location down-regulates/up-regulates the gene in an opposite direction where the disease occurs. Find all compounds that can treat a new disease name (i.e. the missing edges between compound and disease excluding existing drugs). Obtain and output all drugs in a single query.*

Nodes have one label from (Anatomy, Gene, Compound, Disease) and two properties (id and name).
Relations have one label from ('CrC', 'CuG', 'CdG', 'CtD', 'CpD', 'AdG', 'AuG', 'DlA') and no properties. Other edges are disregarded.
The way the design looks is the same as the given diagram.

```
- CREATE CONSTRAINT ON (n: Anatomy) ASSERT n.id IS UNIQUE
- CREATE CONSTRAINT ON (n: Gene) ASSERT n.id IS UNIQUE
- CREATE CONSTRAINT ON (n: Disease) ASSERT n.id IS UNIQUE
- CREATE CONSTRAINT ON (n: Anatomy) ASSERT n.id IS UNIQUE
- CREATE INDEX FOR (n:Disease) ON (n.name)
```

-- Used constraint as not to count the node more than once while loading new edges, also it makes matching Nodes by their ids much faster as constraint adds index.

-- Used index on Disease name to increase the speed of Query2.


## Queries Supported

**Add1 [nodes.tsv] [edges.tsv]**

* Used for loading data into MongoDB database. By the way, never add data before deleting existing data


**Add2 [nodes.tsv] [edges.tsv]**

* Used for loading data into Neo4j database. Since we used ‘LOAD CSV’ a copy of the files are needed to be placed into the import folder for Neo4j.  By the way, never add data before deleting existing data


**Delete1**

* Delete all data in MongoDB database


**Delete2**

* Delete all data in Neo4j database


**Q1 [Disease_id]**

* Execute Query 1


**Q2 [Disease_name]**

* Execute Query 2

**Printer1** (Debugging and Testing Purpose)

* Fetch all data in MongoDB database and print it


**Printer2** (Debugging and Testing  Purpose)

* Fetch all data in Neo4j database and print it

**Exit**

* To terminate the application


