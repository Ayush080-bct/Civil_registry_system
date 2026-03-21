### About Normalization
 
- 1NF -> every column has atomic values, no repeating groups
        i.e all columns are single values
- 2NF -> no partial dependency
       i.e all primary keys are single column Auto_increment 
- 3NF  -> no transitive dependency
        i.e province is in District, not in Person
          profession_name is in Profession, not in Employment
          municipality is in Address, not in Person


