import PySimpleGUI as sg
import os.path as path
from notes import Notes
from descriptions import Desc
sg.theme('DarkBlue4')

inputs = sg.Column([
    [sg.Text("Clef", tooltip=Desc("1st_clef")), 
        sg.Combo(['Bass Clef', 'Alto Clef', 'Tenor Clef', 'Treble Clef'], default_value='Bass Clef', enable_events=True, key='-CLEFS-', expand_x=True)],
    [sg.Text("Major", tooltip=Desc("major")), 
        sg.Combo(['C Major', 'G Major', 'D Major', 'A Major', 'Bb Major', 'F Major'], default_value='C Major', enable_events=True, key='-MAJORS-', expand_x=True)],
    [sg.Text("Note", tooltip=Desc("note")), 
        sg.Combo(['C', 'D', 'E', 'F', 'G', 'A', 'B'], default_value='C', key='-NOTES-', expand_x=True)],
    [sg.Text("Octave", tooltip=Desc("octave")), 
        sg.Combo(['1st', '2nd', '3rd', 'Highest Note'], default_value='1st', enable_events=True, key='-OCTAVES-', expand_x=True)],

    [sg.HorizontalSeparator()],

    [sg.Text("Clef", tooltip=Desc("2nd_clef")), 
        sg.Combo(['Bass Clef', 'Alto Clef', 'Tenor Clef', 'Treble Clef'], default_value='Alto Clef', enable_events=True, key='-DESIRED_CLEF-', expand_x=True)],

    [sg.Button('CONVERT!', key='convert', expand_x=True), sg.Button('Credits', key='-CREDITS-', expand_x=True)]
])

outputs = sg.Column([
    [sg.Image("note_placeholder.png", key='-IMAGE1-')],
    [sg.Image("arrow.png")],
    [sg.Image("note_placeholder.png", key='-IMAGE2-')],
], element_justification='center')

layout = [[inputs, outputs]]

window = sg.Window('Fermata v1.1.0', layout, use_custom_titlebar = True, titlebar_icon='Fermata_Logo.png')

while True:
    event, values = window.read(timeout=50)
    if event == sg.WIN_CLOSED:
        break
    print(values)
    # creating variables for file path
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

    note = values['-NOTES-'][0].lower()

    octave = values['-OCTAVES-'][0]
    # When octave is set to highest_note
    if octave == 'H':
        #It set to highest_x
        octave = 'highest'

        # if note select not the base note for the major, it'll reset image2, set the octave to 1, and warn user to not do that again
        if note != major[0]:
            sg.popup('You currently select a note thats beyond the major avaliable octaves\n\nIf you\'re trying to display the highest note in the major, then select the first note of the major and try again!', title='error')
            octave = '1'
            window['-OCTAVES-'].update(set_to_index = 0)
            window['-IMAGE2-'].update(filename = 'note_placeholder.png')

    
    def isThirdOctaveAval():
        # if the chosen clef and desired clef are the same..
        if values['-DESIRED_CLEF-'] == values['-CLEFS-']:
            # ...and it has 3 octaves, display 3 octaves
            if path.isfile(f"clef_notes\\{clef}\\{major}\\3_{values['-NOTES-'][0].lower()}" + ".png"):
                window['-OCTAVES-'].update(values = ['1st', '2nd', '3rd', 'Highest Note'])
                window['-OCTAVES-'].update(set_to_index = 0)
            
            # ...if not, then 2
            else:
                window['-OCTAVES-'].update(values = ['1st', '2nd', 'Highest Note'])
                window['-OCTAVES-'].update(set_to_index = 0)
        
        # if chosen clef and desired clef are NOT the same...
        else:
            # ...and desired clef and chosen clef has 3 octaves, display 3 clefs
            if path.isfile(f"clef_notes\\{clef_switch}\\{major}\\3_{values['-NOTES-'][0].lower()}" + ".png") and path.isfile(f"clef_notes\\{clef}\\{major}\\3_{values['-NOTES-'][0].lower()}" + ".png"): 
                window['-OCTAVES-'].update(values = ['1st', '2nd', '3rd', 'Highest Note'])
                window['-OCTAVES-'].update(set_to_index = 0)

            #... if not, then 2
            else:
                window['-OCTAVES-'].update(values = ['1st', '2nd', 'Highest Note'])
                window['-OCTAVES-'].update(set_to_index = 0)

    # When the major changes...
    if event == '-MAJORS-':
        # it'll update the note list
        window['-NOTES-'].update(values=Notes(values['-MAJORS-']))
        window['-NOTES-'].update(set_to_index = 0)

        isThirdOctaveAval()
    
    if event == '-DESIRED_CLEF-':
        isThirdOctaveAval()
    
    if event == '-CLEFS-':
        window['-OCTAVES-'].update(set_to_index = 0)
        octave = '1'

        isThirdOctaveAval()


    # Continuously update the current note
    image_input = f"clef_notes\\{clef}\\{major}\\{octave}_{note}" + ".png"
    window['-IMAGE1-'].update(filename = image_input)


    # clicking convert will translate current note and give an image to the bottom image
    if event == 'convert':
        # if user wants to see highest note in user clef where major has 2 octaves and desired clef has 3 octaves, it will give the highest 3rd note
        if octave == 'highest' and not path.isfile(f"clef_notes\\{clef}\\{major}\\3_{values['-NOTES-'][0].lower()}" + ".png"):
            octave = '3'

        image_output = f"clef_notes\\{clef_switch}\\{major}\\{octave}_{note}" + ".png"
        
        window['-IMAGE2-'].update(filename = image_output)
        window.refresh()
    
    # pressing credits popup a window of the credits
    if event == '-CREDITS-':
        sg.popup('Josias Kanyinda - Designing/Programming\n\nThank Jasmine and Jennifer for providing the Treble notes ;3', title='Credits')



window.close()