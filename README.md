# Bank-Receipt-PDF-parser
Banks Receipt PDF Parser using Python - automatically parses pdf and saves data into the SQL database
===========================================================================================================

Dependencies: 	1) pdfminer library (github)
		            2) sqlite3

This is a pdf parser, which is designed to parser specific type of transaction receipts of ZaubaCorp Technologies.
It deigned using python 2.7 using spyder IDE.

This uses a pdf2txt.py file, which comes with the pdfminer library to directly convert pdf file to text file.
Then that text file is stripped of all new line characters to reduce complexity and make the text file generic.
Then the code in source.py will parse these reduced text files for useful data.
It simultaneously establishes a connection to the SQLite  and creates a database named "Transaction_details.db" and stores all the useful data in a table named "Transactions". 

It also takes care of redundancy of data because SQL query makes the receipt number or SRN number as the PRIMARY KEY, and before saving any data, it checks for duplicacy using that primary key.


Procedure to run the code :-
--------------------------

1) Download the zip file 
2) Extract the zip file to any loaction on the system.
3) System must have python 2.7 or above installed with sqlite3 library.
4) Copy all the pdf files which needs to be parsed into the current folder (sample pdf files already added)
5) Open the terminal (linux) or command prompt (windows) and set the folder which contains 'source.py' file, as working directory.
6) Type following command with space separated names of the pdf files which needs to be parsed (make sure that same pdfs are placed in set working directory)
	= "python source.py file1.pdf file2.pdf file3.pdf " without ("") quotes and press enter.
	
	eg: python source.py U16571275.pdf U16572745.pdf U16573131.pdf
7) This will create a database "Transaction_details.db" in the working directory with all the details of parsed pdfs.
