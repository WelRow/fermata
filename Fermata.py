import PySimpleGUI as sg
import os.path as path
from notes import Notes

user_control = sg.Column([
    [sg.Combo(['Bass Clef', 'Alto Clef', 'Tenor Clef', 'Treble Clef'], default_value='Bass Clef',key='-CLEFS-')],
    [sg.Combo(['C Major', 'G Major', 'D Major', 'A Major', 'Bb Major', 'F Major'], default_value='C Major', enable_events=True, key='-MAJORS-')],
    [sg.Combo(['A', 'B', 'C', 'D', 'E', 'F', 'G'], default_value='C', key='-NOTES-')],
    [sg.Combo(['1st', '2nd', '3rd'], default_value='1st', key='-OCTAVES-')],
    [sg.HorizontalSeparator()],
    [sg.Combo(['Bass Clef', 'Alto Clef', 'Tenor Clef', 'Treble Clef'], default_value='Alto Clef', key='-DESIRED_CLEF-')],
    [sg.Button('CONVERT!', key='convert')],
    [sg.Button('Credits', key='-CREDITS-')]
])

user_note_image = sg.Column([[sg.Image("note_placeholder.png", key='-IMAGE1-')]])
arrow = sg.Column([[sg.Image("arrow.png")]])
desired_note_image = sg.Column([[sg.Image("note_placeholder.png", key='-IMAGE2-')]])

layout = [[user_control, user_note_image, arrow, desired_note_image]]

window = sg.Window('Fermata v1.0.0', layout, use_custom_titlebar = True, titlebar_icon='Fermata_Logo.png')

while True:
    event, values = window.read(timeout=50)
    if event == sg.WIN_CLOSED:
        break

    # creating clef, major, and clef_switch variables
    if len(values['-CLEFS-']) == 9:
        clef = values['-CLEFS-'][0:4].lower()

    elif len(values['-CLEFS-']) == 10:
        clef = values['-CLEFS-'][0:5].lower()

    else:
        clef = values['-CLEFS-'][0:6].lower()

    
    if len(values['-DESIRED_CLEF-']) == 9:
        clef_switch = values['-DESIRED_CLEF-'][0:4].lower()

    elif len(values['-DESIRED_CLEF-']) == 10:
        clef_switch = values['-DESIRED_CLEF-'][0:5].lower()

    else:
        clef_switch = values['-DESIRED_CLEF-'][0:6].lower()
    

    major = values['-MAJORS-'][0].lower() + "_major"

    
    # When the major changes...
    if event == '-MAJORS-':
        # it'll update the Notes
        window['-NOTES-'].update(values=Notes(values['-MAJORS-']))
        window['-NOTES-'].update(set_to_index = 0)

        # if major doesnt have a low 3 octave note, then it only displays 2 avaliable octaves
        if not path.isfile(f"clef_notes\\{clef}\\{major}\\3_{values['-NOTES-'][0].lower()}" + ".png"):
            window['-OCTAVES-'].update(values = ['1st', '2nd'])
            window['-OCTAVES-'].update(set_to_index = 0)

        else:
            window['-OCTAVES-'].update(values = ['1st', '2nd', '3rd'])
            window['-OCTAVES-'].update(set_to_index = 0)

    #creating a file path with users input from user_control
    if event == 'convert':
        
        note = values['-NOTES-'][0].lower()
        octave = values['-OCTAVES-'][0]

        image_input = f"clef_notes\\{clef}\\{major}\\{octave}_{note}" + ".png"
        image_output = f"clef_notes\\{clef_switch}\\{major}\\{octave}_{note}" + ".png"

        window['-IMAGE1-'].update(filename = image_input)
        window['-IMAGE2-'].update(filename = image_output)
        window.refresh()
    
    #pressing credits popup a window of the credits
    if event == '-CREDITS-':
        sg.popup('Josias Kanyinda - Designing/Programming\n\nThank Jasmine and Jennifer for providing the Treble notes ;3')



window.close()