import requests
from etl.step import Step


class Extractor(Step):
    """Simple extractor abstraction

    Abstracts an extractor consisting from a fetch method. It must extract
    content from a location (which can be e.g. HTTP, local files or shared network)
    """
    name: str = 'extract'

    def run(self, *args, **kwargs):
        super().run()
        return self.fetch(*args, **kwargs)

    def fetch(self, *args, **kwargs):
        raise NotImplementedError


class ExtractHTTP(Extractor):
    """HTTP extractor
    
    Fetches data from the web in the provided requests Session. It is used for
    REST API communication between our application and the internet.
    """
    def fetch(self, url, session: requests.Session, params=None, headers=None):
        req = session.get(url, params=params, headers=headers)
        content = req.text
        return content