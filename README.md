PCRI Tables
---------------

This repository is the code to build the various tables that PCRI publishes
both in the data description paper, and the rollup that will be place on our
website.

These files are generated as Excel files.


TODO:

 - Remove convert_index_to_col into its own file - try not to repeat/copy/paste code
 - Abstract the design pattern; most of these tables are setup the same. Should be easy to minimize the code
 - Open each dataset once instead of reopening it? Right now each function is designed to represent one table; maybe it should represent each datafile (and then subcompartmentalize from there.) This might be overengineering the whole problem and make my code harder to read
 - Find a more elegant solution instead of the old Stata "gen ones = 1" trick.