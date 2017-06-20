# -*- coding: utf-8 -*-
"""
Created on Mon Feb 06 05:07:05 2017

@author: enzo.calogero
"""
SP="'z_2Week_MA03-A'"
sql_qry1="""
select DATENAME(DW,startdate) as WeekDay ,clientname as Number from commcellbackupinfo 
where backuplevel = 'SyntheticFull' 
"""
sql_qry2="""
and startdate>dateadd(day, -8, getdate())
group by DATENAME(DW,startdate) 
"""


sql_qry=sql_qry1+sql_qry2

import pyodbc
import pandas as pd  
      #cnxn= .connect(Driver='{SQL Server}',Server="10.9.10.40\commvault",Database="Commserv",Trusted_Connection='yes')
cnxn = pyodbc.connect(DSN='lon301cs0499')
      
df = pd.read_sql(sql_qry1, cnxn)
cnxn.close()      
#df=df.set_index('StoragePolicy')['Number'].to_dict()
#result=df


#  select distinct data_sp, DATENAME(DW,startdate),data_sp + DATENAME(DW,startdate) as merged,COUNT(distinct clientname) from commcellbackupinfo where backuplevel = 'SyntheticFull'  
#  group by data_sp, DATENAME(DW,startdate) order by data_sp