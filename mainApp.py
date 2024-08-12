
'''
Copyright (C) AURIN

'''

import PySimpleGUIQt as sg
import pandas as pd
import numpy as np
import webbrowser
import sys
import os
from ctypes import windll
from jenkspy import JenksNaturalBreaks
import traceback

def get_ppi():
    LOGPIXELSX = 88
    LOGPIXELSY = 90
    user32 = windll.user32
    user32.SetProcessDPIAware()
    dc = user32.GetDC(0)   
    pix_per_inch = windll.gdi32.GetDeviceCaps(dc, LOGPIXELSX)
    print("Horizontal DPI is", windll.gdi32.GetDeviceCaps(dc, LOGPIXELSX))
    print("Vertical DPI is", windll.gdi32.GetDeviceCaps(dc, LOGPIXELSY))
    user32.ReleaseDC(0, dc)
    return pix_per_inch

fileIndex = {
   'LST': 0, 
   'NDVI': 1, 
   'NDBI': 2, 
   'Population density': 3, 
   'Age 65+': 4, 
   'Age 4-': 5, 
   'Population need care': 6, 
   'Education level': 7, 
   'Income level': 8 
}
# implement min max scaler for normalization
class minMaxScaler:
    def __init__(self):
        self.scaler = None

    def fit(self, dataframe):
        cols = dataframe.shape[1]
        self.scaler = np.array([[dataframe.iloc[:, i].min(), dataframe.iloc[:, i].max()] for i in range(cols)])
    
    def normalize(self, dataframe, columnIndices):
        arr = np.array(dataframe)
        rowIndices = columnIndices
        arr = arr.astype(np.float32)
        
        for i in rowIndices:
            minV = float(self.scaler[i, 0])
            maxV = float(self.scaler[i, 1])
            if maxV - minV != 0:
                arr[:,i] = (arr[:,i] - minV)/(maxV - minV)
            else:
                arr[:,i] = 1
        return arr
        
# text formatter for text components
def makeText(type=None):
    if type == 'mid':
        return 'l'
    if type == 'right':
        return '                  ...................'
    if type == 'left':
        return '...................                  '
    if type == 'midLR':
        return '..................l..................'
    if type == 'midL':
        return '..................l                  '
    if type == 'midR':
        return '                  l..................'
    if type == 'LR':
        return '.....................................'
    if not type: 
        return '                                     '
    
    return type

# relative path of the files
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# make UI
def make_window(dpi):
    dotSize = (170,20)
    HVIMap = np.full((17,9), [sg.Text(makeText(),size =dotSize,justification='c')])
    # mid
    HVIMap[2,:] = sg.Text(makeText('mid'),size =dotSize,justification='c')
    for i in range(9):
        HVIMap[4,i] = sg.Text(makeText('X'),size =dotSize,justification='c',key = f'_{i}_')
    HVIMap[5,[0,-1,-2]] = sg.Text(makeText('mid'),size =dotSize,justification='c')
    HVIMap[6,[0,4,-1,-2]] = sg.Text(makeText('mid'),size =dotSize,justification='c')
    HVIMap[8,[2,4,6]] = sg.Text(makeText('mid'),size =dotSize,justification='c')
    HVIMap[[10,11,13,14], 4] = sg.Text(makeText('mid'),size =dotSize,justification='c')
    # right
    HVIMap[1,[0,3]] = sg.Text(makeText('right'),size =dotSize,justification='c')
    # left
    HVIMap[1,[2,8]] = sg.Text(makeText('left'),size =dotSize,justification='c')
    # midLR
    HVIMap[1,[1,5]] = sg.Text(makeText('midLR'),size =dotSize,justification='c')
    HVIMap[5,2:6] =  sg.Text(makeText('midLR'),size =dotSize,justification='c')
    HVIMap[9,4] =  sg.Text(makeText('midLR'),size =dotSize,justification='c')
    HVIMap[7,7] =  sg.Text(makeText('midLR'),size =dotSize,justification='c')
    # midL
    HVIMap[5,6] =  sg.Text(makeText('midL'),size =dotSize,justification='c')
    HVIMap[9,6] =  sg.Text(makeText('midL'),size =dotSize,justification='c')
    HVIMap[7,8] =  sg.Text(makeText('midL'),size =dotSize,justification='c')
    # midR
    HVIMap[5,1] =  sg.Text(makeText('midR'),size =dotSize,justification='c')
    HVIMap[7,0] =  sg.Text(makeText('midR'),size =dotSize,justification='c')
    HVIMap[9,2] =  sg.Text(makeText('midR'),size =dotSize,justification='c')
    # LR
    HVIMap[1,[4,6,7]] =  sg.Text(makeText('LR'),size =dotSize,justification='c')
    HVIMap[7,1] =  sg.Text(makeText('LR'),size =dotSize,justification='c')
    HVIMap[9,[3,5]] =  sg.Text(makeText('LR'),size =dotSize,justification='c')
    # file input
    textSize = (170,40)
    textFont = ("Helvetica", 48 * 20 /dpi)
    HVIMap[3,0] = sg.FileBrowse(size = textSize, font=textFont, button_text='LST', target='LST', enable_events = True,button_color=('white', '#C5003C'))
    HVIMap[3,1] = sg.FileBrowse(size = textSize, font=textFont, button_text='NDVI',target='NDVI', enable_events = True,button_color=('black', 'gold')) 
    HVIMap[3,2] = sg.FileBrowse(size = textSize, font=textFont, button_text='NDBI',target='NDBI', enable_events = True,button_color=('black', 'gold')) 
    HVIMap[3,3] = sg.FileBrowse(size = textSize, font=textFont, button_text='Population density',target='Population density', enable_events = True,button_color=('black', 'gold'))  
    HVIMap[3,4] = sg.FileBrowse(size = textSize, font=textFont, button_text='Age 65+',target='Age 65+', enable_events = True,button_color=('black', 'gold')) 
    HVIMap[3,5] = sg.FileBrowse(size = textSize, font=textFont, button_text='Age 4-',target='Age 4-', enable_events = True,button_color=('black', 'gold')) 
    HVIMap[3,6] = sg.FileBrowse(size = textSize, font=textFont, button_text='Population need care',target='Population need care', enable_events = True,button_color=('black', 'gold')) 
    HVIMap[3,7] = sg.FileBrowse(size = textSize, font=textFont, button_text='Education level',target='Education level', enable_events = True,button_color=('white', 'green')) 
    HVIMap[3,8] = sg.FileBrowse(size = textSize, font=textFont, button_text='Income level',target='Income level', enable_events = True,button_color=('white', 'green')) 
    # functional buttons - calculation
    HVIMap[7,2] = sg.Button(size = textSize, font=textFont, button_text='Heat Exposure Index',border_width=100, button_color=('white', '#C5003C'))
    HVIMap[7,4] = sg.Button(size = textSize, font=textFont, button_text='Heat Sensitivity Index',button_color=('black', 'gold'))
    HVIMap[7,6] = sg.Button(size = textSize, font=textFont, button_text='Adaptive Capability Index',button_color=('white', 'green'))
    
    HVIMap[12,4] = sg.Button(size = textSize, font=textFont, button_text='Heat Vulnerability Score',button_color=('white', '#063289'))
    HVIMap[15,4] = sg.Button(size = textSize, font=textFont, button_text='Heat Vulnerability Index',button_color=('white', '#063289'))

    HVIMap[0,1] = sg.Button(size = textSize, font=textFont, button_text='iGEE',button_color=('black', '#FFFAF0'))
    HVIMap[0,5] = sg.Button(size = textSize, font=textFont, button_text='ABS',button_color=('black', '#FFFAF0'))
    textFont_ = ("Helvetica", 48 * 30 /dpi)
    # progress bar and select output path
    Status = [[sg.Text('Status', font=textFont_),sg.ProgressBar(100, orientation = 'h', key='-PROGRESS BAR-'),sg.FolderBrowse(button_text ='Select folder', key ='Output Path',target='Output Path', size=(170,40), font=textFont_)]]
    mainFrame =[[sg.Frame('',element_justification='c',layout = HVIMap,background_color='white',border_width=0)],[sg.T()],[sg.Frame('',layout =Status)],[sg.Stretch(),sg.Text('AURIN | RMIT @ GISALL © 2024',text_color='Gray',font=("Helvetica", 8)),sg.Stretch()]]
    window = sg.Window('IHVI Toolkit', font=("Helvetica", 10), icon= resource_path('logo.ico'), layout = mainFrame, finalize=True,resizable=True)
    return window

# error windows
def createErrorWindow(Text):
    errorWindow = sg.Window('Error!',font=("Arial", 11),icon=resource_path('warning.ico'), layout = [[sg.Column([[sg.T()],[sg.Stretch(),sg.Text(Text),sg.Stretch()],[sg.T()],[sg.Stretch(),sg.Button(button_text = 'OK',key='-OK-',size=(100,30)),sg.Stretch()]])]], size = (500,500),finalize=True,resizable=False)
    while True:
        event, values = errorWindow.Read()
        if event == '-OK-' or event == sg.WIN_CLOSED:
            break
    errorWindow.Close()

# information windows
def createInforWindow(Text):
    errorWindow = sg.Window('Information',font=("Arial", 11),icon=resource_path('logo.ico'), layout = [[sg.Column([[sg.T()],[sg.Stretch(),sg.Text(Text),sg.Stretch()],[sg.T()],[sg.Stretch(),sg.Button(button_text = 'OK',key='-OK-',size=(100,30)),sg.Stretch()]])]], size = (500,500),finalize=True,resizable=False)
    while True:
        event, values = errorWindow.Read()
        if event == '-OK-' or event == sg.WIN_CLOSED:
            break
    errorWindow.Close()

# check none for reuse
def checkNoneAndBlank(checkList):
    for e in checkList:
        if e is None:
            return False
        elif e[0] == '':
            return False
        else:
            continue
    return True

# main calculation function
def calculateProduct(func, progressbar, LST = None, NDVI= None, NDBI= None, PopDens= None, Age65= None, Age4= None, PopNC= None, EduL= None, IncL= None, OutputPath=None):
    
    try:   
        nameList = np.array(['LST', 'NDVI','NDBI','Population density','Age 65+','Age 4-','Population need care','Education level','Income level'])
        
        def formatting(dataframe_, name):
            dataframe = dataframe_
            dataframe = dataframe.loc[:, ['SA1_CODE21', 'mean']]
            dataframe.columns = ['SA1_CODE21', name]
            dataframe[name].fillna(method='ffill', inplace=True)
            return dataframe
        
        def readGroupScaleDataset(dfList_, nameList_ ,progressbar_):
            # read data
            dfList = [pd.read_csv(d) for d in dfList_]
            Cols = ['SA1_CODE21']
            Cols.extend(nameList_)
            progressbar_.UpdateBar(current_count=10, max=100)
            for i in range(len(dfList)):
                dfList[i] = formatting(dfList[i], nameList_[i]) 
            progressbar_.UpdateBar(current_count=20, max=100)     
            # group data
            df_target_area = dfList[0]
            for i in range(1, len(dfList)):
                df_target_area = df_target_area.merge(dfList[i], how='inner', on='SA1_CODE21')
            df_target_area.columns = Cols
            progressbar_.UpdateBar(current_count=30, max=100) 
            # scale dataset
            scaler = minMaxScaler()
            progressbar_.UpdateBar(current_count=40, max=100) 
            scaler.fit(df_target_area)

            df_target_area_scaled = scaler.normalize(df_target_area, list(range(1, df_target_area.shape[1])))

            df_target_area_scaled = pd.DataFrame(df_target_area_scaled, columns=Cols)
            
            progressbar_.UpdateBar(current_count=50, max=100) 
            return df_target_area, df_target_area_scaled
        
        def makeOutput(df_target_area):
            outputpath = f'{func}.csv' if not OutputPath else f'{OutputPath}/{func}.csv'
            df_target_area.to_csv(outputpath, index=None)
        
        if func == 'Heat Exposure Index':

            df_target_area, df_target_area_scaled = readGroupScaleDataset([LST],[nameList[0]],progressbar)
            # calculate product
            df_target_area[func] = df_target_area_scaled[nameList[0]]
            progressbar.UpdateBar(current_count=75, max=100) 
            # output
            makeOutput(df_target_area)
            progressbar.UpdateBar(current_count=100, max=100) 
            
        # if func == 'Heat Sensitivity Index':

        #     df_target_area, df_target_area_scaled = readGroupScaleDataset([NDVI,NDBI,PopDens,Age65,Age4,PopNC],nameList[1:7].tolist(),progressbar)
        #     # calculate product
        #     df_target_area[func] = 1.0/6.0 *df_target_area_scaled[nameList[1:7].tolist()].sum(axis=1)
        #     progressbar.UpdateBar(current_count=75, max=100) 
        #     # output
        #     makeOutput(df_target_area)
        #     progressbar.UpdateBar(current_count=100, max=100) 

        ## calculation formula changed
        if func == 'Heat Sensitivity Index':
            df_target_area, df_target_area_scaled = readGroupScaleDataset([NDVI,NDBI,PopDens,Age65,Age4,PopNC],nameList[1:7].tolist(),progressbar)
            # calculate product
            df_target_area[func] = 1.0/6.0 * df_target_area_scaled[nameList[2:7].tolist()].sum(axis=1)-df_target_area_scaled[nameList[1].tolist()]
            progressbar.UpdateBar(current_count=75, max=100) 
            # output
            makeOutput(df_target_area)
            progressbar.UpdateBar(current_count=100, max=100) 
            
        if func == 'Adaptive Capability Index':
            df_target_area, df_target_area_scaled = readGroupScaleDataset([EduL, IncL],nameList[7:].tolist(),progressbar)
            # calculate product
            df_target_area[func] = 1.0/2.0*df_target_area_scaled[nameList[7:].tolist()].sum(axis=1)
            progressbar.UpdateBar(current_count=75, max=100) 
            # output
            makeOutput(df_target_area)
            progressbar.UpdateBar(current_count=100, max=100) 
            
        # if func == 'Heat Vulnerability Score':
        #     df_target_area, df_target_area_scaled = readGroupScaleDataset([LST,NDVI,NDBI,PopDens,Age65,Age4,PopNC,EduL, IncL],nameList.tolist(),progressbar)
        #     # calculate product
        #     df_target_area['Heat Exposure Index'] = df_target_area_scaled[nameList[0]]
        #     df_target_area['Heat Sensitivity Index'] = 1.0/6.0 *df_target_area_scaled[nameList[1:7].tolist()].sum(axis=1)
        #     df_target_area['Adaptive Capability Index'] = 1.0/2.0*df_target_area_scaled[nameList[7:].tolist()].sum(axis=1)
        #     df_target_area['Heat Vulnerability Score'] = 1.0/3.0 * (df_target_area[['Heat Exposure Index','Heat Sensitivity Index','Adaptive Capability Index']].sum(axis=1))
        #     progressbar.UpdateBar(current_count=75, max=100) 
        #     # output
        #     makeOutput(df_target_area)
        #     progressbar.UpdateBar(current_count=100, max=100) 

        ## calculation formula changed    
        if func == 'Heat Vulnerability Score':
            df_target_area, df_target_area_scaled = readGroupScaleDataset([LST,NDVI,NDBI,PopDens,Age65,Age4,PopNC,EduL, IncL],nameList.tolist(),progressbar)
            # calculate product   
            df_target_area['Heat Exposure Index'] = df_target_area_scaled[nameList[0]]
            df_target_area['Heat Sensitivity Index'] = 1.0/6.0 *df_target_area_scaled[nameList[2:7].tolist()].sum(axis=1)-df_target_area_scaled[nameList[1].tolist()]
            df_target_area['Adaptive Capability Index'] = 1.0/2.0*df_target_area_scaled[nameList[7:].tolist()].sum(axis=1)
            df_target_area['Heat Vulnerability Score'] = 1.0/3.0 * (df_target_area[['Heat Exposure Index','Heat Sensitivity Index']].sum(axis=1) - pd.Series(df_target_area['Adaptive Capability Index']))
            progressbar.UpdateBar(current_count=75, max=100) 
            # output
            makeOutput(df_target_area)
            progressbar.UpdateBar(current_count=100, max=100) 
            
        # if func == 'Heat Vulnerability Index':
                
        #     df_target_area, df_target_area_scaled = readGroupScaleDataset([LST,NDVI,NDBI,PopDens,Age65,Age4,PopNC,EduL, IncL],nameList.tolist(),progressbar)
        #     # calculate product
        #     df_target_area['Heat Exposure Index'] = df_target_area_scaled[nameList[0]]
        #     df_target_area['Heat Sensitivity Index'] = 1.0/6.0 *df_target_area_scaled[nameList[1:7].tolist()].sum(axis=1)
        #     df_target_area['Adaptive Capability Index'] = 1.0/2.0*df_target_area_scaled[nameList[7:].tolist()].sum(axis=1)
        #     df_target_area['Heat Vulnerability Score'] = 1.0/3.0 * (df_target_area[['Heat Exposure Index','Heat Sensitivity Index','Adaptive Capability Index']].sum(axis=1))
        #     progressbar.UpdateBar(current_count=60, max=100) 
        #     # quintile indices
        #     df_target_area['Heat Vulnerability Index'] = pd.qcut(df_target_area.loc[df_target_area[nameList[3]] != 0, 'Heat Vulnerability Score'], 5, labels=False)
        #     progressbar.UpdateBar(current_count=70, max=100) 
        #     # deal with 0
        #     df_target_area.loc[df_target_area[nameList[3]] != 0, 'Heat Vulnerability Index'] += 1
        #     df_target_area.loc[df_target_area[nameList[3]] == 0, 'Heat Vulnerability Index'] = 0
        #     progressbar.UpdateBar(current_count=80, max=100) 
        #     # output
        #     makeOutput(df_target_area)
        #     progressbar.UpdateBar(current_count=100, max=100) 

        ## calculation formula changed 
        if func == 'Heat Vulnerability Index':
                
            df_target_area, df_target_area_scaled = readGroupScaleDataset([LST,NDVI,NDBI,PopDens,Age65,Age4,PopNC,EduL, IncL],nameList.tolist(),progressbar)
            # calculate product
            df_target_area['Heat Exposure Index'] = df_target_area_scaled[nameList[0]]
            df_target_area['Heat Sensitivity Index'] = 1.0/6.0 *df_target_area_scaled[nameList[2:7].tolist()].sum(axis=1)-df_target_area_scaled[nameList[1].tolist()]
            df_target_area['Adaptive Capability Index'] = 1.0/2.0*df_target_area_scaled[nameList[7:].tolist()].sum(axis=1)
            df_target_area['Heat Vulnerability Score'] = 1.0/3.0 * (df_target_area[['Heat Exposure Index','Heat Sensitivity Index']].sum(axis=1)- pd.Series(df_target_area['Adaptive Capability Index']))
            progressbar.UpdateBar(current_count=60, max=100) 
            ## quintile method changed to Natural Breaks
            jnb = JenksNaturalBreaks(5)
            jnb.fit(df_target_area.loc[df_target_area[nameList[3]] != 0, 'Heat Vulnerability Score'])
            df_target_area.loc[df_target_area[nameList[3]] != 0, 'Heat Vulnerability Index'] = jnb.labels_
            progressbar.UpdateBar(current_count=70, max=100) 
            # deal with 0
            df_target_area.loc[df_target_area[nameList[3]] != 0, 'Heat Vulnerability Index'] += 1
            df_target_area.loc[df_target_area[nameList[3]] == 0, 'Heat Vulnerability Index'] = 0
            progressbar.UpdateBar(current_count=80, max=100) 
            # output
            makeOutput(df_target_area)
            progressbar.UpdateBar(current_count=100, max=100) 
        
    # catch exception
    except Exception: 
        traceback.print_exc()
        createErrorWindow('Please check your dataset format.')
 
         
def main():
    window = make_window(get_ppi())
    # initiate variables
    func, LST, NDVI, NDBI, PopDens, Age65, Age4, PopNC, EduL, IncL = None, None, None, None, None, None, None, None, None, None
    progress_bar = window.Rows[2][0]._GetElementAtLocation((0,1))

    while True:             # Event Loop
        # read events
        event, values = window.Read()   
        progress_bar.UpdateBar(current_count =0, max=100)

        if event is None:
            break
        
        if event == sg.WIN_CLOSED:
            break
             
        if event == 'Heat Exposure Index':
            func = event
            if checkNoneAndBlank([values['LST']]):
                LST = values['LST'][0]
                print(func, LST)
                calculateProduct(func, progress_bar, LST = LST, OutputPath=values['Output Path'])
                   
        if event == 'Heat Sensitivity Index':
            func = event
            if checkNoneAndBlank([values['NDVI'],
                          values['NDBI'],
                          values['Population density'],
                          values['Age 65+'],
                          values['Age 4-'],
                          values['Population need care']]):
                NDVI, NDBI, PopDens, Age65, Age4, PopNC, =  values['NDVI'][0],values['NDBI'][0],values['Population density'][0],values['Age 65+'][0],values['Age 4-'][0],values['Population need care'][0]
                calculateProduct(func, progress_bar, NDVI= NDVI, NDBI= NDBI, PopDens= PopDens, Age65= Age65, Age4= Age4, PopNC= PopNC, OutputPath=values['Output Path'])
                
              
        if event == 'Adaptive Capability Index':
            func = event
            if checkNoneAndBlank([values['Education level'],values['Income level']]):
                EduL, IncL = values['Education level'][0],values['Income level'][0]
                calculateProduct(func, progress_bar, EduL= EduL, IncL= IncL,OutputPath=values['Output Path'])
  
                
        if event == 'Heat Vulnerability Score':
             
            func = event
            if checkNoneAndBlank([values['LST' ],values['NDVI' ],values['NDBI' ],values['Population density' ],values['Age 65+' ],values['Age 4-' ],values['Population need care' ],values['Education level' ],values['Income level' ]]):
                LST, NDVI, NDBI, PopDens, Age65, Age4, PopNC, EduL, IncL = values['LST'][0],values['NDVI'][0],values['NDBI'][0],values['Population density'][0],values['Age 65+'][0],values['Age 4-'][0],values['Population need care'][0],values['Education level'][0],values['Income level'][0]
                calculateProduct(func, progress_bar, LST = LST, NDVI= NDVI, NDBI= NDBI, PopDens= PopDens, Age65= Age65, Age4= Age4, PopNC= PopNC, EduL= EduL, IncL= IncL,OutputPath=values['Output Path'])

                
        if event == 'Heat Vulnerability Index':
             
            func = event
            if checkNoneAndBlank([values['LST' ],values['NDVI' ],values['NDBI' ],values['Population density' ],values['Age 65+' ],values['Age 4-' ],values['Population need care' ],values['Education level' ],values['Income level' ]]):
                LST, NDVI, NDBI, PopDens, Age65, Age4, PopNC, EduL, IncL = values['LST'][0],values['NDVI'][0],values['NDBI'][0],values['Population density'][0],values['Age 65+'][0],values['Age 4-'][0],values['Population need care'][0],values['Education level'][0],values['Income level'][0]
                calculateProduct(func, progress_bar, LST = LST, NDVI= NDVI, NDBI= NDBI, PopDens= PopDens, Age65= Age65, Age4= Age4, PopNC= PopNC, EduL= EduL, IncL= IncL,OutputPath=values['Output Path'])

            print(func)
            
        if event == 'iGEE':
            webbrowser.open('http://www.gisonmeta.com')

        if event == 'ABS':
            webbrowser.open('https://www.abs.gov.au/census')
        
        for e in fileIndex.keys():
            if values[e] is None or values[e] == ('', ''):
                window.Rows[0][0]._GetElementAtLocation((4,fileIndex[e])).Update(value='X')
            else:
                window.Rows[0][0]._GetElementAtLocation((4,fileIndex[e])).Update(value='l')
        

        
    window.Close()


if __name__ == '__main__':
    # sg.theme('black')
    # print(get_ppi())
    sg.theme('Default1')
    # sg.theme('dark green 7')
    try:        
        main()
    except Exception:
        createErrorWindow('Unexpected error.')