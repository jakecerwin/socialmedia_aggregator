import pandas as pd
import time

from scrappers.pinterest import PinterestScrapper
from scrappers.linkedin import LinkedinScrapper

usernamePinterest = 'jake.cerwin@yahoo.com'
passwordPinterest = 'datafocusedpythOn'

usernameLinkedIn  = 'jake.cerwin@yahoo.com'
passwordLinkedIn  = '1800317'

""""
linkedin = LinkedinScrapper(usernameLinkedIn, passwordLinkedIn)
time.sleep(5)
df = linkedin.scrape()
breakpoint()
linkedin.close()
"""
"""
pinterest = PinterestScrapper(username, password)
df = pinterest.scrape()
pinterest.refresh()
df = pinterest.scrape()
pinterest.close()
"""
