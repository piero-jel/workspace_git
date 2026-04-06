from datetime import datetime, time
from logging import basicConfig,DEBUG as LEVEL_LOG
from io import BytesIO
#import xlsxwriter
from xlsxwriter import Workbook
from xlsxwriter.workbook import Worksheet
from xlsxwriter.format import Format


from django.utils.translation import gettext as ugettext


from Login.models import Empresa
from config.settings import DEBUG,LOGGING


## setting logger for debug
if DEBUG:
    basicConfig(level=LEVEL_LOG,filename=LOGGING['handlers']['file']['filename']
                ,format='%(asctime)s %(levelname)-5s: %(message)s')


def deltatime2time(deltatime:datetime) -> time:
    """ Conversion desde un datetima estilo time stamp a time 
        - deltatime 
    return tim
    """
    days, seconds = deltatime.days, deltatime.seconds
    Hh = days * 24 + seconds // 3600
    Mm = (seconds % 3600) // 60
    Ss = (seconds % 60)
    # rval = datetime.now()
    # hour=Hh, minute=Mm, second=Ss)
    return time(Hh,Mm,Ss)

