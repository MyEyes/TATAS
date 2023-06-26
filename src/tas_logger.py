import logging
import logging

logging.basicConfig(level=logging.INFO, handlers=[])
global_logger = logging.getLogger('TATAS')
fh = logging.FileHandler('run.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('[{levelname: ^8}] [{name: ^20}] {message}', style='{')
verbose_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
fh.setFormatter(verbose_formatter)
ch.setFormatter(formatter)

global_logger.addHandler(fh)
global_logger.addHandler(ch)