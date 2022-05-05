import PySimpleGUIQt as sg
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

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
  
  
def makeText(type=None):
    if type == 'mid':
        return 'l'
    if type == 'right':
        return '                   ....................'
    if type == 'left':
        return '....................                   '
    if type == 'midLR':
        return '...................l...................'
    if type == 'midL':
        return '...................l                   '
    if type == 'midR':
        return '                   l...................'
    if type == 'LR':
        return '.......................................'
    if not type: 
        return '                                       '
    
    return type


def make_window():
    HVIMap = np.full((17,9), [sg.Text(makeText(),justification='c')])
    # mid
    HVIMap[2,:] = sg.Text(makeText('mid'),justification='c')
    for i in range(9):
        HVIMap[4,i] = sg.Text(makeText('X'),justification='c',key = f'_{i}_')
    HVIMap[5,[0,-1,-2]] = sg.Text(makeText('mid'),justification='c')
    HVIMap[6,[0,4,-1,-2]] = sg.Text(makeText('mid'),justification='c')
    HVIMap[8,[2,4,6]] = sg.Text(makeText('mid'),justification='c')
    HVIMap[[10,11,13,14], 4] = sg.Text(makeText('mid'),justification='c')
    # right
    HVIMap[1,[0,3]] = sg.Text(makeText('right'),justification='c')
    # left
    HVIMap[1,[2,8]] = sg.Text(makeText('left'),justification='c')
    # midLR
    HVIMap[1,[1,5]] = sg.Text(makeText('midLR'),justification='c')
    HVIMap[5,2:6] =  sg.Text(makeText('midLR'),justification='c')
    HVIMap[9,4] =  sg.Text(makeText('midLR'),justification='c')
    HVIMap[7,7] =  sg.Text(makeText('midLR'),justification='c')
    # midL
    HVIMap[5,6] =  sg.Text(makeText('midL'),justification='c')
    HVIMap[9,6] =  sg.Text(makeText('midL'),justification='c')
    HVIMap[7,8] =  sg.Text(makeText('midL'),justification='c')
    # midR
    HVIMap[5,1] =  sg.Text(makeText('midR'),justification='c')
    HVIMap[7,0] =  sg.Text(makeText('midR'),justification='c')
    HVIMap[9,2] =  sg.Text(makeText('midR'),justification='c')
    # LR
    HVIMap[1,[4,6,7]] =  sg.Text(makeText('LR'),justification='c')
    HVIMap[7,1] =  sg.Text(makeText('LR'),justification='c')
    HVIMap[9,[3,5]] =  sg.Text(makeText('LR'),justification='c')

    HVIMap[3,0] = sg.FileBrowse(size = (170,40),button_text='LST', target='LST', enable_events = True,button_color=('white', '#C5003C'))
    HVIMap[3,1] = sg.FileBrowse(size = (170,40),button_text='NDVI',target='NDVI', enable_events = True,button_color=('black', 'gold')) 
    HVIMap[3,2] = sg.FileBrowse(size = (170,40),button_text='NDBI',target='NDBI', enable_events = True,button_color=('black', 'gold')) 
    HVIMap[3,3] = sg.FileBrowse(size = (170,40),button_text='Population density',target='Population density', enable_events = True,button_color=('black', 'gold'))  
    HVIMap[3,4] = sg.FileBrowse(size = (170,40),button_text='Age 65+',target='Age 65+', enable_events = True,button_color=('black', 'gold')) 
    HVIMap[3,5] = sg.FileBrowse(size = (170,40),button_text='Age 4-',target='Age 4-', enable_events = True,button_color=('black', 'gold')) 
    HVIMap[3,6] = sg.FileBrowse(size = (170,40),button_text='Population need care',target='Population need care', enable_events = True,button_color=('black', 'gold')) 
    HVIMap[3,7] = sg.FileBrowse(size = (170,40),button_text='Education level',target='Education level', enable_events = True,button_color=('white', 'green')) 
    HVIMap[3,8] = sg.FileBrowse(size = (170,40),button_text='Income level',target='Income level', enable_events = True,button_color=('white', 'green')) 
        
    HVIMap[7,2] = sg.Button(size = (170,40),button_text='Heat Exposure Index',border_width=100, button_color=('white', '#C5003C'))
    HVIMap[7,4] = sg.Button(size = (170,40),button_text='Heat Sensitivity Index',button_color=('black', 'gold'))
    HVIMap[7,6] = sg.Button(size = (170,40),button_text='Adaptive Capability Index',button_color=('white', 'green'))

    HVIMap[12,4] = sg.Button(size = (170,40),button_text='Heat Vulnerability Score',button_color=('white', '#063289'))
    HVIMap[15,4] = sg.Button(size = (170,40),button_text='Heat Vulnerability Index',button_color=('white', '#063289'))

    HVIMap[0,1] = sg.Text(makeText('iGEE'),justification='c')
    HVIMap[0,5] = sg.Text(makeText('ABS'),justification='c')

    Status = [[sg.Text('Status'),sg.ProgressBar(100, orientation = 'h', key='-PROGRESS BAR-'),sg.FolderBrowse(button_text ='Select folder', key ='Output Path',target='Output Path', size=(100,30))]]

    mainFrame =[[sg.Frame('',layout = HVIMap,background_color='white',border_width=0)],[sg.T()],[sg.Frame('',layout =Status)]]
    window = sg.Window('IHVI Toolkit', font=("Helvetica", 10), layout = mainFrame, finalize=True,resizable=False)
    return window


def createErrorWindow(Text):
    errorWindow = sg.Window('Error!',font=("Arial", 11), layout = [[sg.Column([[sg.T()],[sg.Stretch(),sg.Text(Text),sg.Stretch()],[sg.T()],[sg.Stretch(),sg.Button(button_text = 'OK',key='-OK-',size=(100,30)),sg.Stretch()]])]], size = (500,500),finalize=True,resizable=False)
    while True:
        event, values = errorWindow.Read()
        if event == '-OK-' or event == sg.WIN_CLOSED:
            break
    errorWindow.Close()


def checkNoneAndBlack(checkList):
    for e in checkList:
        if e is None:
            return False
        elif e[0] == '':
            return False
        else:
            continue
    return True


def calculateProduct(func, progressbar, LST = None, NDVI= None, NDBI= None, PopDens= None, Age65= None, Age4= None, PopNC= None, EduL= None, IncL= None, OutputPath=None):
    
    # try:   
    
    nameList = np.array(['LST', 'NDVI','NDBI','Population density','Age 65+','Age 4-','Population need care','Education level','Income level'])
    
    def formatting(dataframe_, name):
        dataframe = dataframe_
        dataframe = dataframe.loc[:, ['SA1_7DIG16', 'mean']]
        dataframe.columns = ['SA1_7DIG16', name]
        dataframe[name].fillna(method='ffill', inplace=True)
        return dataframe
    
    def readGroupScaleDataset(dfList_, nameList_ ,progressbar_):
        # read data
        dfList = [pd.read_csv(d) for d in dfList_]
        Cols = ['SA1_7DIG16']
        Cols.extend(nameList_)
        progressbar_.UpdateBar(current_count=10, max=100)
        for i in range(len(dfList)):
            dfList[i] = formatting(dfList[i], nameList_[i]) 
        progressbar_.UpdateBar(current_count=20, max=100)     
        # group data
        df_target_area = dfList[0]
        for i in range(1, len(dfList)):
            df_target_area = df_target_area.merge(dfList[i], how='inner', on='SA1_7DIG16')
        df_target_area.columns = Cols
        progressbar_.UpdateBar(current_count=30, max=100) 
        # scale dataset
        scaler = MinMaxScaler()
        progressbar_.UpdateBar(current_count=40, max=100) 
        scaler.fit(df_target_area.iloc[:,1:])
        df_target_area_scaled = scaler.transform(df_target_area.iloc[:,1:])

        df_target_area_scaled = pd.DataFrame(df_target_area_scaled, columns=Cols[1:])
        
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
        
    if func == 'Heat Sensitivity Index':

        df_target_area, df_target_area_scaled = readGroupScaleDataset([NDVI,NDBI,PopDens,Age65,Age4,PopNC],nameList[1:7].tolist(),progressbar)
        # calculate product
        df_target_area[func] = 1.0/6.0 *df_target_area_scaled[nameList[1:7].tolist()].sum(axis=1)
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
        
    if func == 'Heat Vulnerability Score':
        df_target_area, df_target_area_scaled = readGroupScaleDataset([LST,NDVI,NDBI,PopDens,Age65,Age4,PopNC,EduL, IncL],nameList.tolist(),progressbar)
        # calculate product
        df_target_area['Heat Exposure Index'] = df_target_area_scaled[nameList[0]]
        df_target_area['Heat Sensitivity Index'] = 1.0/6.0 *df_target_area_scaled[nameList[1:7].tolist()].sum(axis=1)
        df_target_area['Adaptive Capability Index'] = 1.0/2.0*df_target_area_scaled[nameList[7:].tolist()].sum(axis=1)
        df_target_area['Heat Vulnerability Score'] = 1.0/3.0 * (df_target_area[['Heat Exposure Index','Heat Sensitivity Index','Adaptive Capability Index']].sum(axis=1))
        progressbar.UpdateBar(current_count=75, max=100) 
        # output
        makeOutput(df_target_area)
        progressbar.UpdateBar(current_count=100, max=100) 
        
    if func == 'Heat Vulnerability Index':
            
        df_target_area, df_target_area_scaled = readGroupScaleDataset([LST,NDVI,NDBI,PopDens,Age65,Age4,PopNC,EduL, IncL],nameList.tolist(),progressbar)
        # calculate product
        df_target_area['Heat Exposure Index'] = df_target_area_scaled[nameList[0]]
        df_target_area['Heat Sensitivity Index'] = 1.0/6.0 *df_target_area_scaled[nameList[1:7].tolist()].sum(axis=1)
        df_target_area['Adaptive Capability Index'] = 1.0/2.0*df_target_area_scaled[nameList[7:].tolist()].sum(axis=1)
        df_target_area['Heat Vulnerability Score'] = 1.0/3.0 * (df_target_area[['Heat Exposure Index','Heat Sensitivity Index','Adaptive Capability Index']].sum(axis=1))
        progressbar.UpdateBar(current_count=60, max=100) 
        # quintile indices
        df_target_area['Heat Vulnerability Index'] = pd.qcut(df_target_area.loc[df_target_area[nameList[3]] != 0, 'Heat Vulnerability Score'], 5, labels=False)
        progressbar.UpdateBar(current_count=70, max=100) 
        # deal with 0
        df_target_area.loc[df_target_area[nameList[3]] != 0, 'Heat Vulnerability Index'] += 1
        df_target_area.loc[df_target_area[nameList[3]] == 0, 'Heat Vulnerability Index'] = 0
        progressbar.UpdateBar(current_count=80, max=100) 
        # output
        makeOutput(df_target_area)
        progressbar.UpdateBar(current_count=100, max=100) 
    # except Exception:
    #     createErrorWindow('Please check your dataset format.')
 
         
def main():
    window = make_window()
    
    func, LST, NDVI, NDBI, PopDens, Age65, Age4, PopNC, EduL, IncL = None, None, None, None, None, None, None, None, None, None
    progress_bar = window.Rows[2][0]._GetElementAtLocation((0,1))

    while True:             # Event Loop
        event, values = window.Read()   
        progress_bar.UpdateBar(current_count =0, max=100)

        if event is None:
            break
        
        if event == sg.WIN_CLOSED:
            break
             
        if event == 'Heat Exposure Index':
            func = event
            if checkNoneAndBlack([values['LST']]):
                LST = values['LST'][0]
                print(func, LST)
                calculateProduct(func, progress_bar, LST = LST, OutputPath=values['Output Path'])
                   
        if event == 'Heat Sensitivity Index':
            func = event
            if checkNoneAndBlack([values['NDVI'],
                          values['NDBI'],
                          values['Population density'],
                          values['Age 65+'],
                          values['Age 4-'],
                          values['Population need care']]):
                NDVI, NDBI, PopDens, Age65, Age4, PopNC, =  values['NDVI'][0],values['NDBI'][0],values['Population density'][0],values['Age 65+'][0],values['Age 4-'][0],values['Population need care'][0]
                calculateProduct(func, progress_bar, NDVI= NDVI, NDBI= NDBI, PopDens= PopDens, Age65= Age65, Age4= Age4, PopNC= PopNC, OutputPath=values['Output Path'])
                
              
        if event == 'Adaptive Capability Index':
            func = event
            if checkNoneAndBlack([values['Education level'],values['Income level']]):
                EduL, IncL = values['Education level'][0],values['Income level'][0]
                calculateProduct(func, progress_bar, EduL= EduL, IncL= IncL,OutputPath=values['Output Path'])
  
                
        if event == 'Heat Vulnerability Score':
             
            func = event
            if checkNoneAndBlack([values['LST' ],values['NDVI' ],values['NDBI' ],values['Population density' ],values['Age 65+' ],values['Age 4-' ],values['Population need care' ],values['Education level' ],values['Income level' ]]):
                LST, NDVI, NDBI, PopDens, Age65, Age4, PopNC, EduL, IncL = values['LST'][0],values['NDVI'][0],values['NDBI'][0],values['Population density'][0],values['Age 65+'][0],values['Age 4-'][0],values['Population need care'][0],values['Education level'][0],values['Income level'][0]
                calculateProduct(func, progress_bar, LST = LST, NDVI= NDVI, NDBI= NDBI, PopDens= PopDens, Age65= Age65, Age4= Age4, PopNC= PopNC, EduL= EduL, IncL= IncL,OutputPath=values['Output Path'])

                
        if event == 'Heat Vulnerability Index':
             
            func = event
            if checkNoneAndBlack([values['LST' ],values['NDVI' ],values['NDBI' ],values['Population density' ],values['Age 65+' ],values['Age 4-' ],values['Population need care' ],values['Education level' ],values['Income level' ]]):
                LST, NDVI, NDBI, PopDens, Age65, Age4, PopNC, EduL, IncL = values['LST'][0],values['NDVI'][0],values['NDBI'][0],values['Population density'][0],values['Age 65+'][0],values['Age 4-'][0],values['Population need care'][0],values['Education level'][0],values['Income level'][0]
                calculateProduct(func, progress_bar, LST = LST, NDVI= NDVI, NDBI= NDBI, PopDens= PopDens, Age65= Age65, Age4= Age4, PopNC= PopNC, EduL= EduL, IncL= IncL,OutputPath=values['Output Path'])

        for e in fileIndex.keys():
            if values[e] is None or values[e] == ('', ''):
                window.Rows[0][0]._GetElementAtLocation((4,fileIndex[e])).Update(value='X')
            else:
                window.Rows[0][0]._GetElementAtLocation((4,fileIndex[e])).Update(value='l')
        
    
    window.Close()


if __name__ == '__main__':
    # sg.theme('black')
    sg.theme('Default1')
    # sg.theme('dark green 7')
    main()
    try:   
        main()
    except Exception:
        createErrorWindow('Unexpected error.')