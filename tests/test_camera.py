from unittest import TestCase
from cameras.camera import Camera, PerspectiveCamera


class TestCameraTestCase(TestCase):
    def setUp(self) -> None:
        self.cam = Camera()

    def test_create_camera_ray(self):
        pass


class TestPerspectiveTestCase(TestCase):

    def setUp(self) -> None:
        self.cam = PerspectiveCamera()
