__author__ = 'Administrator'
#coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import wx
import wind_mssql
import datetime
from datetime import *
import wind_caiji
from WindPy import *
import wind_log
app=wx.App()


class task:
    def __init__(self,win,title,grid,Refresh):
        self.refresh=Refresh
        self.grid=grid
        self.window=wx.Frame(win, title=title,size=(810,685))
        self.window.Center()
        self.panel=wx.Panel(self.window)
        self.mssql=wind_mssql.MSSQL(host="172.19.9.54",user="sa",pwd="Yafco2012",db="datacenter_new",charset="utf8")
        self.okbtn=wx.Button(self.panel,label="确定")
        self.okbtn.Bind(wx.EVT_BUTTON,self.Ok)

        self.cancelbtn=wx.Button(self.panel,label="取消")
        self.cancelbtn.Bind(wx.EVT_BUTTON,self.Cancel)

        self.taskname=wx.StaticText(self.panel,label="任务名称")
        self.taskname_t=wx.TextCtrl(self.panel)
        self.tablename=wx.StaticText(self.panel,label="表名")
        self.tablename_t=wx.TextCtrl(self.panel)
        self.freqinterval=wx.StaticText(self.panel,label="采集频率")
        self.freqinterval_t=wx.TextCtrl(self.panel)
        self.freunit=wx.StaticText(self.panel,label="采集周期")
        sampleList = ['日', '周','旬','半月', '月','季度','半年', '年']
        self.sampleListtoint={'日':'1', '周':'2','旬':'3','半月':'4', '月':'5','季度':'6','半年':'7', '年':'8'}
        self.taskstatuslist=['开启采集','关闭采集']
        self.taskstatuslisttoint={'开启采集':'0','关闭采集':'1'}
        self.freunit_t=wx.ComboBox(self.panel, -1, "日", (15, 30), wx.DefaultSize,choices=sampleList)
        self.taskstatus=wx.StaticText(self.panel,label="任务状态")
        self.taskstatus_t=wx.ComboBox(self.panel, -1, '开启采集', (15, 30), wx.DefaultSize,choices=self.taskstatuslist)
        self.isunittoint={'否':'0','是':'1'}
        self.isunit=wx.StaticText(self.panel,label="是否按采集周期提取")
        self.isunit_t=wx.ComboBox(self.panel, -1, '否', (15, 30), wx.DefaultSize,choices=['是','否'])
        self.zbname=wx.StaticText(self.panel,label="指标名称")
        self.zbname_t=wx.TextCtrl(self.panel,style=wx.TE_MULTILINE|wx.HSCROLL)
        self.zbid=wx.StaticText(self.panel,label="指标ID")
        self.zbid_t=wx.TextCtrl(self.panel,style=wx.TE_MULTILINE|wx.HSCROLL)
        self.zbfield=wx.StaticText(self.panel,label="指标field")
        self.zbfield_t=wx.TextCtrl(self.panel,style=wx.TE_MULTILINE|wx.HSCROLL)
        vbox1= wx.BoxSizer(wx.VERTICAL)
        vbox2= wx.BoxSizer(wx.VERTICAL)
        vbox3= wx.BoxSizer(wx.VERTICAL)
        vbox4= wx.BoxSizer(wx.VERTICAL)
        vbox5= wx.BoxSizer(wx.VERTICAL)
        hbox1=wx.BoxSizer(wx.HORIZONTAL)
        hbox2=wx.BoxSizer(wx.HORIZONTAL)
        hbox3=wx.BoxSizer(wx.HORIZONTAL)
       
        self.freqinterval_t.SetValue('1')
        vbox1.Add(self.taskname,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=5)
        vbox1.Add(self.taskname_t,proportion=0,flag=wx.EXPAND|wx.ALL,border=0 )
        vbox1.Add(self.tablename,proportion=0,flag=wx.EXPAND|wx.ALL,border=5 )
        vbox1.Add(self.tablename_t,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=0)
        vbox1.Add(self.freqinterval,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=5)
        vbox1.Add(self.freqinterval_t,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=0)
        vbox1.Add(self.freunit,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=5)
        vbox1.Add(self.freunit_t,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=0)
        vbox1.Add(self.taskstatus,proportion=0,flag=wx.EXPAND|wx.ALL,border=5 )
        vbox1.Add(self.taskstatus_t,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=0)
        vbox1.Add(self.isunit,proportion=0,flag=wx.EXPAND|wx.ALL,border=5 )
        vbox1.Add(self.isunit_t,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=0)
        vbox1.Add(self.okbtn,proportion=0 ,flag=wx.EXPAND|wx.TOP,border=5)
        vbox1.Add(self.cancelbtn,proportion=0 ,flag=wx.EXPAND|wx.TOP,border=5)
        vbox2.Add(self.zbid,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
        vbox2.Add(self.zbid_t,proportion=1,flag=wx.EXPAND|wx.ALL)
        vbox3.Add(self.zbname,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
        vbox3.Add(self.zbname_t,proportion=1,flag=wx.EXPAND|wx.ALL)
        vbox5.Add(self.zbfield,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
        vbox5.Add(self.zbfield_t,proportion=1,flag=wx.EXPAND|wx.ALL)
       

        hbox1.Add(vbox3,proportion=1,flag=wx.EXPAND|wx.RIGHT,border=10)
        hbox1.Add(vbox2,proportion=0.5,flag=wx.EXPAND|wx.RIGHT,border=10)
        hbox1.Add(vbox5,proportion=0.5,flag=wx.EXPAND|wx.RIGHT,border=10)
        hbox1.Add(vbox1,proportion=0)
        vbox4.Add(hbox1,proportion=1,flag=wx.EXPAND|wx.ALL,border=5)





        self.panel.SetSizer(vbox4)







        self.window.Show()

        return
    def Cancel(self,event):
        self.window.Close(True)

    def Ok(self,event):
        print("ok")
        if str(self.tablename_t.GetValue())=='':
            dlg = wx.MessageDialog(None,'表名不能为空','通知',wx.OK)
            if dlg.ShowModal() == wx.ID_OK:
                    return
            dlg.Destroy()

        else:
            if str(self.taskname_t.GetValue())=='':
                dlg = wx.MessageDialog(None,'任务名称不能为空','通知',wx.OK)
                if dlg.ShowModal() == wx.ID_OK:
                    return
                dlg.Destroy()
                
                
        self.zbidlist=self.zbid_t.GetValue().splitlines()
        self.zbnamelist=self.zbname_t.GetValue().splitlines()
        self.zbfieldlist=self.zbfield_t.GetValue().splitlines()

        if len(self.zbidlist)==len(self.zbnamelist):
            if len(self.zbidlist)==len(self.zbfieldlist):
                #print(self.mssql.ExecQuery("SELECT COUNT(task_id) FROM [YaParams].[dbo].[task_mgr] WHERE table_name='"+str(self.tablename_t.GetValue())+"'"))
                if  self.mssql.ExecQuery("SELECT COUNT(task_id) FROM [YaParams].[dbo].[task_mgr] WHERE table_name='"+str(self.tablename_t.GetValue())+"'")[0][0]==0:


                    zbstr=('')


                    self.basic_type=self.mssql.ExecQuery("SELECT MAX(basic_type) FROM [datacenter_new].[dbo].[T_BASICDATA] ")[0][0]+1

                    #在task_mgr中插入元组
                    try:
                        self.mssql.ExecNonQuery("insert into [YaParams].[dbo].[task_mgr](source_id,task_type,task_name,table_name,start_time,freq_interval,freq_unit,task_status,source,contract_type) values('"+str(self.basic_type)+"','4','"+str(self.taskname_t.GetValue())+"','"+str(self.tablename_t.GetValue())+"','"+datetime.today().strftime('%Y-%m-%d %H:%M:%S')+"','"+str(self.freqinterval_t.GetValue())+"','"+self.sampleListtoint[str(self.freunit_t.GetValue())]+"','"+self.taskstatuslisttoint[str(self.taskstatus_t.GetValue())]+"','万得','"+self.isunittoint[str(self.isunit_t.GetValue())]+"')")
                        print("在表task_mgr中插入元组   '"+str(self.basic_type)+"','4','"+str(self.taskname_t.GetValue())+"','"+str(self.tablename_t.GetValue())+"','"+datetime.today().strftime('%Y-%m-%d %H:%M:%S')+"','"+str(self.freqinterval_t.GetValue())+"','"+self.sampleListtoint[str(self.freunit_t.GetValue())]+"','"+self.taskstatuslisttoint[str(self.taskstatus_t.GetValue())]+"'")
                    except:
                        print("在task_mgr中插入元组出错")

                    self.taskid=self.mssql.ExecQuery("SELECT task_id FROM [YaParams].[dbo].[task_mgr] WHERE task_type='4' and source_id='"+str(self.basic_type)+"'")[0][0]
                    newtasklog=datetime.today().strftime('%Y-%m-%d %H:%M:%S ')+"新建任务："+str(self.taskid)+"\n"
                    zbstr+=newtasklog
                    wind_log.date().datewrite(newtasklog,datetime.now().strftime('%Y-%m-%d'))


                    #在T_BASIC中插入元组
                    try:

                        for i in range(len(self.zbidlist)):
                            self.mssql.ExecNonQuery("insert into [datacenter_new].[dbo].[T_BASICDATA](basic_type,basic_no,basic_value,bloomberg_code) values('"+str(self.basic_type)+"','"+str(i+1)+"','"+str(self.zbnamelist[i])+"','"+str(self.zbidlist[i])+"')")
                            print("在表T_BASIC中插入数据   '"+str(self.basic_type)+"','"+str(i+1)+"','"+str(self.zbnamelist[i])+"','"+str(self.zbidlist[i])+"'")

                            self.mssql.ExecNonQuery("insert into [Yaparams].[dbo].[task_wind_job_new](basic_type,basic_no,zbfield) values('"+str(self.basic_type)+"','"+str(i+1)+"','"+str(self.zbfieldlist[i])+"')")
                            print("在表task_wind_job_new中插入数据   '"+str(self.basic_type)+"','"+str(i+1)+"','"+str(self.zbfieldlist[i])+"'")
                            zbstr+=datetime.today().strftime('%Y-%m-%d %H:%M:%S')+" 加入指标   '"+str(self.zbnamelist[i])+"','"+str(self.zbidlist[i])+"','"+str(self.zbfieldlist[i])+"'\n"
                    except:
                        print("在T_BASIC中插入数据  "+str(self.basic_type)+"','2','"+str(self.taskname_t.GetValue())+"   出错")



                    # 在datacenter_new建表
                    try:
                       self.mssql.ExecNonQuery("execute create_datacenter_table '"+str(self.tablename_t.GetValue())+"','"+str(self.taskname_t.GetValue())+"',''")
                        #print(str(back))
                        #if str(back)=='':
                           # print("NOne")
                      #  else:
                       print("调用存储过程建表　 execute create_datacenter_table '"+str(self.tablename_t.GetValue())+"'")
                    except:
                        print("建表"+str(self.tablename_t.GetValue())+"出错")
                    self.refresh(True)
                    wind_log.zb().zbwrite(zbstr,str(self.basic_type))
                    self.window.Close(True)
                else:
                    dlg = wx.MessageDialog(self.window,'该表名已存在','通知',style= wx.CANCEL)
                    dlg.ShowModal()



            else:
                dlg = wx.MessageDialog(self.window,'指标输入数目不等','通知',style= wx.CANCEL)
                dlg.ShowModal()

        else:
            dlg = wx.MessageDialog(self.window,'指标输入数目不等','通知',style= wx.CANCEL)
            dlg.ShowModal()


class looktask:
    def __init__(self,win,basic_type,refresh):
        self.basic_type=basic_type
        self.refresh=refresh
        self.mssql=wind_mssql.MSSQL(host="172.19.9.54",user="sa",pwd="Yafco2012",db="YaParams",charset="utf8")
        self.tasklist = self.mssql.ExecQuery("SELECT task_id,source_id,task_name,table_name,start_time,freq_interval,freq_unit,task_status,contract_type FROM task_mgr WHERE task_type='4' and source_id='"+str(self.basic_type)+"'")
        self.zblist=self.mssql.ExecQuery("SELECT basic_value,bloomberg_code FROM [datacenter_new].[dbo].[T_BASICDATA] WHERE basic_type='"+str(self.basic_type)+"'")
        self.zbfieldlist=self.mssql.ExecQuery("SELECT zbfield FROM [Yaparams].[dbo].[task_wind_job_new] WHERE basic_type='"+str(self.basic_type)+"'")
        self.window=wx.Frame(win, title="查看任务 "+str(self.tasklist[0][0])+"",size=(810,785))
        self.panel=wx.Panel(self.window)

        self.okbtn=wx.Button(self.panel,label="采集历史数据")
        self.okbtn.Bind(wx.EVT_BUTTON,self.Caiji)
        self.clearbtn=wx.Button(self.panel,label="清空对应数据表")
        self.clearbtn.Bind(wx.EVT_BUTTON,self.Clear)
        self.savebtn=wx.Button(self.panel,label="保存并关闭")
        self.savebtn.Bind(wx.EVT_BUTTON,self.Save)




        self.taskid=wx.StaticText(self.panel,label="任务id")
        self.taskid_t=wx.TextCtrl(self.panel)
        self.taskid_t.SetValue(str(self.tasklist[0][0]))
        self.taskbasic_type=wx.StaticText(self.panel,label="basic_type")
        self.taskbasic_type_t=wx.TextCtrl(self.panel)
        self.taskbasic_type_t.SetValue(str(self.tasklist[0][1]))
        self.taskname=wx.StaticText(self.panel,label="任务名称")
        self.taskname_t=wx.TextCtrl(self.panel)
        self.taskname_t.SetValue(str(self.tasklist[0][2]))
        self.tablename=wx.StaticText(self.panel,label="表名")
        self.tablename_t=wx.TextCtrl(self.panel)
        self.tablename_t.SetValue(str(self.tasklist[0][3]))
        self.freqinterval=wx.StaticText(self.panel,label="采集频率")
        self.freqinterval_t=wx.TextCtrl(self.panel)
        self.freunit=wx.StaticText(self.panel,label="采集周期")
        sampleList = ['日', '周','旬','半月', '月','季度','半年', '年']
        self.sampleListtoint={'日':'1', '周':'2','旬':'3','半月':'4', '月':'5','季度':'6','半年':'7', '年':'8'}
        self.inttochar={'1':'日', '2':'周','3':'旬','4':'半月', '5':'月','6':'季度','7':'半年', '8':'年'}
        self.taskstatuslist=['开启采集','关闭采集']
        self.taskstatuslisttoint={'开启采集':'0','关闭采集':'1'}
        self.taskstatusinttochar={'0':'开启采集','1':'关闭采集'}
        self.freunit_t=wx.ComboBox(self.panel, -1, self.inttochar[str(self.tasklist[0][6])], (15, 30), wx.DefaultSize,choices=sampleList)
        self.taskstatus=wx.StaticText(self.panel,label="任务状态")
        self.taskstatus_t=wx.ComboBox(self.panel, -1, self.taskstatusinttochar[str(self.tasklist[0][7])], (15, 30), wx.DefaultSize,choices=self.taskstatuslist)
        self.isunittochar={'0':'否','1':'是','None':'否'}
        self.isunittoint={'否':'0','是':'1'}
        self.isunitlist=['是','否']
        self.isunit=wx.StaticText(self.panel,label="是否按采集周期提取")
        self.isunit_t=wx.ComboBox(self.panel, -1, self.isunittochar[str(self.tasklist[0][8])], (15, 30), wx.DefaultSize,choices=self.isunitlist)






        self.zbname=wx.StaticText(self.panel,label="指标名称")
        self.zbname_t=wx.TextCtrl(self.panel,style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_READONLY|wx.TE_READONLY)
        for zbname in (self.zblist):
            self.zbname_t.AppendText(str(zbname[0])+"\n")
        self.zbid=wx.StaticText(self.panel,label="指标ID")
        self.zbid_t=wx.TextCtrl(self.panel,style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_READONLY)
        for zbid in (self.zblist):
            self.zbid_t.AppendText(str(zbid[1])+"\n")
        self.zbfield=wx.StaticText(self.panel,label="指标field")
        self.zbfield_t=wx.TextCtrl(self.panel,style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_READONLY)
        for zbfield in (self.zbfieldlist):
            self.zbfield_t.AppendText(str(zbfield[0])+"\n")

        vbox1= wx.BoxSizer(wx.VERTICAL)
        vbox2= wx.BoxSizer(wx.VERTICAL)
        vbox3= wx.BoxSizer(wx.VERTICAL)
        vbox4= wx.BoxSizer(wx.VERTICAL)
        vbox5= wx.BoxSizer(wx.VERTICAL)
        hbox1=wx.BoxSizer(wx.HORIZONTAL)
        hbox2=wx.BoxSizer(wx.HORIZONTAL)
        hbox3=wx.BoxSizer(wx.HORIZONTAL)
        self.logtext=wx.TextCtrl(self.panel,size=(200,200),style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_RICH2)
        self.freqinterval_t.SetValue('1')
        vbox1.Add(self.taskid,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=5)
        vbox1.Add(self.taskid_t,proportion=0,flag=wx.EXPAND|wx.ALL,border=0 )
        vbox1.Add(self.taskbasic_type,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=5)
        vbox1.Add(self.taskbasic_type_t,proportion=0,flag=wx.EXPAND|wx.ALL,border=0 )
        vbox1.Add(self.taskname,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=5)
        vbox1.Add(self.taskname_t,proportion=0,flag=wx.EXPAND|wx.ALL,border=0 )
        vbox1.Add(self.tablename,proportion=0,flag=wx.EXPAND|wx.ALL,border=5 )
        vbox1.Add(self.tablename_t,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=0)
        vbox1.Add(self.freqinterval,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=5)
        vbox1.Add(self.freqinterval_t,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=0)
        vbox1.Add(self.freunit,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=5)
        vbox1.Add(self.freunit_t,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=0)
        vbox1.Add(self.taskstatus,proportion=0,flag=wx.EXPAND|wx.ALL,border=5 )
        vbox1.Add(self.taskstatus_t,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=0)
        vbox1.Add(self.isunit,proportion=0,flag=wx.EXPAND|wx.ALL,border=5 )
        vbox1.Add(self.isunit_t,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=0)
        vbox1.Add(self.okbtn,proportion=0 ,flag=wx.EXPAND|wx.TOP,border=5)
        vbox1.Add(self.clearbtn,proportion=0 ,flag=wx.EXPAND|wx.TOP,border=5)
        vbox1.Add(self.savebtn,proportion=0 ,flag=wx.EXPAND|wx.TOP,border=5)

        vbox2.Add(self.zbid,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
        vbox2.Add(self.zbid_t,proportion=1,flag=wx.EXPAND|wx.ALL)
        vbox3.Add(self.zbname,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
        vbox3.Add(self.zbname_t,proportion=1,flag=wx.EXPAND|wx.ALL)
        vbox5.Add(self.zbfield,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
        vbox5.Add(self.zbfield_t,proportion=1,flag=wx.EXPAND|wx.ALL)


        hbox1.Add(vbox3,proportion=1,flag=wx.EXPAND|wx.RIGHT,border=10)
        hbox1.Add(vbox2,proportion=0.5,flag=wx.EXPAND|wx.RIGHT,border=10)
        hbox1.Add(vbox5,proportion=0.5,flag=wx.EXPAND|wx.RIGHT,border=10)
        hbox1.Add(vbox1,proportion=0)
        vbox4.Add(hbox1,proportion=1,flag=wx.EXPAND|wx.ALL,border=5)
        vbox4.Add(self.logtext,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)



        self.panel.SetSizer(vbox4)





        self.logtext.SetValue(wind_log.zb().zbread(self.tasklist[0][1]))


        self.window.Show()

        return
    def Caiji(self,event):





        #self.dlg = wx.MessageDialog(self.window,'正在采集','通知',style= wx.CANCEL)
        caiji=wind_caiji.caiji([self.basic_type],self.logtext)
        caiji.start()
    def Clear(self,event):
        sql="delete FROM [datacenter_new].[dbo].["+self.tasklist[0][3]+"]"
        self.mssql.ExecNonQuery(sql)
    def Save(self,event):
        zbstr=(wind_log.zb().zbread(self.tasklist[0][1]))
        sql="UPDATE task_mgr SET task_name='"+self.taskname_t.GetValue()+"',freq_interval='"+str(self.freqinterval_t.GetValue())+"',freq_unit='"+self.sampleListtoint[str(self.freunit_t.GetValue())]+"',task_status='"+self.taskstatuslisttoint[str(self.taskstatus_t.GetValue())]+"',contract_type='"+self.isunittoint[str(self.isunit_t.GetValue())]+"' WHERE task_type='4' and source_id='"+str(self.basic_type)+"'"
        print(sql)
        self.mssql.ExecNonQuery(sql)
        self.refresh(True)
        zbstr+="SET task_name='"+self.taskname_t.GetValue()+"',freq_interval='"+str(self.freqinterval_t.GetValue())+"',freq_unit='"+self.sampleListtoint[str(self.freunit_t.GetValue())]+"',task_status='"+self.taskstatuslisttoint[str(self.taskstatus_t.GetValue())]+"'\n"
        wind_log.zb().zbwrite(zbstr,self.tasklist[0][1])
        self.window.Close(True)









        


app.MainLoop()
