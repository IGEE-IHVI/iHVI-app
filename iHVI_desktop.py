import PySimpleGUI as sg
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


"""
    Copyright 2022 PySimpleGUI
"""

NAME_SIZE = 50


def make_window(theme=None):

    def name(name):
        dots = NAME_SIZE-len(name)-2
        return sg.Text(name + ' ' + ' '*dots, size=(NAME_SIZE, 1), justification='r', pad=(0, 0), font='Courier 10')

    sg.theme(theme)

    layout_l = [[sg.T("")], [sg.Text("Input LST File Path: ")], [sg.Input(), sg.FileBrowse()],
                [sg.T("")], [sg.Text("Input NDBI File Path: ")], [sg.Input(), sg.FileBrowse()],
                [sg.T("")], [sg.Text("Input NDVI File Path: ")], [sg.Input(), sg.FileBrowse()],
                [sg.T("")], [sg.Text("Input Other Parameters File Path: ")], [sg.Input(), sg.FileBrowse()],
                [sg.T("")], [sg.Text("Output File Path: ")], [sg.Input(), sg.FolderBrowse()],
                [sg.T("")], [sg.Button('Start'), sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS BAR-')]]
    descriptive_layout = [[sg.T('Upcoming features!')]]

    menu_def = [['&Application', ['E&xit']],
                ['&Help', ['&About']]]

    layout = [
        [sg.MenubarCustom(menu_def, key='-MENU-', font='Courier 15', tearoff=True)]]
    layout += [[sg.TabGroup([[sg.Tab('iHVI', layout_l),
                             sg.Tab('Descriptive Stats', descriptive_layout)]], key='-TAB GROUP-', expand_x=True, expand_y=True),
                
                ]]
    window = sg.Window('IHVI Toolkit', layout, finalize=True,
                       right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_EXIT)

    return window


def calculateIHVI(LST, NDBI, NDVI, OtherSix, directory, progressbar):

    progressbar.update(current_count=1)
    filepath1 = LST
    filepath2 = NDBI
    filepath3 = NDVI
    filepath4 = OtherSix

    # read data
    df_other_6 = pd.read_csv(filepath4)
    # pd.read_pickle("./othersixparas.pkl")
    df_B_LST = pd.read_csv(filepath1)
    progressbar.update(current_count=5)
    df_B_NDBI = pd.read_csv(filepath2)
    progressbar.update(current_count=15)
    df_B_NDVI = pd.read_csv(filepath3)
    progressbar.update(current_count=20)

    def unifycolumns(dataset, word):
        cols = list(dataset.columns)
        newcols = [word if word in col else col for col in cols]
        dataset.columns = newcols

    unifycolumns(df_B_LST, 'mean')
    unifycolumns(df_B_NDBI, 'mean')
    unifycolumns(df_B_NDVI, 'mean')
    # formating input data

    df_B_LST = df_B_LST.loc[:, ['SA1_7DIG16', 'mean']]
    df_B_LST.columns = ['SA1', 'LST']
    df_B_LST['LST'].fillna(method='ffill', inplace=True)
    df_B_NDBI = df_B_NDBI.loc[:, ['SA1_7DIG16', 'mean']]
    df_B_NDBI.columns = ['SA1', 'NDBI']
    df_B_NDBI['NDBI'].fillna(method='ffill', inplace=True)
    df_B_NDVI = df_B_NDVI.loc[:, ['SA1_7DIG16', 'mean']]
    df_B_NDVI.columns = ['SA1', 'NDVI']
    df_B_NDVI['NDVI'].fillna(method='ffill', inplace=True)
    progressbar.update(current_count=30)

    # group data
    df_target_area = df_B_LST.merge(df_B_NDBI, how='inner', on='SA1').merge(
        df_B_NDVI, how='inner', on='SA1')
    df_target_area = df_target_area.merge(df_other_6, how='left', on='SA1')
    progressbar.update(current_count=35)

    # # calculate pop density
    # df_target_area['Population Density'] = df_target_area['Population Density'].div(
    #     df_target_area['Area_SQKM'], axis=0).fillna(0).replace([np.inf, -np.inf], 0)
    # progressbar.update(current_count=40)

    # renaming columns
    df_target_area_ = df_target_area.iloc[:, 1:]
    df_target_area_ = df_target_area_.set_axis(
        ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'], axis=1, inplace=False)
    df_target_area_.loc[df_target_area_['D'] == 0, ['E', 'F', 'G']] = 0
    df_target_area_.loc[df_target_area_['E'] > 1, 'E'] = 1.0
    df_target_area_.loc[df_target_area_['F'] > 1, 'F'] = 1.0
    df_target_area_.loc[df_target_area_['G'] > 1, 'G'] = 1.0
    progressbar.update(current_count=50)

    # scale dataset
    scaler = MinMaxScaler()
    scaler.fit(df_target_area_[df_target_area_['D'] != 0])
    df_target_area_scaled = scaler.transform(df_target_area_)
    df_target_area_scaled = pd.DataFrame(df_target_area_scaled)
    df_target_area_scaled.head()
    df_target_area_scaled = df_target_area_scaled.set_axis(
        ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'], axis=1, inplace=False)
    progressbar.update(current_count=60)

    # calculate iHVI and other indices
    df_target_area_['Heat Exposure Index'] = df_target_area_scaled['A']
    df_target_area_['Heat Sensitivity Index'] = df_target_area_scaled[[
        'B', 'C', 'D', 'E', 'F', 'G']].sum(axis=1)
    df_target_area_[
        'Adaptive Capability Index'] = df_target_area_scaled[['H', 'I']].sum(axis=1)
    df_target_area_['HVI'] = 1.0/3.0 * (df_target_area_scaled['A'] + 1.0/6.0 * df_target_area_scaled[[
                                        'B', 'C', 'D', 'E', 'F', 'G']].sum(axis=1) - 1.0/2.0 * df_target_area_scaled[['H', 'I']].sum(axis=1))
    progressbar.update(current_count=70)

    # quintile indices
    df_target_area_['HVI'] = pd.qcut(df_target_area_.loc[df_target_area_[
                                     'D'] != 0, 'HVI'], 5, labels=False)
    df_target_area_['Heat Exposure Index'] = pd.qcut(
        df_target_area_.loc[df_target_area_['D'] != 0, 'Heat Exposure Index'], 5, labels=False)
    df_target_area_['Heat Sensitivity Index'] = pd.qcut(
        df_target_area_.loc[df_target_area_['D'] != 0, 'Heat Sensitivity Index'], 5, labels=False)
    df_target_area_['Adaptive Capability Index'] = pd.qcut(
        df_target_area_.loc[df_target_area_['D'] != 0, 'Adaptive Capability Index'], 5, labels=False)
    progressbar.update(current_count=80)

    # deal with 0
    df_target_area_.loc[df_target_area_['D'] != 0, 'HVI'] += 1
    df_target_area_.loc[df_target_area_['D'] == 0, 'HVI'] = 0
    df_target_area_.loc[df_target_area_['D'] != 0, 'Heat Exposure Index'] += 1
    df_target_area_.loc[df_target_area_['D'] == 0, 'Heat Exposure Index'] = 0
    df_target_area_.loc[df_target_area_['D']
                        != 0, 'Heat Sensitivity Index'] += 1
    df_target_area_.loc[df_target_area_['D']
                        == 0, 'Heat Sensitivity Index'] = 0
    df_target_area_.loc[df_target_area_['D']
                        != 0, 'Adaptive Capability Index'] += 1
    df_target_area_.loc[df_target_area_['D']
                        == 0, 'Adaptive Capability Index'] = 0
    progressbar.update(current_count=90)

    # join dataset
    df_target_area = df_target_area.join(df_target_area_[
                                         ['HVI', 'Heat Exposure Index', 'Heat Sensitivity Index', 'Adaptive Capability Index']])
    df_target_area.loc[:, 'HVI'] = df_target_area.loc[:, 'HVI'].astype(int)
    progressbar.update(current_count=95)

    # output
    outputpath = directory + '/iHVI_results.csv'
    df_target_area.to_csv(outputpath, index=None)
    progressbar.update(current_count=100)


def main():
    window = make_window()

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Edit Me':
            sg.execute_editor(__file__)

        if event == "Start":
            progress_bar = window['-PROGRESS BAR-']
            progress_bar.update(current_count=0)
            LST, NDBI, NDVI, OtherSix, directory = values[0], values[1], values[2], values[3], values[4]

            # 0 and 1 are keys of dictionary `values`
            print(LST, NDBI, NDVI,OtherSix, directory)
            try:
                calculateIHVI(LST, NDBI, NDVI, OtherSix, directory, progress_bar)
            except Exception as e:
                sg.popup(e, keep_on_top=True)

    window.close()


if __name__ == '__main__':
    # sg.theme('black')
    # sg.theme('dark red')
    sg.theme('dark green 7')
    main()
