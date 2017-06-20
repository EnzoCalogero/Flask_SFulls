import pandas as pd 
import pyodbc 

##################################################
#### Merging Area ################################
##################################################
def Merge_Dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z
LON3={"CS401":'lon301cs0401',"CS402":'lon301cs0402',"CS403":"lon301cs0403","CS404":"lon301cs0404","CS406":"lon301cs0406","CS410":'lon301cs0410',"CS411":'lon301cs0411',"CS499":"lon301cs0499","CS498":"lon301cs0498","CSITS":"lon301ITS",}
LON5={"CS301":'lon501cs0301',"CS302":'lon501cs0302'}
CS=Merge_Dicts(LON3,LON5)
ORD={"CS901":'ord101cs0901',"CS902":'ord101cs0902',"CS903":"ord101cs0903","CS904":"ord101cs0904","CS905":"ord101cs0905","CS906":'ord101cs0906'}
CS=Merge_Dicts(CS,ORD)
IAD={"CS801":'iad201cs0801',"CS802":'iad201cs0802',"CS803":"iad201cs0803","CS804":"iad301cs0804","CS805":"iad301cs0805"}
CS=Merge_Dicts(CS,IAD)
DFW={"CS01":'dfw101cs0001',"CS07":'dfw101cs0007',"CS12":"dfw101cs0012","CS20":"dfw102cs0020","CS21":"dfw102cs0021","CS41":"dfw103cs0041","CS101":"dfw301CS0101","CS102":"dfw301CS0102","AONCS":"dfw0102AONCS"}
CS=Merge_Dicts(CS,DFW)
syd={"CS501":'syd201cs0501',"CS502":'syd201cs0502',"CS510":"syd401cs0510"}
CS=Merge_Dicts(CS,syd)
HK={"CS701":'HKG101cs0701'}
CS=Merge_Dicts(CS,HK)


##################################################
#### End Merging Area ############################
##################################################


from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/')
def route():

   return render_template('TSQuery.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   #print(request.form)
   if request.method == 'POST':
      #result = request.form
      CSloc=CS[request.form["commcell"]]
      SP=request.form["Storage Policy"]
      SP= "'"+SP+"'"
      #SP="'z_2Week_MA03-A'"
      
      #del request.form["commcell"]
      result = request.form
######################################################      
      
      
      cnxn = pyodbc.connect(DSN=CSloc)
      
      sql_qry1="""

      select DATENAME(DW,startdate) as WeekDay ,COUNT( distinct(clientname)) as Number from commcellbackupinfo 
      where backuplevel = 'SyntheticFull' and  data_sp=
      """
      sql_qry2="""
       and startdate>dateadd(day, -8, getdate())
      group by DATENAME(DW,startdate) 
      """

      sql_qry=sql_qry1+SP+sql_qry2

      
      
      
      df = pd.read_sql(sql_qry, cnxn)
      cnxn.close()  
      df=df.set_index('WeekDay')['Number'].to_dict()
      result=df
      

          
          
          
      
         
      
####################################################################      
   return render_template("result.html",result=result,SPloc = SP,CSl=CSloc)   
   


@app.route('/SyntFulls')
def SyntFulls():

   return render_template('SFQuery.html')   

@app.route('/SFresult',methods = ['POST', 'GET'])
def SFresult():
   #print(request.form)
   if request.method == 'POST':
      result = request.form
      
#########################################
      sql_qry="""
      select data_sp as StoragePolicy, COUNT(distinct( clientname))as Number from commcellbackupinfo where backuplevel = 'SyntheticFull' group by    
      data_sp ORDER BY Number 
      """
      
      #cnxn=pyodbc.connect(Driver='{SQL Server}',Server="10.9.10.40\commvault",Database="Commserv",Trusted_Connection='yes')
      cnxn = pyodbc.connect(DSN=CS[result["Commcell"]])
      
      df = pd.read_sql(sql_qry, cnxn)
      cnxn.close()      
      df=df.set_index('StoragePolicy')['Number'].to_dict()
      result=df
     
############################################################      
  
      return render_template("SFresult.html",result = result)
      
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
      
      
      
      
@app.route('/TSresult',methods = ['POST', 'GET'])
def TSresult():
   #print(request.form)
   if request.method == 'POST':
      result = request.form
      
#########################################
      sql_qry="""
      select data_sp as StoragePolicy, COUNT(distinct( clientname))as Number from commcellbackupinfo where backuplevel = 'SyntheticFull' group by    
      data_sp ORDER BY Number 
      """
      import pyodbc
      #cnxn=pyodbc.connect(Driver='{SQL Server}',Server="10.9.10.40\commvault",Database="Commserv",Trusted_Connection='yes')
      cnxn = pyodbc.connect(DSN=CS[result["Commcell"]])
      
      df = pd.read_sql(sql_qry, cnxn)
      cnxn.close() 
      if(df.empty):
#         df=result   
          return render_template('Nodata.html') 
      df=df.set_index('StoragePolicy')['Number'].to_dict()
      CSloc=result["Commcell"]

      result=df  
          

       
############################################################      
  
      return render_template("TSresult.html",result = result,CSl=CSloc)
@app.route('/TS')
def TS():

   return render_template('TSQuery.html')   
   

if __name__ == '__main__':
   app.run(debug=True )