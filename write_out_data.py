# -*- coding utf-8 -*-

"""
By : Real Limoges
Last Updated : 5/11/15

Writes out data to Excel file

"""

#Global Variables
BEGIN_CHAR = 'A'
BEGIN_NUM = 2

def basic_write_out(df, TITLE, workbook, 
					width = {'index':15, 'other':15}, cell_style=0x0a):
	#Creates and Writes out Workbook to file; default style of cell is percentages

	END_CHAR = chr( ord(BEGIN_CHAR) + len(df.columns) - 1)
	END_NUM = BEGIN_NUM + len(df)

	#Setup worksheet
	worksheet = workbook.add_worksheet()
	worksheet.set_column('%s:%s' %(BEGIN_CHAR, BEGIN_CHAR), width['index'])
	worksheet.set_column('%s:%s' %(char(ord(BEGIN_CHAR) +1), END_CHAR), width['other'])

	#Formats for cells
	formatting = workbook.add_format()
	formatting.set_num_format(cell_style)

	merge_format = workbook.add_format({'align': 'center', 'bold': True,
										'font_size' = 16})


	#Creates Variables to output workbook
	table_dim = '%s%s:%s%s' %(BEGIN_CHAR, str(BEGIN_NUM), END_CHAR, str(END_NUM))
	data = df.values
	columns = [{'header': col, 'format': formatting} for col in df.columns.tolist()]

	#Write Data out
	worksheet.merge_range('%s1:%s1' %(BEGIN_CHAR, END_CHAR), TITLE, merge_format)
	worksheet.add_table(table_dim, {'data': data, 'columns': columns,
									'autofilter': False})