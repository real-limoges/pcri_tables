# -*- coding utf-8 -*-

"""
By : Real Limoges
Last Updated : 5/11/15

This file contains the main function for creating tables for PCRI - for both the
rollup and the Data Description Paper.
"""

#User Made Modules
import build_dd_tables
import build_rollup

def main():

	build_dd_tables.main()
	build_rollup.main()

main()