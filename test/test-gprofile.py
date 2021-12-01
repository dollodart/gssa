from gssa.gprofile import schol_list, gprofile_search
import gssa.query
from gssa.dummy import dummy_reqget
from gssa.env import INPUT_DIR, test_logger
import gssa.userenv
gssa.userenv.CACHE_DIR = gssa.userenv.DUMMY_CACHE_DIR


gssa.query.reqget = dummy_reqget


with open(f'{INPUT_DIR}/aeinstein.html', 'r') as _:
    taj = schol_list(_)

publist = gprofile_search(taj)
