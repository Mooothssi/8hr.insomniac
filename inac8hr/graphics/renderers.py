from arcade import shader, SpriteList
from ctypes import *
from arcade.shader import VertexArray
from .primitives import GraphicDrawable, DrawableLayer
from ..gui.basics import RectangularRegion
from ..wrappers.inac8hr_arcade import PreferredSprite
import pyglet.gl as gl
import pyglet
from threading import Thread
from arcade import get_projection, VERTEX_SHADER, FRAGMENT_SHADER
from collections import deque
from PIL import Image
from PIL import ImageFilter
from .primitives import DrawableLayer
import numpy as np
import math
import time


class VisualRenderer:
    __instance = None

    def __init__(self):
        self.vao = None
        self._queue = deque()
        self._layers = deque()
        self.sprite_data_buf = None
        self.texture_id = None
        self._texture = None
        self.program = shader.program(
            vertex_shader=VERTEX_SHADER,
            fragment_shader=FRAGMENT_SHADER
        )

        self.array_of_texture_names = []
        self.array_of_images = []
        self.array_of_layers = []
        self.is_static = False
        self.vertices = np.array([
            #  x,    y,   u,   v in GL Triangle Strip Mode
            -1.0, -1.0, 0.0, 0.0,
            -1.0, 1.0, 0.0, 1.0,
            1.0, -1.0, 1.0, 0.0,
            1.0, 1.0, 1.0, 1.0,
        ], dtype=np.float32
        )
        self.ended = False
        self.times = []

    @staticmethod
    def instance():
        if VisualRenderer.__instance is None:
            VisualRenderer.__instance = VisualRenderer()
        return VisualRenderer.__instance

    def queue(self, item: DrawableLayer):
        self._queue.append(item)

    def queue_one(self, item: GraphicDrawable):
        # index = len(self._queue)
        group = DrawableLayer()
        group.queue(item)
        self._queue.append(group)
        # item.register_z_order(index)

    def remove(self, item):
        if item in self._queue:
            self._queue.remove(item)

    def schedule(self, rate=1/60):
        pyglet.clock.unschedule(self.draw)
        pyglet.clock.schedule_interval(self.draw, rate)

    @staticmethod
    def check_occlusion(outer, inner):
        print([point for point in inner.region.vertex_loop if outer.is_point_inside(point)])
        print([point for point in outer.region.vertex_loop if inner.is_point_inside(point)])

    def clear_screen(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    def setup_shader_program_if_needed(self):
        if self.program is None:
            self.program = shader.program(
             vertex_shader=VERTEX_SHADER,
             fragment_shader=FRAGMENT_SHADER)

    def draw(self, delta):
        if len(self._queue) == 0:
            return
        # self.clear_screen()
        self.setup_shader_program_if_needed()
        for layer in self._queue:
            if len(layer._queue) == 0 or not layer.visible:
                continue
            if layer.vao is None:
                layer.rasterize()
            layer.gl_texture.use(1)

            gl.glEnable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

            with layer.vao:
                self.program['Texture'] = 1 # self.texture_id
                self.program['Projection'] = get_projection().flatten()

                layer.gl_data_buf.write(layer.sprite_data)

                layer.vao.render(gl.GL_TRIANGLE_STRIP, instances=len(layer._queue))

                layer.gl_data_buf.orphan()
            layer.visible = False
            layer.vao = None

    def _merge_down_to_image(self, total_width, max_height):
        #
        # SLUGGISH REGION: REDUCE IMAGES AS MANY AS POSSIBLE!
        #
        new_image = Image.new('RGBA', (total_width, max_height))  # Make a composite image
        x_offset = 0
        t = time.time()
        for image in self.array_of_layers:
            new_image.paste(image, (x_offset, 0))
            x_offset += image.size[0]
        print(f"elapsed: {time.time()-t}")
        return new_image
        #
        #
        #

    def _calculate_sprite_buffer(self):
        if len(self._queue) == 0:
            return
#
# Initialize arrays
#
        array_of_positions = []
        array_of_sizes = []
        array_of_colors = []
        array_of_angles = []
        self.array_of_layers.clear()
        num_sprites = 0
#
#
# 
        for layer in self._queue:
            for sprite in layer._queue:
                array_of_positions.append([sprite.center_x, sprite.center_y])
                array_of_angles.append(math.radians(sprite.angle))
                size_h = sprite.height / 2
                size_w = sprite.width / 2
                array_of_sizes.append([size_w, size_h])
                array_of_colors.append(sprite.color + (sprite.alpha, ))
            num_sprites += len(layer._queue)

        new_array_of_texture_names = []
        new_array_of_images = []
        new_texture = False
        if self.array_of_images is None:
            new_texture = True

        for layer in self._queue:
            for sprite in layer._queue:

                if sprite._texture is None:
                    raise Exception("Error: Attempt to draw a sprite without a texture set.")

                name_of_texture_to_check = sprite._texture.name
                if name_of_texture_to_check not in self.array_of_texture_names:
                    new_texture = True

                if name_of_texture_to_check not in new_array_of_texture_names:
                    new_array_of_texture_names.append(name_of_texture_to_check)
                    image = sprite._texture.image
                    new_array_of_images.append(image)

        if new_texture:
            # Add back in any old textures. Chances are we'll need them.
            for index, old_texture_name in enumerate(self.array_of_texture_names):
                if old_texture_name not in new_array_of_texture_names and self.array_of_images is not None:
                    new_array_of_texture_names.append(old_texture_name)
                    image = self.array_of_images[index]
                    new_array_of_images.append(image)

            self.array_of_texture_names = new_array_of_texture_names

            self.array_of_images = new_array_of_images
            # print(f"New Texture Atlas with names {self.array_of_texture_names}")

        # Get their sizes
        widths, heights = zip(*(i.size for i in self.array_of_images))

        # Figure out what size a composite would be
        total_width = sum(widths)
        max_height = max(heights)

        if new_texture:
            new_image = self._merge_down_to_image(total_width, max_height)
            # Create a texture out the composite image
            self._texture = shader.texture(
                 (new_image.width, new_image.height),
                 4, np.asarray(new_image))
            if self.texture_id is None:
                self.texture_id = SpriteList.next_texture_id

        # Create a list with the coordinates of all the unique textures
        tex_coords = []
        start_x = 0.0
        for image in self.array_of_images:
            end_x = start_x + (image.width / total_width)
            normalized_width = image.width / total_width
            start_height = 1 - (image.height / max_height)
            normalized_height = image.height / max_height
            tex_coords.append([start_x, start_height, normalized_width, normalized_height])
            start_x = end_x

        # Go through each sprite and pull from the coordinate list, the proper
        # coordinates for that sprite's image.
        array_of_sub_tex_coords = []
        for layer in self._queue:
            for sprite in layer._queue:
                index = self.array_of_texture_names.index(sprite._texture.name)
                array_of_sub_tex_coords.append(tex_coords[index])

        # Create numpy array with info on location and such
        buffer_type = np.dtype([('position', '2f4'),
                                ('angle', 'f4'),
                                ('size', '2f4'),
                                ('sub_tex_coords', '4f4'),
                                ('color', '4B')])
        self.sprite_data = np.zeros(num_sprites, dtype=buffer_type)
        self.sprite_data['position'] = array_of_positions
        self.sprite_data['angle'] = array_of_angles
        self.sprite_data['size'] = array_of_sizes
        self.sprite_data['sub_tex_coords'] = array_of_sub_tex_coords
        self.sprite_data['color'] = array_of_colors

        if self.is_static:
            usage = 'static'
        else:
            usage = 'stream'

        self.sprite_data_buf = shader.buffer(
            self.sprite_data.tobytes(),
            usage=usage
        )

        self.vbo_buf = shader.buffer(self.vertices.tobytes())
        vbo_buf_desc = shader.BufferDescription(
            self.vbo_buf,
            '2f 2f',
            ('in_vert', 'in_texture')
        )
        pos_angle_scale_buf_desc = shader.BufferDescription(
            self.sprite_data_buf,
            '2f 1f 2f 4f 4B',
            ('in_pos', 'in_angle', 'in_scale', 'in_sub_tex_coords', 'in_color'),
            normalized=['in_color'], instanced=True)

        vao_content = [vbo_buf_desc, pos_angle_scale_buf_desc]

        # Can add buffer to index vertices
        self.vao = shader.vertex_array(self.program, vao_content)


class ControlVFXRenderer:
    pass
