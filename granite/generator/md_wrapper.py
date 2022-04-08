# External includes
import markdown_generator as mg
from typing import Optional, TypeVar

# Project includes
from granite.generator.output_file_wrapper import OutputFileWrapper

Md_code = TypeVar('markdown_generator.code.Code')      # Declare type variable

class MarkDownFileWrapper(OutputFileWrapper):
    """
    Wrapper for easy handling with markdown file.
    """

    def __init__(self, filename: str) -> None:
        """
        Initialize the object instance
        """

        # Call the parent class constructor
        super().__init__(filename, ".MD")

        self.md_writer = mg.Writer(self.document)

    def __del__(self) -> None:
        """
        Redefine the class destructor to call its parent's destructor

        """
        super().__del__()

    def init_code(self, language: str = "c") -> Md_code:
        """
        Method to initialize a source code section
        :param language: source code language to obtain synthetic coloring

        :return a code source section
        """
        
        return mg.Code(language)

    def write_heading(
        self,
        string: str,
        level: int = 1
    ) -> None:
        """
        Method for initializing a section of source code in Markdown

        :param language: source code language to get synthax coloration
        """
        self.md_writer.write_heading(string, level)
        
    def write(self, string: str) -> None:
        """
        Method for writing a string a section of source code

        :param language: source code language to get synthax coloration
        """
        self.md_writer.write(string)
        
    def _write_hrule(self) -> None:
        """
        Method for writing a horizontal ruler tag to the Markdown file

        """
        self.md_writer.write_hrule()

    def _append_code(self, code_section, string: str) -> None:
        """
        Method to add the string to the code

        :param dict_field: value of the structure fields

        """
        # Add the speficied string into the code section
        code_section.append(string)

    def _write_code(self, code_section) -> None:
        """
        Method for writing the instance of the code object in the markdown file

        """
        self.md_writer.write(code_section)

    def writeline(
        self,
        string: Optional[str] = None
    ) -> None:
        """
        Method for writing a line in the markdown file

        :param string: optional string
        """
        self.md_writer.writeline(string)

    def init_table(self):
        return mg.Table()

    def write_header_table(self, table, dict_header):
        
        # For each items in the dictionary
        for key, value in dict_header.items():
            # add the items into the table
            table.add_column(key, value)

    def write_table(self, table) -> None:
        """
        Method of writing the table to the markdown file

        """

        self.write(table)

    def append_table(
        self,
        table,
        dict_field: dict
    ) -> None:
        """
        Method for appending the input dicionary to the object instance table

        :param dict_field: value of the structure fields
        """

        table.append(*[f'{j}' for j in dict_field.values()])

    def write_source_code(
        self,
        tc_name: str,
        c_structure: str
    ) -> None:
        """Method of writing the source code section in the mardown file

        Parameters
        ----------
        tc_name: 
            telecommand name
        c_structure:
            C strucuture of the telecommand

        """

        # Mark a boundary between the beginning of the document and the source section
        self._write_hrule()

        # Initialize a source section in C language
        code_section = self.init_code("c")

        # Add comment to the structure
        self._append_code(
            code_section,
            f"/* Autogenerated C implementation of the '{tc_name}' structure */",
        )


        # Add the C structure to the source section
        self._append_code(code_section, c_structure)

        # Write the source section to the MD file
        self._write_code(code_section)

        # Mark a boundary between the source section and the rest of the document
        self._write_hrule()