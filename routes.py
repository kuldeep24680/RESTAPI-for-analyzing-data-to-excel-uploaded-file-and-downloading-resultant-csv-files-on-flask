from app import app
from flask import render_template, request,send_file
import pandas as pd
import csv
import xlrd



# to route the user the upload the .xlsx file
@app.route('/')
def upload_file():
   return render_template('upload.html')

# function that converts the .xlsx file into .csv file and saves it into input folder as test.csv which is used for further analytics 
@app.route('/Fileupload', methods = ['POST'])
def upload():
   if request.method == 'POST':
      f = request.files['file']
      f.save("input/sample.xlsx")
      wb = xlrd.open_workbook('input/sample.xlsx')
      sh = wb.sheet_by_name('Raw Data')
      your_csv_file = open('input/test.csv', 'w')
      wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

      for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

      your_csv_file.close()


   return 'file uploaded successfully'
# function that reads the test.csv and creates dataframe from which a filtered dataframe is generated which contains all the metabolics with suffix as PC and later write it a file
@app.route('/metabolic_suffix_PC')
def metabolic_suffix_PC():
    column_names = pd.read_csv('input/test.csv',  engine='python')
    columns=list(column_names.columns.values)
    dict={}
    for i in range(len(columns)):
        dict[i]=columns[i]


    csv_df = pd.read_csv('input/test.csv', header=None, skiprows=1, engine='python')
    child_dataset1 = csv_df[csv_df[2].str.endswith('PC', na=False)]
    child_dataset1.rename(columns=dict,inplace=True)
    tfile = open('outputs/output_PC.csv', 'w')
    tfile.write(child_dataset1.to_string())
    tfile.close()
    return send_file('outputs/output_PC.csv',
                     mimetype='text/csv',
                     attachment_filename='output_PC.csv',
                     as_attachment=True)

# function that reads the test.csv and creates dataframe from which a filtered dataframe is generated which contains all the metabolics with suffix as LPC and later write it a file
@app.route('/metabolic_suffix_LPC')
def metabolic_suffix_LPC():
    column_names = pd.read_csv('input/test.csv',  engine='python')
    columns=list(column_names.columns.values)
    dict={}
    for i in range(len(columns)):
        dict[i]=columns[i]


    csv_df = pd.read_csv('input/test.csv', header=None, skiprows=1, engine='python')
    child_dataset2 = csv_df[csv_df[2].str.endswith('LPC', na=False)]
    child_dataset2.rename(columns=dict,inplace=True)
    tfile = open('outputs/output_LPC.csv', 'w')
    tfile.write(child_dataset2.to_string())
    tfile.close()
    return send_file('outputs/output_LPC.csv',
                     mimetype='text/csv',
                     attachment_filename='output_LPC.csv',
                     as_attachment=True)

# function that reads the test.csv and creates dataframe from which a filtered dataframe is generated which contains all the metabolics with suffix as plasmalogen and later write it a file
@app.route('/metabolic_suffix_plasmalogen')
def metabolic_suffix_plasmalogen():
    column_names = pd.read_csv('input/test.csv',  engine='python')
    columns=list(column_names.columns.values)
    dict={}
    for i in range(len(columns)):
        dict[i]=columns[i]


    csv_df = pd.read_csv('input/test.csv', header=None, skiprows=1, engine='python')
    child_dataset3 = csv_df[csv_df[2].str.endswith('plasmalogen', na=False)]
    child_dataset3.rename(columns=dict,inplace=True)
    tfile = open('outputs/output_plasmalogen.csv', 'w')
    tfile.write(child_dataset3.to_string())
    tfile.close()
    return send_file('outputs/output_plasmalogen.csv',
                     mimetype='text/csv',
                     attachment_filename='output_plasmalogen.csv',
                     as_attachment=True)
# function that appends the Retention Time Roundoff column in the main dataframe and later write it a file
@app.route('/parentfile_with_RTR')
def parentfile_with_RTR():
    column_names = pd.read_csv('input/test.csv',  engine='python')
    columns=list(column_names.columns.values)
    dict={}
    for i in range(len(columns)):
        dict[i]=columns[i]


    csv_df = pd.read_csv('input/test.csv', header=None, skiprows=1, engine='python')
    csv_df[1050] = round(csv_df[1])
    csv_df.rename(columns={1050:'Retention Time Roundoff(in mins)'}, inplace=True)
    csv_df.rename(columns=dict,inplace=True)
    tfile = open('outputs/outputfile_with_RTR.csv', 'w')
    tfile.write(csv_df.to_string())
    tfile.close()
    return send_file('outputs/outputfile_with_RTR.csv',
                     mimetype='text/csv',
                     attachment_filename='outputfile_with_RTR.csv',
                     as_attachment=True)
# function that creates a dataframe that has mean of all metabolics readings grouped by Retention Time Roundoff(in mins) and these dataframe doesnot include unnecessary columns and finally it is written to the file
@app.route('/metabolicmean_with_similarRTR')
def metabolicmean_with_similarRTR():
    column_names = pd.read_csv('input/test.csv',  engine='python')
    columns=list(column_names.columns.values)
    dict={}
    for i in range(3,len(columns)):
        dict[i]=columns[i]
    csv_df = pd.read_csv('input/test.csv', header=None, skiprows=1, engine='python')
    csv_df[1050] = round(csv_df[1])
    csv_df.drop([0,1,2], axis = 1, inplace = True)
    csv_df.rename(columns=dict,inplace=True)



    csv_df.rename(columns={1050:'Retention Time Roundoff(in mins)'}, inplace=True)

    final =csv_df.groupby('Retention Time Roundoff(in mins)').agg('mean')

    tfile = open('outputs/outputfile_metabolicmean_with_similarRTR.csv', 'w')

    tfile.write(final.to_string())
    tfile.close()
    return send_file('outputs/outputfile_metabolicmean_with_similarRTR.csv',
                     mimetype='text/csv',
                     attachment_filename='outputfile_metabolicmean_with_similarRTR.csv',
                     as_attachment=True)


