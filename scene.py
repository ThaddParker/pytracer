from cameras.camera import Camera


class Scene:
    """Scene has all the information needed for the ray tracing engine"""

    def __init__(self, settings, camera: Camera, objects, lights):
        self.settings = settings
        self.camera = camera
        self.objects = objects
        self.lights = lights
        # self.width = settings.width
        # self.height = settings.height

    def render(self):
        pass
