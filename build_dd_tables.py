# -*- coding utf-8 -*-

"""
By : Real Limoges
Last Updated : 5/11/15

This file builds the tables for the data description paper

"""

#Standard Libraries
import os
import pandas as pd
import xlsxwriter

#User Made Modules
import global_vars

def gp_loc_perc(workbook):
	#Creates a table that shows a pivot of GP by location over time (decades)

	title = 'Table 1: General Partners by Location of Company Headquarters'

	#Basic cleaning of GP data
	df = pd.read_csv(os.path.join(OPEN_PATH, 'gp_view.csv'), header = 0)
	df = df[["YEAR_FOUNDED", "REGION_ID", "COUNTRY_ID"]]
	df = df.dropna()
	df = df[df.YEAR_FOUNDED >= 1980]
	df = df[df.REGION_ID != "ANTARCTICA"]

	#Separates UNITED STATES from North America
	df.ix[df.COUNTRY_ID == "UNITED STATES", "REGION_ID"] = "UNITED STATES"

	df = pd.crosstab(df.REGION_ID, [df.YEAR_FOUNDED], rownames = ["REGION_ID"],
					 colnames = ["YEAR_FOUNDED"])

	df = transform_to_decades(df)
	df["Total"] = df.sum(axis = 1)
	df = convert_columns_to_perc(df)
	df = convert_index_to_col(df, "REGIONS")

	df["REGIONS"].replace(global_vars.region_replace, inplace = True)

def transform_to_decades(df):
	#Converts dataframe from having years as columns

	decades = ["1980-89", "1990-99", "2000-09", "2010-Present"]
	col_list = [range(1980,1990), range(1990,2000), range(2000,2010),
				range(2010,2015)]

	#Cleans columns to string variables
	columns = df.columns.tolist()
	columns = [str(x)[:-4] for x in columns]
	df.columns = columns

	for col in range(len(col_list)):
		col_list[col] = map(str, col_list[col])

	#Sums up each of the columns in a range
	for decade, col in zip(decades, col_list):
		set_col = set(col)
		set_df = set(df.columns.values)
		intersection = set_col.intersection(set_df)
		intersection = list(intersection)
		df[decade] = df[intersection].sum(axis = 1)

	#Drops the original columns
	for col in flatten(col_list):
		year = str(col)
		if year in df.columns.values:
			df = df.drop(year, axis = 1)

	return df

def convert_columns_to_perc(df):
	#Loops through all columns in the datarame and converts into percentages

	for item in df.columns.tolist()
		df[item] = df[item] / df[item].sum(axis = 1)

	return df

def convert_index_to_col(df, index_name):
	#Converts the dataframe index into a column; places as first column in dataframe

	df[index_name] = df.index
	cols = df.columns.tolist()
	cols = cols[-1:] + cols[:-1]
	df = df[cols]

	return df

def main():

	workbook = xlsxwriter.Workbook(os.path.join(SAVE_PATH, OUTFILE))
	gp_loc_perc(workbook)

