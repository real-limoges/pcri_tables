# -*- coding utf-8 -*-

"""
By : Real Limoges
Last Updated : 5/11/15

This file builds the rollup for the main PCRI database

"""

#Standard Libraries
import os
import pandas as pd
import xlsxwriter

#User Made Modules
import global_vars
from write_out_data import basic_write_out

#Global Variables
comma_style = 0x03
OUTFILE = "Dashboard.xlsx"
OPEN_PATH = global_vars.OPEN_PATH
SAVE_PATH = global_vars.SAVE_PATH

def exit_type_id(workbook):
	#Creates a table that shows the distribution of exit_type_id

	title = 'Distribution of Exit Type ID'

	#Cleans the data
	df = pd.read_csv(os.path.join(OPEN_PATH, 'exit_view.csv'), header = 0)
	df['Count'] = 1
	df = df.groupby(['EXIT_TYPE_ID'])
	df = df.agg({'Count':'sum'})

	df = convert_index_to_col.create(df, "Exit Types")
	width = {'index': 25, 'other': 15}

	basic_write_out(df, title, workbook, width = width, cell_style = comma_style)

def investment_category(workbook):
	#Creates a table that shows the distribution of investment_type

	title = 'Distribution of Investment Type'

	#Cleans the data
	df = pd.read_csv(os.path.join(OPEN_PATH, 'investment_view.csv'), header = 0)
	df['Count'] = 1

	df = df.groupby(['INVESTMENT_TYPE'])
	df = df.agg({'Count':'sum'})

	df = convert_index_to_col(df, "Investment Types")
	width = {'index': 30, 'other': 15}

	basic_write_out(df, title, workbook, width = width, cell_style = comma_style)

def convert_index_to_col(df, index_name):
	#Converts the dataframe index into a column; places as first column in dataframe

	df[index_name] = df.index
	cols = df.columns.tolist()
	cols = cols[-1:] + cols[:-1]
	df = df[cols]

	return df

def main():
	workbook = xlsxwriter.Workbook(os.path.join(SAVE_PATH, OUTFILE))
	exit_type_id(workbook)
	investment_category(workbook)

if __name__ == '__main__':
	main()
