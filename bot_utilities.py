import configparser

def load_config(filename):
    """Loads and reads config file.

    keyword arguments:
    filename -- str, config file name
    
    returns a valid ConfigParser() object
    """

    config = configparser.ConfigParser()
    try:
        with open(filename, 'r') as f:
            config.read_file(f)
        if not config.get('bot','token'):
            raise ValueError
    except (OSError, IOError, FileNotFoundError):
        print('Bot config file \'{}\' not found.'.format(filename))
        exit()
    except ValueError:
        print('Bot token not found. Place in config file as\n'
                'token = <bot token>'
        )
        exit()

    return config