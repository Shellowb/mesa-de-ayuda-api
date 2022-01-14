from ..command import NotDefinedCommand

class UnknownCommand(NotDefinedCommand):
    ERR_UNKNOWN = f'''El texto que enviaste, 
                    no se reconoce como commando, 
                    revisa que este bien escrito o
                    que los parametros sean los adecuados
                    '''
    error = NotDefinedCommand.CommandError(ERR_UNKNOWN)
