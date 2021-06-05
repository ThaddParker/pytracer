

class Settings:

    def __init__(self, **kwargs):
        self.width = int(kwargs.get('width', 400))  # image width
        self.aspect_ratio = kwargs.get('aspect_ratio', 16./9.)
        self.height = int(self.width / self.aspect_ratio)
        self.samples_per_pixel = int(kwargs.get('samples', 50)) # number of samples taken for each pixel shot
        self.max_depth = kwargs.get('max_depth', 50)
