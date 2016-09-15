import sublime
import sublime_plugin
import subprocess
import os


class GitblameCommand(sublime_plugin.TextCommand):
    '''
    Displays the 'git blame' of the current selection. Requires git version
    1.8.5 or above to be installed.
    '''

    def run(self, edit):
        # Create a temp file for displaying the content of our response.
        tab = sublime.active_window().new_file()
        # Get the file path of the current view.
        filepath = self.view.file_name()
        # Check if are in a temporary file.
        if filepath:
            # Transform the line ranges of the current selections to a format that
            # git blame understands.
            line_ranges = []
            # Iterate over all selections of text.
            for selection in self.view.sel():
                # Get selection start and end rows, and compensate for zero-based
                # index (git blame indexes lines starting at 1).
                start_row = self.view.rowcol(selection.begin())[0] + 1
                end_row = self.view.rowcol(selection.end())[0] + 1
                # Add start and end rows to the ranges we will git blame on.
                line_ranges.extend([ '-L', '%s,%s' % (start_row, end_row) ])
            # Get directory to run git commands from.
            git_dir = os.path.dirname(filepath)
            # Construct the git blame command.
            command = [ 'git', '-C', git_dir, 'blame', filepath ] + line_ranges
            # Run the git blame command.
            blame = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # Wait until it completes.
            blame.wait()
            # Construct contents for the new tab.
            contents = blame.stdout.read().decode('utf-8')
            tab.insert(edit, 0, contents)
        else:
            tab.insert(edit, 0, 'Cannot `git blame` on temporary files')
