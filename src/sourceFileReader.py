import os


class SourceFileReader:
    # Attributes
    def __init__(self):
        self._file_name = ""
        self._source_text = ""
        self._source_lines = []

    # Input Method
    # Reads a MiniLang source file line by line and stores both the full
    # source text and the individual lines. Line numbers stay 1-based so a
    # later lexical analyzer can report errors with the correct line.
    def read_from_file(self, file_name):
        if not os.path.isfile(file_name):
            raise FileNotFoundError("Could not open source file '" + file_name + "'")

        self._file_name = file_name
        self._source_text = ""
        self._source_lines = []

        with open(file_name, "rt") as read_file:
            for an_input_line in read_file:
                if an_input_line.endswith("\n"):
                    an_input_line = an_input_line[:-1]
                if an_input_line.endswith("\r"):
                    an_input_line = an_input_line[:-1]
                self._source_lines.append(an_input_line)

        self._source_text = "\n".join(self._source_lines)
        if self._source_lines:
            self._source_text += "\n"

    # Accessors
    def get_file_name(self):
        return self._file_name

    def get_source_text(self):
        return self._source_text

    def get_source_lines(self):
        return self._source_lines

    def get_line_count(self):
        return len(self._source_lines)

    def get_line(self, line_number):
        if line_number < 1 or line_number > len(self._source_lines):
            return ""
        return self._source_lines[line_number - 1]
