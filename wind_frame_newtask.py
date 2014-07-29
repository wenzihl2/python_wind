__author__ = 'Administrator'
#coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import wx
import wx.grid
import wind_mssql
app=wx.App()


class task():
    panel=wx.Panel
    okbtn=wx.Button(panel,label="确定")
    cancelbtn=wx.Button(panel,label="取消")
    taskname=wx.StaticText(panel,label="任务名称")
    taskname_t=wx.TextCtrl(panel)
    tabelname=wx.StaticText(panel,label="表名")
    tabelname_t=wx.TextCtrl(panel)
    freqinterval=wx.StaticText(panel,label="采集频率")
    freqinterval_t=wx.TextCtrl(panel)
    freunit=wx.StaticText(panel,label="采集周期")
    sampleList = ['日', '周','半月', '月','半年', '年']

    freunit_t=wx.ComboBox(panel, -1, "日", (15, 30), wx.DefaultSize,choices=sampleList)
    taskstatus=wx.StaticText(panel,label="任务状态")
    taskstatus_t=wx.TextCtrl(panel)
    zbid=wx.StaticText(panel,label="指标名称")
    zbid_t=wx.TextCtrl(panel,style=wx.TE_MULTILINE|wx.HSCROLL)
    zbname=wx.StaticText(panel,label="指标ID")
    zbname_t=wx.TextCtrl(panel,style=wx.TE_MULTILINE|wx.HSCROLL)
    vbox1= wx.BoxSizer(wx.VERTICAL)
    vbox2= wx.BoxSizer(wx.VERTICAL)
    vbox3= wx.BoxSizer(wx.VERTICAL)
    vbox4= wx.BoxSizer(wx.VERTICAL)
    hbox1=wx.BoxSizer(wx.HORIZONTAL)
    hbox2=wx.BoxSizer(wx.HORIZONTAL)
    hbox3=wx.BoxSizer(wx.HORIZONTAL)
    logtext=wx.TextCtrl(panel,size=(200,200),style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_RICH2)


    def __init__(self,win):
        panel=wx.Panel(win)
    def createwindow(win):
        vbox1.Add(taskname,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=5)
        vbox1.Add(taskname_t,proportion=0,flag=wx.EXPAND|wx.ALL,border=0 )
        vbox1.Add(tabelname,proportion=0,flag=wx.EXPAND|wx.ALL,border=5 )
        vbox1.Add(tabelname_t,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=0)
        vbox1.Add(freqinterval,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=5)
        vbox1.Add(freqinterval_t,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=0)
        vbox1.Add(freunit,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=5)
        vbox1.Add(freunit_t,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=0)
        vbox1.Add(taskstatus,proportion=0,flag=wx.EXPAND|wx.ALL,border=5 )
        vbox1.Add(taskstatus_t,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=0)
        vbox1.Add(okbtn,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=5)
        vbox1.Add(cancelbtn,proportion=0 ,flag=wx.EXPAND|wx.ALL,border=5)
        vbox2.Add(zbid,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
        vbox2.Add(zbid_t,proportion=1,flag=wx.EXPAND|wx.ALL)
        vbox3.Add(zbname,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
        vbox3.Add(zbname_t,proportion=1,flag=wx.EXPAND|wx.ALL)


        hbox1.Add(vbox2,proportion=1,flag=wx.EXPAND|wx.RIGHT,border=10)
        hbox1.Add(vbox3,proportion=1,flag=wx.EXPAND|wx.RIGHT,border=10)
        hbox1.Add(vbox1,proportion=0)
        vbox4.Add(hbox1,proportion=1,flag=wx.EXPAND|wx.ALL,border=5)
        vbox4.Add(logtext,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
        panel.SetSizer(vbox4)
    def newtaskframe(preframe):
        window=wx.Frame(preframe, title="新增任务",size=(810,685))
        createwindow(window)
        window.Show()
    def edittaskframe(preframe):
        window=wx.Frame(preframe, title="编辑任务",size=(810,685))
        createwindow(window)

        window.Show()
        return preframe
    def _Ok(event):
        print(self)
app.MainLoop()
