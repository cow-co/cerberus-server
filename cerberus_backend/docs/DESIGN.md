# Overall Design

## Data Objects

We use two types of data object: data access objects (DAOs) and data transfer objects (DTOs)

DAOs represent what is in the database, and the code related to them handles all the database operations (querying, inserting, updating, deleting).
The important principle is that the database-handling code should be as isolated as possible, with as little knowledge of database innards leaking out as possible. This means that DAOs are transformed to/from DTOs as soon as we can. The reasons are:

- There's a lot of DB-related concepts that the DAOs embody which are simply not relevant in the rest of the code (foreign keys, for example).
- This allows us to sanitise information (eg. passwords) as soon as possible. When reading user accounts out of the database, only the DAO needs to "know" that they have a password; as soon as we leave the DB area of the code, that knowledge is deliberately lost.

Meanwhile, DTOs represent what the rest of the system should know about the entities. Different DTOs can be used for requests and responses, in cases where certain fields (notably: IDs and passwords) are relevant in one but not the other.

## Three-Tier Structure

