
#def Conn(CS="CS404"):

#import pypyodbc
#import os
import pandas as pd  
sql_qry="""
select data_sp as StoragePolicy, COUNT(distinct( clientname))as Number from commcellbackupinfo where backuplevel = 'SyntheticFull' group by 
data_sp ORDER BY Number
"""
LON3={"CS401":"lon301cs0401","CS404":"lon301cs0404","CS498":"lon301cs0498","CSITS":"lon301ITS","CS499":"lon301cs0499"}


#k={u'z_940995_52WeekOffSite_HC08-C': 1, u'Z_1700246_HCO1_Lon5OffSite(disk)': 2, u'z4WeekOffsite (DiskA-MA9)': 3, u'z_12WeekOffsite_MA06-B': 2, u'z4WeekOffSite (DiskJ-MA12)': 2, u'z52WeekOffSite (DiskB-MA15)': 2, u'z4WeekOffsite (DiskH-MA9)': 2, u'Z_239737_HCO3_3Week(disk)_4WeekOffsite(tape)': 7, u'4WeekOffsite (DiskA-MA13)': 1, u'z_4WeekOffSite (DiskD-MA12)': 3, u'52WeekOffSite (DiskA-MA15)': 1}
#df.set_index('storagepolicy')['number'].to_dict() 
#df=pd.read_csv('C:\pyproject\dati.csv')
#df=df.set_index('StoragePolicy')['number'].to_dict()





from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/')
def route():

   return render_template('FirstQuery.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   #print(request.form)
   #if request.method == 'POST':
      result = request.form
      
#########################################
      sql_qry="""
      select data_sp as StoragePolicy, COUNT(distinct( clientname))as Number from commcellbackupinfo where backuplevel = 'SyntheticFull' group by    
      data_sp ORDER BY Number 
      """
      import pyodbc
      cnxn=pyodbc.connect(Driver='{SQL Server}',Server="10.9.10.40\commvault",Database="Commserv",Trusted_Connection='yes')#,uid="enzo.calogero",pwd="N1cole89."
    
      #cnxn = pypyodbc.connect(DSN="lon301cs0401") #DSN=MYDATABASE; UID=MYUSER; PWD=MYPASSWORD
      df = pd.read_sql(sql_qry, cnxn)
      df=df.set_index('StoragePolicy')['Number'].to_dict()
      result=df
      cnxn.close()
############################################################      
      
     # print(result)
     # cnxn = pypyodbc.connect(DSN="lon301cs0404")
     # df = pd.read_sql(sql_qry, cnxn)
      #result=df.set_index('storagepolicy')['number'].to_dict()  
      #print(result)
      #result = request.form
      return render_template("result.html",result = result)

if __name__ == '__main__':
   app.run(debug=True )