#coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import wind_mssql
import wx
import datetime
from datetime import *
from WindPy import *
import threading
import wind_log
class caiji(threading.Thread):
    def __init__(self,basic_types,logtext):
        threading.Thread.__init__(self)
        self.basic_types=basic_types
        self.thread_stop = False
        self.logtext=logtext
        w.start()



    def run(self):
        self.mssql=wind_mssql.MSSQL(host="172.19.9.54",user="sa",pwd="Yafco2012",db="YaParams",charset="utf8")

        w.start()

        for basic_type in self.basic_types:


            self.tasklist = self.mssql.ExecQuery("SELECT task_id,source_id,task_name,table_name,start_time,freq_interval,freq_unit,task_status FROM task_mgr WHERE task_type='4' and source_id='"+str(basic_type)+"'")
            self.zblist=self.mssql.ExecQuery("SELECT basic_value,bloomberg_code FROM [datacenter_new].[dbo].[T_BASICDATA] WHERE basic_type='"+str(basic_type)+"'")
            self.zbfieldlist=self.mssql.ExecQuery("SELECT zbfield FROM [Yaparams].[dbo].[task_wind_job_new] WHERE basic_type='"+str(basic_type)+"'")
            cur=self.mssql.GetConnect()
            print(self.zblist)
            zbstr=(wind_log.zb().zbread(self.tasklist[0][1]))





            startdate="1900-01-01"
            enddate=datetime.today()
            #taskstartlog=enddate.strftime('%Y-%m-%d %H:%M:%S   ')+"task: "+str(self.tasklist[0][0])+" start  from "+startdate.strftime('%Y-%m-%d')+"   to  "+enddate.strftime('%Y-%m-%d')+'\n'
            taskstartlog=enddate.strftime('%Y-%m-%d %H:%M:%S   ')+"task: "+str(self.tasklist[0][0])+" start\n"
            wind_log.date().datewrite(taskstartlog,datetime.now().strftime('%Y-%m-%d'))
            zbstr+=taskstartlog
            self.logtext.AppendText(taskstartlog)
            print(taskstartlog)

            for j in range(len(self.zblist)):
                print(self.zblist)
                cur.execute("SELECT COUNT(fdate) FROM [datacenter_new].[dbo].["+self.tasklist[0][3]+"] WHERE ftype='"+str(j+1)+"'")

                if(cur.fetchall()[0][0]==0):
                    startdate="1900-01-01"
                else:
                    cur.execute("SELECT MAX(fdate) FROM [datacenter_new].[dbo].["+self.tasklist[0][3]+"] WHERE ftype='"+str(j+1)+"'")
                    startdate=cur.fetchall()[0][0]
                print(startdate)


                i=0
                data=w.wsd(str(self.zblist[j][1]),str(self.zbfieldlist[j][0]), startdate,enddate, "Fill=Previous")
                print(data)
                if data.ErrorCode==0:

                    for i in range(len(data.Times)):


                        try:
                            sql="insert into [datacenter_new].[dbo].["+self.tasklist[0][3]+"](fdate,ftype,famount,updatetime) values('"+str(data.Times[i])+"','"+str(j+1)+"','"+str(data.Data[0][i])+"','"+datetime.today().strftime('%Y-%m-%d %H:%M:%S')+"')"
                            cur.execute(sql)
                            sqllog="insert "+"values('"+str(data.Times[i])+"','"+str(j+1)+"','"+str(data.Data[0][i])+"','"+datetime.today().strftime('%Y-%m-%d %H:%M:%S')+"')"

                            print(sqllog)
                            self.mssql.conn.commit()


                            self.logtext.AppendText(sqllog+"\n")
                            zbstr+=(sqllog+"\n")
                        except:
                            print("insert error")
                            sql="UPDATE [datacenter_new].[dbo].["+self.tasklist[0][3]+"] SET famount='"+str(data.Data[0][i])+"',updatetime='"+datetime.today().strftime('%Y-%m-%d %H:%M:%S')+"' WHERE fdate='"+str(data.Times[i])+"' and ftype='"+str(j+1)+"'"
                            cur.execute(sql)
                            sqllog="update "+"values('"+str(data.Times[i])+"','"+str(j+1)+"','"+str(data.Data[0][i])+"','"+datetime.today().strftime('%Y-%m-%d %H:%M:%S')+"')"

                            print(sqllog)
                            self.mssql.conn.commit()
                            self.logtext.AppendText(sqllog+"\n")
                            zbstr+=(sqllog+"\n")
                        #insert.conn.close()  #关闭放在外面执行
                else:
                    print("w.wsd error")

            self.mssql.conn.close()  #关闭放在外面执行
            taskendlog=datetime.today().strftime('%Y-%m-%d %H:%M:%S   ')+"task: "+str(self.tasklist[0][0])+" end"
            print(taskendlog)
            zbstr+=(taskendlog+"\n")
            wind_log.date().datewrite(taskendlog+"\n",datetime.now().strftime('%Y-%m-%d'))
            self.logtext.AppendText(taskendlog+"\n")
            wind_log.zb().zbwrite(zbstr,str(basic_type))



    def stop(self):
        self.thread_stop = True
class caijitask:
    None


