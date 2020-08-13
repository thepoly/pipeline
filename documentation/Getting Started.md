# Getting Started with Pipeline

**System:** MacOS Mojave 10.14.6

This document serves as an addendum to the 'README.md' file under the root file tree.
**Please note:** Excellent documentation (written from the perspective of a Windows user) is maintained by GitHub user 'JustinM2250' and can be found here: [Learning Journal](https://github.com/thepoly/pipeline/blob/Windows_Learning_Journal/documentation/Windows%20Setup.md) and [Learning DJango Framework](https://github.com/thepoly/pipeline/blob/Windows_Learning_Journal/documentation/Learning%20DJango.md). Even for MacOS users, these documents help provide helpful pieces of information.

## Part 1 ('README.md' -> 'Requirements')
Just like the primary 'README.md' file, install the following:
- [Python 3.7](https://www.python.org) or Python 3.6
- [Pipenv](https://docs.pipenv.org)
- [npm](https://www.npmjs.com/get-npm)
- [Postgres](https://www.postgresql.org)
  - For the Postgres install specifically, make sure to keep the default options checked, and be sure to set your port number to '5432' (should be set by default) and your user name and password to 'postgres'.

## Part 2 ('README.md' -> 'Note about Postgres')
```
brew install postgresql
brew services start postgresql
createdb pipeline
```

After running this command, you might be asked for a password for your desktop username. You'll find that your desktop password fails if this is the case. You'll need to switch your username to 'postgres'.

```
psql -U postgres
```

Enter 'postgres' as your password. The command 'psql' will open the postgres command line. To create the pipeline database from here, you'll need to do:

```
CREATE DATABASE pipeline;
```

Note the ';' (semicolon), this is required syntax for the end of a command in SQL.

To confirm the database has been created, you can run:

```
\l
```

This will show you a list of databases.

To exit this command line, enter:

```
\q
```



