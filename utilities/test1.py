import os
import time

ISOTIMEFORMAT='%Y%m%d'
log_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/logs/SHREPA_"+str(time.strftime(ISOTIMEFORMAT))+".log"
print(log_file)
