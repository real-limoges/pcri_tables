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
from write_out_data import basic_write_out

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

	width = {'index' = 17, 'other' = 17}
	basic_write_out(df, title, workbook, width = width)

def funds_by_investment_type(workbook):
	#Creates a table that shows a pivot of funds by investment type over vintage year
	# in decades

	title = 'Table 2: Breakdown of Funds by Investment Type'

	#Basic Cleaning of Fund Data
	df = pd.read_csv(os.path.join(OPEN_PATH, 'fund_view.csv'), header = 0)
	df = df[["VINTAGE_YEAR", "FUND_TYPE"]]
	df = df.dropna()
	df = df[df.VINTAGE_YEAR >= 1980]
	df = df[df.VINTAGE_YEAR <= 2014]

	df = pd.crosstab(df.FUND_TYPE, [df.VINTAGE_YEAR], rownames = ["FUND_TYPE"],
					 colnames = ["VINTAGE_YEAR"])

	df = transform_to_decades(df)
	df["Total"] = df.sum(axis = 1)
	df = convert_columns_to_perc(df)
	df = convert_index_to_col(df, "Fund Type")

	#Converts Fund Type to more readable format
	df["Fund Type"].replace(global_vars.fund_type_replace, inplace = True)

	basic_write_out(df, title, workbook)

def companies_by_nvca(workbook):
	#Creates a table that shows a pivot of portfolio company by NVCA over year founded

	title = 'Table 3: Companies by Industry, Split by Year Founded'

	#Basic cleaning of Company data
	df = pd.read_csv(os.path.join(OPEN_PATH, 'company_view.csv'), header = 0)
	df = df[["YEAR_FOUNDED", "NVCA"]]
	df = df.dropna()
	df = df[df.YEAR_FOUNDED >= 1980]
	df = df[df.NVCA != "OTHER"]

	df = pd.crosstab(df.NVCA, [df.YEAR_FOUNDED], rownames = ["NVCA"],
					 colnames = ["YEAR_FOUNDED"])

	df = transform_to_decades(df)
	df["Total"] = df.sum(axis = 1)
	df = convert_columns_to_perc(df)
	df = convert_index_to_col(df, "NVCA")

	width = {'index': 20, 'other': 15}
	basic_write_out(df, title, workbook, width = width)

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
	funds_by_investment_type(workbook)

