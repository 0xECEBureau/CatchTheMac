sqlite3 Manifest.db

SQLite version 3.40.1 2022-12-28 14:03:47
Enter ".help" for usage hints.
sqlite> .tables
Files       Properties

sqlite> SELECT * FROM Files WHERE fileID LIKE '%message%'
   ...> OR domain LIKE '%message%'
   ...> OR relativePath LIKE '%message%';

e69dcd03e0f1c75c1d4837428b8842b74262653b|HomeDomain|Library/MessagesMetaData|2|bplist00
