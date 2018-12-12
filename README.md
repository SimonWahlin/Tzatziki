# Tzatziki - Simple xml file appending tool

This project sets out to create a program that automatically appends an .xml file used by Google GCDS, using data exported from an LDAP server. GCDS will use this info to create OU structure, and ultimately as a search scope to include users for import to G Suite.

As time moves on, more attribute values are created on the LDAP server. These new values may be missing in the .xml file and thus users are not imported. This algorithm presumes that new values have already been fetched from LDAP and formatted in to a text file, stored locally. 

* Workflow:
 
1. Data gets exported from LDAP server periodically.
2. Code runs to determine whether the .xml file needs to update to include all data from LDAP
3. If data differs from export and the containments in the .xml file, the program will add to the .xml file with new custom-built elements for every differing data.

* Todo's:

1. Break apart main.py to separate modules using classes
2. Prettify output data written to .xml file. (right now its all a massive one-liner. Not pretty.) 
3. Have even more fun !! 
4. Consider including LDAP Query in a separate module to fetch new data
