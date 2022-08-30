import logging
import requests
import sqlalchemy
import urllib3


class Connector:
    """Simple connector abstraction

    Abstracts a connector consisting from a setup and a cleanup method.
    Used for long connections (e.g. HTTP or Database) that requires special
    attention to error handling during the execution. For example, in databases
    we always have to close the connection and commit the applied changes.
    """
    name: str = 'unnamed'
    resource = None

    def __enter__(self):
        logging.info(f'Opening {self.name} connector')
        self.resource = self.setup()
        return self.resource

    def __exit__(self, exc_type, exc_value, traceback):
        logging.info(f'Closing {self.name} connector')
        return self.cleanup(self.resource)

class HTTPConnector(Connector):
    """Connector for HTTP
    
    Connects with HTTP protocol without verification. This class
    can be used to bypass proxy authentication etc.
    """
    name: str = 'http'

    def setup(self) -> requests.Session:
        s = requests.Session()
        s.verify = False
        urllib3.disable_warnings()
        return s

    def cleanup(self, s: requests.Session):
        s.close()

class DBConnector(Connector):
    """Connector for Database
    
    Connects with SQLite protocol in market database. This class
    can be extended for other databases, but here we want to keep it simple.
    """
    name: str = 'db'

    def setup(self) -> sqlalchemy.engine:
        engine = sqlalchemy.create_engine('sqlite:///db/market.db')
        return engine

    def cleanup(self, engine: sqlalchemy.engine):
        return