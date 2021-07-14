Installation instructions:
1. download and install Python anaconda package for 2.7 version
2. copy the excel and .py code into same location
3. open file and update values in green then press 'Calculate'

Excel to web template transformation rules"
1. Tabs 'Main' and 'data rates' would need to be transformed into a web pages
2. User would be required to register with the website to gain access to the 
main calculation section (information from tabs Main and data rates)
3. Back-end calculation code 'CalculatingYield.py' would need to be kept in 
python. This code is run whenever user clicks 'Calculate'
4. After user logs into the website, they would see several input tabs from
'Main' tab (i. - iii.). The user should see a default excample, similar to as
seen after opening the excel file.
5. 'data estimates' is maintained by owner of website in a postgres database. The
user will have functionality to adjust these curves (already part of the code),
by changing 'LOSS MULTIPLIER' and 'PREPAY MULTIPLIER' on tab 'data rates'. The
default values are set at 1, if the user changes the value to 1.2 than means that
values in 'data estimates' tab will be multiplied by 1.2. This is done in the
python code. 

Tab Descriptions
1. 'Main' - 5 tables
	(i). User input table - fields highlighted green should be input 
	fields entered by user.
		a. Term is a drop down reference from 'data rates' tab field called 'Term'
		b. Grade is a drop down reference from 'data rates' tab field called 'Grade'
		c. Recovery Rate is a manually typed field by user
	(ii.) User input table - fields highlighted green should be input 
	fields entered by user.
		a.-f. all fields are manually entered by user
	(iii. - vi.) All tables are output tables that get updated values after
	user clicks 'Calculate'. All the graphs below the tables should be 
	displayed to the user in a form of a dashboard.
2. 'data rates' - All values in this table are manual inputs from user, there
should be a choice for them to enter values for each individual row. Then that 
row will be written into a table in a database. User should also have a choice
to import this data as a csv.
3. 'data estimates' - This tab is a backend table in the database (postgres database) that will be 
updated by the owner of the website 
4. 'Portfolio' - disregard this tab for now
	
	
	 
