from cameras.camera import Camera



class Scene:
    """Scene has all the information needed for the ray tracing engine"""

    def __init__(self, camera: Camera, objects, lights, width, height):
        self.camera = camera
        self.objects = objects
        self.lights = lights
        self.width = width
        self.height = height

    def render(self):
        camera_aspect_ratio = self.camera.setup_camera()
        

