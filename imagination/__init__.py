__version__ = '1.0'

def make_from_xml(file_path):
    ''' Make the locator from the configuration file at *file_path*. '''
    
    if not exists(file_path):
        raise UnknownFileError, 'Cannot locate the file.'
    
    