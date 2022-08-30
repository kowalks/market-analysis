from etl.step import Step


class Transform(Step):
    """Transform step
    
    The transform step accepts a transform function that takes raw data
    and (hopefully) transforms it on a Pandas DataFrame.
    """
    name: str = 'transform'

    def __init__(self, transform=None):
        self.transform_ = transform
        super().__init__()

    def run(self, *args, **kwargs):
        super().run()
        transformed = self.transform(*args, **kwargs)
        return transformed

    def transform(self, *args, **kwargs):
        if self.transform_:
            return self.transform_(*args, **kwargs)
        raise NotImplementedError
