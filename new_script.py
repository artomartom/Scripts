#!/usr/bin/env python3

from argparse import ArgumentParser
from argparse import BooleanOptionalAction
from argparse import Action
import os 

 
class Script(Action):
    def __init__(self, option_strings, dest,  default=False,   required=False, help=None,  metavar=None):
        super(Script, self).__init__( option_strings=option_strings, dest=dest, nargs=0, const=True, 
        default=default, required=required, help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.const)
        fullname = self.get_filename(namespace.name)
        with open(fullname, 'x') as script:
            script.write( self.get_content())
            current_dir = os.getcwd()
            os.system(f"chmod +x  '{current_dir}/{fullname}'") 

    def get_content(self):
        return 'new_script'

    def get_filename(self):
        return 'code'


class Python(Script):

    def get_content(self):
        return '#!/usr/bin/env python3'

    def get_filename(self,name:str):
        return f'{name}.py'

class Bash(Script):

    def get_content(self):
        return '#!/usr/bin/env'

    def get_filename(self,name:str):
        return f'{name}.sh'

class PowerShell(Script):

    def get_content(self):
        return ''

    def get_filename(self,name:str):
        return f'{name}.ps1'


if  __name__ == "__main__":         

    parser =  ArgumentParser()
    parser.add_argument('name',help="name for the new script file without extension" )
    parser.add_argument('-py', '--python', action=Python,
                        help='create a python script')
    parser.add_argument('-sh','--bash',  action=Bash,
                        help='create a bash script')
    parser.add_argument('-ps1','--powershell',  action=PowerShell,
                        help='create a powerShell script')
    args = parser.parse_args( )
 
 
 

