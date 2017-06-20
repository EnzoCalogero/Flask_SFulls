
def Conn(CS="CS404"):
    '''
    argoment teh Commcell return the list of synthetic full per Storage policy on the Commcell
    '''        
    
    import pypyodbc
#import os
    import pandas as pd  
    sql_qry="""

    select data_sp as StoragePolicy, COUNT(distinct( clientname))as Number from commcellbackupinfo where backuplevel = 'SyntheticFull' group by 
    data_sp ORDER BY Number

    """
    LON3={"CS401":"lon301cs0401","CS404":"lon301cs0404","CS498":"lon301cs0498","CSITS":"lon301ITS","CS499":"lon301cs0499"}
    
    
    #sql_Ora="SELECT CONVERT(NVARCHAR(30),getdate(), 120) "
    ###################################################
    #CS="CS404"
    
    #print(LON3[CS])
        #try:
    cnxn = pypyodbc.connect(DSN=LON3[CS]) #DSN=MYDATABASE; UID=MYUSER; PWD=MYPASSWORD
             
    #Ora=pd.read_sql(sql_Ora, cnxn)
    df = pd.read_sql(sql_qry, cnxn)
    #print(Ora)
    #print(df)
    
    df=df.set_index('StoragePolicy')['Number'].to_dict()
    return df





from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def student():
   return render_template('FirstQuery.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   print(request.form)
   if request.method == 'POST':
      result = request.form
      print(result)
      #result=Conn(result["Commcell"])  
      print(result)
   return render_template("result.html",result = result)

if __name__ == '__main__':
   app.run(debug=True )