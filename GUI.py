import PySimpleGUI as psg


def gui_settings():
    psg.theme('Dark')

    # Options inside GUI
    layout = [
        [psg.Text('Number of Rows     '), psg.Slider(range=(3, 100), orientation='h', default_value='22')],
        [psg.Text('Number of Columns'), psg.Slider(range=(3, 100), orientation='h', default_value='35')],
        [psg.Text('Grid Square Size    '), psg.Slider(range=(2, 50), orientation='h', default_value='30')],
        [psg.Button('Depth first search'), psg.Button('Breadth first search')]
    ]

    # Initialize GUI window with layout
    gui = psg.Window('github.com/awillisford', layout)

    inputs = []
    while True:
        event, values = gui.read()
        if event in (None, 'Depth first search', 'Breadth first search'):
            inputs.append(event)
            for i in values:
                inputs.append(int(values[i]))
            break

    print(inputs)
    gui.close()

    return inputs
