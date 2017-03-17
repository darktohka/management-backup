from ServerBase import ServerBase
import logging, os
import __builtin__

logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')
logging.root.setLevel(logging.INFO)
logging.info('Welcome to the Backup Server!')

__builtin__.base = ServerBase()
base.run()