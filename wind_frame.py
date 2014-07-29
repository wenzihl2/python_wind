#coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import wx
import wx.grid
import wind_mssql
import wind_frame_newtask_self
import os
import wind_caiji
import threading
import datetime
import wind_log
refresh=wind_mssql.MSSQL(host="172.19.9.54",user="sa",pwd="Yafco2012",db="YaParams",charset="utf8")
app=wx.App()
win=wx.Frame(None, title="万得数据采集工具",size=(910,635))
win.Center()
panel=wx.Panel(win)
panel.SetBackgroundColour((255,255,255,255))
grid=wx.grid.Grid(panel,style=wx.WANTS_CHARS,  name="tasklist")
grid.DisableDragRowSize()
v_box_sizer = wx.BoxSizer(wx.VERTICAL)
grid.EnableEditing(False)
h_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
grid.CreateGrid(1,8,selmode=wx.grid.Grid.SelectRows)
inttochar={'1':'日', '2':'周','3':'旬','4':'半月', '5':'月','6':'季度','7':'半年', '8':'年'}

taskstatusinttochar={'0':'开启采集','1':'关闭采集'}
colLabels = ["任务id","T_BASIC序号" ,"任务名称","表名","任务开始时间","采集频率","采集周期","任务状态"]
for row in range(8):
    grid.SetColLabelValue(row,colLabels[row])

class runtask:
    def __init__(self):
        self.isrun=True
    def start(self):
        print "rundaytask"
        wind_log.date().datewrite(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')+"  开启自动采集\n",datetime.datetime.now().strftime('%Y-%m-%d'))


        self.isrun=True
        self.runmin()

    def stop(self):
        self.isrun=False

    def runday(self):

        if (self.isrun==True):
            print "hello world2"
            resList = refresh.ExecQuery("SELECT task_mgr.task_id,task_time FROM task_mgr,task_exec_list WHERE task_mgr.task_type='4' and task_mgr.task_id=task_exec_list.task_id ")
            #for tasktoday in resList:
                #if tasktoday[1].strftime('%Y-%m-%d')==datetime.datetime.now().strftime('%Y-%m-%d'):
                    #refresh.ExecNonQuery("UPDATE task_mgr SET task_status='1' WHERE task_id='"+tasktoday[0]+"'")




            runday = threading.Timer(1, self.runday)
            runday.start()

    def runmin(self):
         if (self.isrun==True):
            print "runmin   taskList:"
            resList = refresh.ExecQuery("SELECT task_mgr.task_id,source_id FROM task_mgr,task_exec_list WHERE task_mgr.task_type='4' and task_exec_list.exec_status='0' and  task_mgr.task_id=task_exec_list.task_id")
            taskrunList=[]
            print(resList)
            for taskrun in resList:
                taskrunList.append(taskrun[1])
                refresh.ExecNonQuery("UPDATE task_exec_list SET exec_status='1' WHERE task_id='"+str(taskrun[0])+"'")
            caijitask=wind_caiji.caiji(taskrunList, logtext)
            caijitask.start()




            runmin = threading.Timer(60, self.runmin)
            runmin.start()
task=runtask()

def New(event):
    print("new")
    newtask=wind_frame_newtask_self
    newtask.task(win,'新增任务',grid,Refresh)
    grid.MoveCursorDownBlock(False)
def Delete(event):
    print("delete")
    print(grid.GetSelectedRows())
    resList = refresh.ExecQuery("SELECT task_id,source_id,task_name,table_name,start_time,freq_interval,freq_unit,task_status FROM task_mgr WHERE task_type='4'")
    selectedrows=grid.GetSelectedRows()
    print(len(selectedrows))
    for i in range(len(selectedrows)):
        try:
            refresh.ExecNonQuery("DELETE FROM task_mgr WHERE task_id='"+str(resList[selectedrows[i]][0])+"'")
        except:
            print("在数据表task_mgr中删除数据出错")
    grid.DeleteRows(pos=selectedrows[0], numRows=len(selectedrows))
    Refresh(True)
    print(grid.GetSelectedRows())
def Edit(event):
    print("edit")
    resList = refresh.ExecQuery("SELECT task_id,source_id,task_name,table_name,start_time,freq_interval,freq_unit,task_status FROM task_mgr WHERE task_type='4'")
    selectedrows=grid.GetSelectedRows()
    for i in range(len(selectedrows)):
        wind_frame_newtask_self.looktask(win,resList[selectedrows[i]][1],Refresh)
def Save(event):
    print("save")
    print(os.listdir(os.getcwd()))



def Start(event):
    startbtn.SetLabel("关闭自动采集")
    startbtn.Bind(wx.EVT_BUTTON,Stop)
    task.start()
def Stop(event):
    startbtn.SetLabel("开启自动采集")
    startbtn.Bind(wx.EVT_BUTTON,Start)
    task.stop()


def Refresh(event):
    i=0
    print("refresh")
    sampleList=os.getcwd()+'\datelog'

    dateList=os.listdir(sampleList)
    dateList.append('')
    dateList.reverse()

    date.SetItems(dateList)
    date.SetValue(dateList[0])
    Openlog(True)
    resList = refresh.ExecQuery("SELECT task_id,source_id,task_name,table_name,start_time,freq_interval,freq_unit,task_status FROM task_mgr WHERE task_type='4'")
    if len(resList)>grid.GetNumberRows():
        grid.AppendRows(numRows=len(resList)-grid.GetNumberRows())
    else:
        grid.DeleteRows(numRows=grid.GetNumberRows()-len(resList))
    for (task_id,source_id,task_name,table_name,start_time,freq_interval,freq_unit,task_status) in resList:
        grid.SetCellValue(i, 0, str(task_id))
        grid.SetCellValue(i, 1, str(source_id))
        grid.SetCellValue(i, 2, str(task_name))
        grid.SetCellValue(i, 3, str(table_name))
        grid.SetCellValue(i, 4, str(start_time))
        grid.SetCellValue(i, 5, str(freq_interval))
        grid.SetCellValue(i, 6, inttochar[str(freq_unit)])
        grid.SetCellValue(i, 7, taskstatusinttochar[str(task_status)])
        i+=1
    grid.AutoSizeColumns(setAsMin=True)


def Caiji(event):
    print("caiji")
    print(grid.SelectedRows)
    selectedtasks=[]
    for selectedrow in grid.SelectedRows:
        selectedtasks.append(int(grid.GetCellValue(selectedrow,1)))
    print(selectedtasks)
    caijitask=wind_caiji.caiji(selectedtasks, logtext)
    caijitask.start()
def Openlog(event):
    print("Openlog")
    logtext.SetValue(wind_log.date().datetxtread(date.GetValue()))


grid.SetColSize(1, 125)
grid.SetCellValue(0,0,"dsadsadadsadsadasdsadsasdadsasads")
grid.AutoSizeColumns(setAsMin=True)
grid.SetRowLabelSize(80)
startbtn=wx.Button(panel,size=(100,50),label="开启自动采集")
startbtn.Bind(wx.EVT_BUTTON,Start)
newbtn=wx.Button(panel,label="新增")
newbtn.Bind(wx.EVT_BUTTON,New)
deletebtn=wx.Button(panel,label="删除选中行")
deletebtn.Bind(wx.EVT_BUTTON,Delete)
editbtn=wx.Button(panel,label="查看选中行")
editbtn.Bind(wx.EVT_BUTTON,Edit)
savebtn=wx.Button(panel,label="保存列表")
savebtn.Bind(wx.EVT_BUTTON,Save)
refreshbtn=wx.Button(panel,label="刷新")
refreshbtn.Bind(wx.EVT_BUTTON,Refresh)
caijibtn=wx.Button(panel,label="采集选中行")
caijibtn.Bind(wx.EVT_BUTTON,Caiji)
tasklabel=wx.StaticText(panel,label="任务列表")
sampleList=os.getcwd()+'\datelog'

dateList=os.listdir(sampleList)
dateList.append('')

date=wx.ComboBox(panel, -1, dateList[0], (15, 30), (120,30),choices=dateList)
openlog=wx.Button(panel,label="打开日志")
openlog.Bind(wx.EVT_BUTTON,Openlog)


logtext=wx.TextCtrl(panel,size=(200,200),style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_RICH2)
Refresh(True)
h_box_sizer.Add(startbtn, proportion=1, )
h_box_sizer.Add(newbtn, proportion=1, )
h_box_sizer.Add(editbtn, proportion=1, )
h_box_sizer.Add(deletebtn, proportion=1, )
h_box_sizer.Add(savebtn, proportion=1, )
h_box_sizer.Add(refreshbtn, proportion=1, )
h_box_sizer.Add(caijibtn, proportion=1, )
h_box_sizer.Add(date, proportion=1,flag=wx.LEFT,border=30)

h_box_sizer.Add(openlog, proportion=1)
v_box_sizer.Add(tasklabel, proportion=0,flag=wx.EXPAND|wx.ALL,border=10 )
v_box_sizer.Add(grid, proportion=1,flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=10 )
v_box_sizer.Add(h_box_sizer, proportion=0,flag=wx.LEFT|wx.RIGHT,border=10 )
v_box_sizer.Add(logtext, proportion=0,flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=10)

panel.SetSizer(v_box_sizer)
win.Show()
app.MainLoop()

