

class zb:
    def __init__(self):
        None




    def zbwrite(self,zbwrite,taskid):
        self.file =open('zblog/basic_type'+str(taskid)+'.txt','w')
        self.file.write(zbwrite)
        self.file.close()

    def zbread(self,taskid):
        try:

            self.file =open('zblog/basic_type'+str(taskid)+'.txt')
        except:
            self.zbwrite('',taskid)
            self.file =open('zblog/basic_type'+str(taskid)+'.txt')

        return self.file.read()
        self.file.close()
    def zbclose(self):
        self.file.close()
class date:
    def __init__(self):
        None




    def datewrite(self,datewrite,date):
        datewrite=self.dateread(date)+str(datewrite)
        self.file =open('datelog/'+str(date)+'.txt','w')


        self.file.write(datewrite)
        self.file.close()
    def datetxtread(self,date):
        try:

            self.file =open('datelog/'+str(date))
        except:
            return ''

        return self.file.read()
        self.file.close()
    def dateread(self,date):
        try:

            self.file =open('datelog/'+str(date)+'.txt')
        except:
            self.file =open('datelog/'+str(date)+'.txt','w')
            self.file.write('')
            self.file.close()
            self.file =open('datelog/'+str(date)+'.txt')

        return self.file.read()
        self.file.close()
    def dateclose(self):
        self.file.close()

