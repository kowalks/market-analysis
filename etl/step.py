import logging


class Step:
    """Step abstract class
    
    Abstracts an ETL step. Only for internal use."""
    name: str = 'unnamed'

    def run(self):
        logging.info(f'Running {self.name}...')