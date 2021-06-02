#  MIT License
#
#  Copyright (c) [year] [fullname]
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import shutil
import tempfile
from multiprocessing import Process, Value
from pathlib import Path

from utils.vector import Vector

from utils.color import Color
from utils.image import Image
import includes.consts as consts
from ray import Ray
from scene import Scene


def setup_camera(camera):
    camera_direction = camera.direction
    camera_right = camera.right
    camera_up = camera.up
    camera_location = camera.origin
    # aspect_ratio = 4.0/3.0
    camera_length_right = camera_right.length
    camera_length_up = camera_up.length

    # TODO: need to add different aspect ratios based on camera type
    # this is the default aspect ratio for prespective camera
    return camera_length_right / camera_length_up


def create_camera_ray(camera_origin, param):
    ray = Ray(camera_origin)



class RenderEngine:
    """Renders 3D objects into 2D objects using ray tracing"""

    def render_multiprocess(self, scene: Scene, process_count, img_fileobj):
        def split_range(count, parts):
            d, r = divmod(count, parts)
            return [
                (i * d + min(i, r), (i + 1) * d + min(i + 1, r)) for i in range(parts)
            ]

        width = scene.width
        height = scene.height
        ranges = split_range(height, process_count)
        temp_dir = Path(tempfile.mkdtemp())
        temp_file_tmpl = "puray-part-{}.temp"
        processes = []
        try:
            rows_done = Value("i", 0)
            for hmin, hmax in ranges:
                part_file = temp_dir / temp_file_tmpl.format(hmin)
                processes.append(
                    Process(
                        target=self.render,
                        args=(scene, hmin, hmax, part_file, rows_done),
                    )
                )
            # Start all the processes
            for process in processes:
                process.start()
            # Wait for all the processes to finish
            for process in processes:
                process.join()
            # Construct the image by joining all the parts
            Image.write_ppm_header(img_fileobj, height=height, width=width)
            for hmin, _ in ranges:
                part_file = temp_dir / temp_file_tmpl.format(hmin)
                img_fileobj.write(open(part_file, "r").read())
        finally:
            shutil.rmtree(temp_dir)

    def render(self, scene: Scene, hmin, hmax, part_file, rows_done):

        width = scene.width
        height = scene.height
        aspect_ratio = setup_camera(scene.camera)  # 4.0/3.0 # float(width) / height
        x0 = -1.0
        x1 = +1.0
        xstep = (x1 - x0) / (width - 1)
        y0 = -1.0 / aspect_ratio
        y1 = +1.0 / aspect_ratio
        ystep = (y1 - y0) / (height - 1)

        camera_origin = scene.camera.location
        pixels = Image(width, hmax - hmin)

        for j in range(hmin, hmax):
            x0 = 0.5 - j/height  # y0 + j * ystep
            for i in range(width):
                y0 = i/width - 0.5  # x0 + i * xstep
                direction = scene.camera.direction + x0 * scene.camera.right + y0 * scene.camera.up
                ray = Ray(camera_origin, direction.normalize())
                pixels.set_pixel(i, j - hmin, self.ray_trace(ray, scene))
            # Update progress bar
            if rows_done:
                with rows_done.get_lock():
                    rows_done.value += 1
                    print(
                        "{:3.0f}%".format(float(rows_done.value) / float(height) * 100),
                        end="\r",
                    )
        with open(part_file, "w") as part_fileobj:
            pixels.write_ppm_raw(part_fileobj)

    def ray_trace(self, ray: Ray, scene: Scene, depth=0):
        color = Color(0, 0, 0)
        # Find the nearest object hit by the ray in the scene
        dist_hit, obj_hit = self.find_nearest(ray, scene)
        if obj_hit is None:
            return color # TODO: Change this to skysphere

        hit_pos = ray.origin + ray.direction * dist_hit
        hit_normal = obj_hit.normal(hit_pos)
        color += self.color_at(obj_hit, hit_pos, hit_normal, scene)

        if depth < consts.MAX_DEPTH:
            new_ray_pos = hit_pos + hit_normal * consts.MIN_DISPLACE
            new_ray_dir = (ray.direction - 2 * ray.direction.dot(hit_normal) * hit_normal)
            new_ray = Ray(new_ray_pos, new_ray_dir)
            # Attenuate the reflected ray by the reflection coefficient
            color += (self.ray_trace(new_ray, scene, depth + 1) * obj_hit.material.finish.reflection)
        return color

    @staticmethod
    def find_nearest(ray: Ray, scene: Scene):
        dist_min = None
        obj_hit = None
        for obj in scene.objects:
            dist = obj.intersects(ray)
            if dist is not None and (obj_hit is None or dist < dist_min):
                dist_min = dist
                obj_hit = obj
        return dist_min, obj_hit

    @staticmethod
    def color_at(obj_hit, hit_pos, normal, scene: Scene):
        material = obj_hit.material
        obj_color = material.color_at(hit_pos)
        to_cam = scene.camera.location - hit_pos

        color = material.finish.ambient * Color.from_hex("#FFFFFF")
        # Light calculations
        for light in scene.lights:
            to_light = Ray(hit_pos, light.position - hit_pos)

            # Diffuse shading (Lambert)
            color += (obj_color * material.finish.diffuse * max(normal.dot(to_light.direction), 0))

            # Specular shading (Blinn-Phong)

            color += RenderEngine.compute_phong(light, material, color, normal, to_light, to_cam)
        return color

    @staticmethod
    def compute_metallic(self, finish):
        pass

    @staticmethod
    def compute_phong(light, material, color, normal, to_light_dir, to_cam_dir, ):
        specular_k = 50
        half_vector = (to_light_dir.direction + to_cam_dir).normalize()
        color += (light.color * material.finish.specular * max(normal.dot(half_vector), 0) ** specular_k)
        return color