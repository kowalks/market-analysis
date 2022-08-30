import pandas as pd
from etl.step import Step


class Loader(Step):
    """Simple loader abstraction

    Abstracts a loader consisting from a load method. Since the load step
    is controlled by us, it is only used for Database loading. However, this class
    can be extended to any other kind of loader.
    """
    name: str = 'load'
    table: str = None

    def __init__(self, table):
        super().__init__()
        self.table = table

    def run(self, *args, **kwargs):
        super().run()
        return self.load(*args, **kwargs)

    def load(self, *args, **kwargs):
        raise NotImplementedError


class LoadDB(Loader):
    """Database loader
    
    It safely loads content from a Pandas DataFrame to a SQLAlchemy connection
    using the Pandas built-in engine. If the table exists, it only appends the new
    DataFrame.

    NOTE: In the real world, we could be more rigorous about the append function. Ideally,
    the load funcion shoud only update content in the database (i.e. append if the content
    doesn't exists or replace otherwise). 
    """
    def load(self, content: pd.DataFrame, con):
        cfg = {
            'name': self.table,
            'if_exists': 'append',
            'con': con,
            'index': False,
        }
        return content.to_sql(**cfg)
