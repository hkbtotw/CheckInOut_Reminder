#### Work with environment  conda checkio, python=3.6

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from datetime import date, datetime

secret_path=r'C:/Users/70018928/Documents/GitHub/CheckInOut_Reminder/CheckInOutReminder-e2ff28c53e80.json'
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(secret_path, scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("WFH_CheckInOut").sheet1

colDict={
    'Date':1,
    'Time_In':2,
    'Check_In':3,
    'Time_Out':4,
    'Check_Out':5   
}

def InsertNewValue_In(todayStr, nowDate, nowTime):
    lenRecords=len(sheet.get_all_values())
    print(" len : ",lenRecords)
    lastDate=sheet.cell(lenRecords,1).value
    print(' lastDate : ',lastDate)
    if(todayStr != lastDate):
        todayRow=lenRecords+1
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
        print('Check_In Input recorded')
    else:
        print('Not Updated')
    
def InsertNewValue_Out(todayStr, nowDate, nowTime):
    lenRecords=len(sheet.get_all_values())
    print(" len : ",lenRecords)
    lastDate=sheet.cell(lenRecords,1).value
    print(' lastDate : ',lastDate)
    if(todayStr == lastDate and len(sheet.cell(lenRecords,colDict['Time_In']).value)>1):
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

def GetDateTime():
    today=date.today()
    now=datetime.now()
    # dd/mm/YY H:M:S
    todayStr=today.strftime("%Y-%m-%d")
    nowDate = now.strftime("%Y-%m-%d")
    nowTime = now.strftime("%H:%M:%S")

    print(' today : ',todayStr)
    print(nowDate, ' ==> ', nowTime)
    return todayStr, nowDate, nowTime

todayStr, nowDate, nowTime=GetDateTime()
InsertNewValue_Out(todayStr, nowDate, nowTime)
InsertNewValue_In(todayStr, nowDate, nowTime)


