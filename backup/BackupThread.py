from ManagerGlobals import *
import traceback, time, logging, threading, os

class BackupThread(threading.Thread):

    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.daemon = True
        self.connection = connection
    
    def run(self):
        name = self.connection.getName()
        
        while True:
            logging.info('Backing %s up...' % name)
            
            try:
                response = self.connection.connect(BACKUP_DATABASE)
                
                if 'extraData' not in response:
                    base.log("Couldn't back %s up! Empty response!" % name)
                    continue

                extraData = response['extraData']
                
                if not extraData:
                    base.log("Couldn't back %s up! Empty response!" % name)
                    continue
                
                extraData = extraData.decode('base64')
                directory = base.getBackupDirectoryFor(name)
                filename = base.getBackupFilename(name)
                
                with open(filename, 'wb') as file:
                    file.write(extraData)

                logging.info('Backup complete for %s!' % name)
                
                files = os.listdir(directory)
                maximumFiles = settings.get('maxBackupFiles', 72)

                if len(files) > maximumFiles:
                    files = [os.path.join(directory, file) for file in files]
                    files.sort(key=lambda x: os.path.getmtime(x))
                    
                    for i in xrange(len(files) - maximumFiles):
                        file = files.pop(0)
                        os.remove(file)
                        base.log('Removed old file %s.' % os.path.basename(file))

                time.sleep(settings.get('backupFrequency', 3600))
            except:
                base.log("Couldn't back %s up!" % name)
                base.log(traceback.format_exc())
                time.sleep(120)