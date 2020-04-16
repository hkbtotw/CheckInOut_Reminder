#### Work with environment  conda checkio, python=3.6

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date, datetime
import pytz

colDict={
    'Date':1,
    'Time_In':2,
    'Check_In':3,
    'Time_Out':4,
    'Check_Out':5,
    'Load':6   
}


class Update_Time(object):
    def __init__(self):
        self.secret_path_1=r'C:/Users/70018928/Documents/GitHub/CheckInOut_Reminder/CheckInOutReminder-e2ff28c53e80.json'
        self.secret_path_2=r'./CheckInOutReminder-e2ff28c53e80.json'
        self.scope= ['https://spreadsheets.google.com/feeds',
                              'https://www.googleapis.com/auth/drive']

    def Authorization(self):
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(self.secret_path_1, self.scope)
        except:
            creds = ServiceAccountCredentials.from_json_keyfile_name(self.secret_path_2, self.scope)
        client = gspread.authorize(creds) 
        sheet = client.open("WFH_CheckInOut").sheet1
        return sheet

    def InsertNewValue_In(self,todayStr, nowDate, nowTime, sheet):
        lenRecords=len(sheet.get_all_values())
        list_of_hashes=sheet.get_all_records()
        lenHash=len(list_of_hashes)
        print(" len : ",lenRecords)
        lastDate=sheet.cell(lenRecords,1).value
        print(' lastDate : ',lastDate)
        lenDate=len(list_of_hashes[lenHash-1]['Date'])
        if(todayStr != lastDate):
            if(lenDate==0):
                todayRow=lenRecords
            else:
                todayRow=lenRecords+1
            row_index=todayRow
            
            ## previous load
            col_index=colDict['Load']
            try:
                previousLoad=sheet.cell(row_index,col_index).value
            except:
                previousLoad=0
            if(previousLoad==None or previousLoad==''):
                previousLoad=0
            print(' previousLoad : ',previousLoad)
            currentLoad=int(previousLoad)+1
            message=currentLoad
            sheet.update_cell(row_index, col_index,message)
            print('Check_In Input recorded')
            if(currentLoad>1):
                todayRow=lenRecords
                row_index=todayRow
                col_index=colDict['Date']
                message=todayStr
                sheet.update_cell(row_index, col_index,message)
                col_index=colDict['Time_In']
                message=nowTime
                sheet.update_cell(row_index, col_index,message)
                col_index=colDict['Check_In']
                message="Yes"
                sheet.update_cell(row_index, col_index,message)
                print(' record new update')
                ## previous load
                col_index=colDict['Load']
                try:
                    previousLoad=sheet.cell(row_index,col_index).value
                except:
                    previousLoad=0
                if(previousLoad==None or previousLoad==''):
                    previousLoad=0
                print(' previousLoad : ',previousLoad)
                currentLoad=int(previousLoad)+1
                message=currentLoad
                sheet.update_cell(row_index, col_index,message)
            else:
                print(' refresh does not count')

        else:
            print('Not Updated')
    
    def InsertNewValue_Out(self,todayStr, nowDate, nowTime, sheet):
        lenRecords=len(sheet.get_all_values())
        print(" len : ",lenRecords)
        lastDate=sheet.cell(lenRecords,1).value
        print(' lastDate : ',lastDate)
        if(todayStr == lastDate and len(sheet.cell(lenRecords,colDict['Time_In']).value)>1 ):
            todayRow=lenRecords
            row_index=todayRow
            col_index=colDict['Time_Out']
            message=nowTime
            sheet.update_cell(row_index, col_index,message)
            col_index=colDict['Check_Out']
            message="Yes"
            sheet.update_cell(row_index, col_index,message)
            print('Check_Out Input recorded')
        else:
            print('Not Updated')

    def GetDateTime(self):
        todayUTC=datetime.today()
        nowUTC=datetime.now()
        # dd/mm/YY H:M:S
        to_zone = pytz.timezone('Asia/Bangkok')

        today=todayUTC.astimezone(to_zone)
        now=nowUTC.astimezone(to_zone)

        todayStr=today.strftime("%Y-%m-%d")
        nowDate = now.strftime("%Y-%m-%d")
        nowTime = now.strftime("%H:%M:%S")

        print(' today : ',todayStr)
        print(nowDate, ' ==> ', nowTime)
        return todayStr, nowDate, nowTime

    def ReadCurrentStatus(self,todayStr, nowDate, nowTime, sheet):
        lenRecords=len(sheet.get_all_values())
        print(" len : ",lenRecords)
        lastDate=sheet.cell(lenRecords,1).value
        print(' lastDate : ',lastDate)
        list_of_hashes=sheet.get_all_records()
        lenHash=len(list_of_hashes)
        lastDate=sheet.cell(lenRecords,1).value
        lenDate=len(list_of_hashes[lenHash-1]['Date'])
        if(todayStr != lastDate):
            checkIn=0
            checkOut=0
        else:
            col_index=colDict['Check_In']
            updStatus=sheet.cell(lenRecords,col_index).value
            if(updStatus=="Yes"):
                checkIn=1
            else:
                checkIn=0
            col_index=colDict['Check_Out']
            updStatus=sheet.cell(lenRecords,col_index).value
            if(updStatus=="Yes"):
                checkOut=1
            else:
                checkOut=0
                

        print(' cio : ', checkIn, ' ::' , checkOut)

        return checkIn, checkOut


