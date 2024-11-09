

class Log:
    """
    Handles reading and writing to the Log

    Properties:
    file (str) - name of the log file including extension (default: log.dat)

    Methods:
    write() - Write text to the log file
    read() - Returns entire contents of log file
    """

    def __init__(self, file='log.dat'):
        """
        Initialize the Log object, optionally set the name of the log file (default: log.dat)
        """
        self.file = file

    def write(self, line, mode='a'):
        """
        Write the line to the log file

        line (str) - Text to be written (new line character added automatically, do not include)
        mode (str) - a (default) = Append; w = overwrite (use for first line of file)
        """
        with open(self.file, mode) as f:
            f.write(line + '\n')
    
    def read(self):
        """
        Reads and returns entire contents of log with HTML break statements or empty string if no log file exists
        """
        try:
            html = ''
            with open(self.file) as f:
                for line in f:
                    html += line + '<br />'
            
            return html
        except OSError:
            return ''