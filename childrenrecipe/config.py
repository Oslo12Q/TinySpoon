import os


DOMAIN_NAME = os.getenv('DOMAINNAME')
DOMAIN_URL = 'http://%s' % DOMAIN_NAME


#PI_DOMAIN_NAME = os.getenv('APIDOMAINNAME')
API_DOMAIN_NAME = '218.240.151.115:8081'
API_DOMAIN_URL = 'http://%s' % API_DOMAIN_NAME

CARD_RECIPE_URL = '%s/static/index.html?state=%s' % (API_DOMAIN_URL, '%s')

