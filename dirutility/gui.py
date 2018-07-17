import PySimpleGUI as gui
from dirutility import desktop


def source_path(window, title, folder='Source'):
    with g.FlexForm(window, auto_size_text=True) as form:
        form_rows = [[g.Text(title)],
                     [g.Text(folder + ' Folder', size=(15, 1), auto_size_text=False), g.InputText(folder),
                      g.FolderBrowse()],
                     [g.Submit(), g.Cancel()]]
        (button, source) = form.LayoutAndShow(form_rows)
    if button == 'Submit':
        # do something useful with the inputs
        g.MsgBox('Submitted', 'Click OK to set this directory', source)
        return source
    else:
        g.MsgBoxError('Cancelled', 'User Cancelled')


class WalkGUI:
    def __init__(self, title):
        """GUI window for inputing DirPaths parameters"""
        self.title = title
        self.params = {}

    def __iter__(self):
        return iter(self.values)

    def __str__(self):
        return str(self.values)

    @staticmethod
    def _line(char='_', width=100, size=(70, 1)):
        return gui.Text(char * width, size=size)

    def _saving(self):
        """Parameters for saving results to file"""
        with gui.FlexForm(self.title, auto_size_text=True, default_element_size=(40, 1)) as form:
            layout = [
                [gui.Text('Results Saving Settings', size=(30, 1), font=("Helvetica", 25), text_color='blue')],
                # Source
                [gui.Text('Destination Folder', size=(15, 1), auto_size_text=False), gui.InputText(desktop()),
                 gui.FolderBrowse()],

                # File types
                [gui.Text('Select file types you would like to save output to.')],
                [gui.Checkbox('CSV', default=True), gui.Checkbox('JSON')],
                [self._line()],

                # Save results to file
                [gui.Submit(), gui.Cancel()]]

            (button, (values)) = form.LayoutAndShow(layout)

        # gui.MsgBox(self.title, 'Parameters set', 'The results of the form are... ',
        #            'The button clicked was "{}"'.format(button), 'The values are', values, auto_close=True)

        self.params['save'] = {
            'directory': values[0],
            'csv': values[1],
            'json': values[2],
        }
        return self.params

    def parsing(self):
        """Parameters for parsing directory trees"""
        with gui.FlexForm(self.title, auto_size_text=True, default_element_size=(40, 1)) as form:
            layout = [
                [gui.Text('Directory Paths utility', size=(30, 1), font=("Helvetica", 25), text_color='blue')],
                # Source
                [gui.Text('Source Folder', size=(15, 1), auto_size_text=False), gui.InputText('Source'),
                 gui.FolderBrowse()],

                # Parallel / Sequential
                [gui.Text('Parallel or Sequential Processing. Larger directory trees are typically parsed faster '
                          'using parallel processing.')],
                [gui.Radio('Parallel Processing', "RADIO1"), gui.Radio('Sequential Processing', "RADIO1",
                                                                       default=True)],
                [self._line()],

                # Files and non-empty-folders
                [gui.Text('Return files or folders, returning folders is useful for creating inventories.')],
                [gui.Radio('Return Files', "RADIO2", default=True), gui.Radio('Return Non-Empty Directories',
                                                                              "RADIO2")],
                [self._line()],

                # max_level
                [gui.Text('Max Depth.... Max number of sub directory depths to traverse (starting directory is 0)')],
                [gui.InputCombo(list(reversed(range(0, 13))), size=(20, 3))],
                [self._line()],

                # Relative and absolute
                [gui.Text('Relative or Absolute Paths.  Relative paths are saved relative to the starting directory. '
                          'Absolute paths are saved as full paths.')],
                [gui.Radio('Relative Paths', "RADIO3", default=True), gui.Radio('Absolute Paths', "RADIO3")],
                [self._line()],

                # Topdown and output
                [gui.Checkbox('Topdown Parse', default=True), gui.Checkbox('Live output results')],
                [self._line()],

                # Save results to file
                [gui.Checkbox('Save Results to File', default=False)],
                [gui.Submit(), gui.Cancel()]]

            (button, (values)) = form.LayoutAndShow(layout)

        # gui.MsgBox(self.title, 'Parameters set', 'The results of the form are... ',
        #            'The button clicked was "{}"'.format(button), 'The values are', values, auto_close=True)

        self.params['parse'] = {
            'directory': values[0],
            'parallelize': values[1],
            'sequential': values[2],
            'yield_files': values[3],
            'non_empty_folders': values[4],
            'max_level': int(values[5]),
            '_relative': values[6],
            'full_paths': values[7],
            'topdown': values[8],
            'console_stream': values[9],
            'save_file': values[10],
        }

        if self.params['parse']['save_file']:
            self._saving()

        return self.params
