from backup.util.Settings import Settings
from BackupThread import BackupThread
from ServerConnection import ServerConnection
from ManagerGlobals import *
import shutil, logging, time, sys, os, re
import __builtin__

class ServerBase(object):

    def __init__(self):
        if not os.path.exists('ca.crt'):
            logging.error('SSL certificate is missing.')
            return

        self.directory = os.getcwd()
        self.servers = []
        self.backupThreads = []

        logging.info('Loading settings...')
        __builtin__.settings = Settings(os.path.join(self.directory, 'settings.json'))
        __builtin__.servers = Settings(os.path.join(self.directory, 'servers.json'))
    
    def getDirectory(self):
        return self.directory
    
    def getBackupDirectory(self):
        return os.path.join(self.directory, 'backups')
    
    def getLogDirectory(self):
        return os.path.join(self.directory, 'logs')

    def getLogFilename(self):
        logDirectory = self.getLogDirectory()
        
        if not os.path.exists(logDirectory):
            os.makedirs(logDirectory)
        
        return os.path.join(logDirectory, time.strftime('%Y%m%d-%H%M%S.log'))
    
    def getBackupDirectoryFor(self, backupName):
        return os.path.join(self.getBackupDirectory(), backupName)

    def getBackupFilename(self, backupName):
        backupDirectory = self.getBackupDirectoryFor(backupName)
        
        if not os.path.exists(backupDirectory):
            os.makedirs(backupDirectory)
        
        return os.path.join(backupDirectory, time.strftime('%y%M%d-%H%M%S.zip'))

    def getLogFile(self):
        return self.logFile
    
    def log(self, message):
        self.logFile.write('%s %s\n' % (time.strftime('[%Y/%m/%d %H:%M:%S]'), message))
        self.logFile.flush()
        logging.info(message)

    def run(self):
        if not hasattr(self, 'directory'):
            return

        filename = self.getLogFilename()
        mode = 'w' if not os.path.exists(filename) else 'a'
        self.logFile = open(filename, mode)
        
        for serverName, connection in servers.iteritems():
            connection = ServerConnection(serverName, connection['ip'], connection.get('port', 29015), connection['key'])
            thread = BackupThread(connection)
            
            thread.start()
            self.backupThreads.append(thread)
        while True:
            pass