from pywikibot import family

# for local testing of updates to api.wikimedia.org

class Family(family.Family):
    name = 'commons'
    # domain = 'commons.wikimedia.org'
    langs = {
        'en': 'commons.wikimedia.org/',
    }

    def protocol(self, code):
      return 'HTTPS'