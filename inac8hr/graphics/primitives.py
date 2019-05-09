import math
import numpy as np
import uuid
from abc import abstractmethod
from arcade import FRAGMENT_SHADER, VERTEX_SHADER
from arcade import Sprite as ArcadeSprite
from arcade import Texture
from collections import deque
from PIL import Image
from ..events import Event
from typing import Tuple


class GraphicDrawable:
    def __init__(self):
        self.visible = True

    def register_z_order(self, z_index, relative=True):
        self.z_order = z_index
        self.z_order_relative = relative

    @abstractmethod
    def draw(self):
        pass

class GLShader:
    @staticmethod
    def get_program():
        return shader.program(vertex_shader=VERTEX_SHADER,
                              fragment_shader=FRAGMENT_SHADER)

class DrawableLayer:
    def __init__(self, maximum=500):
        self.array_of_texture_names = []
        self.array_of_images = []
        self.effects = None
        self.texture_change = Event(self)
        self._queue = deque(maxlen=maximum)
        self._group_queue = deque(maxlen=maximum)
        self._tex_changed_flag = False
        self.vao = None
        self.sprite_data = None
        self.gl_data_buf = None
        self.gl_texture = None
        self.program = GLShader.get_program()

    def queue(self, item: GraphicDrawable):
        index = len(self._queue)
        item.register_z_order(index)
        self._queue.append(item)
        self.on_texture_changed("add", item)

    def queue_group(self, item):
        item.texture_change += self.on_group_changed
        for i in item._queue:
            self.queue(i)

    def remove(self, item: GraphicDrawable):
        if item in self._queue:
            self._queue.remove(item)
        self.on_texture_changed("remove", item)

    def remove_group(self, item):
        item.texture_change -= self.on_group_changed
        for i in item._queue:
            self.remove(i)
#
# OpenGL texture creation wrapper functions
#

    def _extract_textures(self) -> Tuple[dict, list]:
        atlas_map = [(sprite, sprite._texture.name) for sprite in self._queue]
        tex_map = dict([(sprite._texture.name, sprite._texture.image) for sprite in self._queue])
        texture_images = [tex_map[tex_name].image for tex_name in tex_map]
        return atlas_map, tex_map, texture_images

    def _process_textures(self, images: list):

        def _merge_down_to_image(total_width, max_height, images):
            #
            # SLUGGISH REGION: REDUCE IMAGES AS MANY AS POSSIBLE!
            #
            new_image = Image.new('RGBA', (total_width, max_height))  # Make a composite image
            x_offset = 0
            for image in images:
                new_image.paste(image, (x_offset, 0))
                x_offset += image.size[0]
            return new_image
            #
            #
            #

        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)
        max_height = max(heights)
        return total_width, max_height, self._apply_effects(_merge_down_to_image(total_width, max_height, images))

    def _map_textures_to_atlas(self, total_width, max_height, atlas: list, tex_map):
        tex_coords = {}
        start_x = 0.0
        for tex_name, image in tex_map:
            end_x = start_x + (image.width / total_width)
            normalized_width = image.width / total_width
            start_height = 1 - (image.height / max_height)
            normalized_height = image.height / max_height
            tex_coords[tex_name] = [start_x, start_height, normalized_width, normalized_height]
            start_x = end_x

        # Go through each sprite and pull from the coordinate list, the proper
        # coordinates for that sprite's image.
        tex_atlas_coords = [tex_coords[tex_name] for sprite, tex_name in atlas]
        return tex_atlas_coords

    def _cache_vao(self, total_width, max_height, atlas, tex_map):
        sprite_count = len(self._queue)
        sprite_positions = [[sprite.center_x, sprite.center_y] for sprite in self._queue]
        sprite_colors = [sprite.color + (sprite.alpha, ) for sprite in self._queue]
        sprite_angles = [math.radians(sprite.angle) for sprite in self._queue]
        sprite_sizes = [[sprite.width / 2, sprite.height / 2] for sprite in self._queue]
        sprite_coords = self._map_textures_to_atlas(total_width, max_height, atlas, tex_map)

        # 
        # Creating OpenGL data buffer
        #

        sprite_data_buffer = np.zeros(sprite_count,
                                      dtype=np.dtype([('position', '2f4'), ('angle', 'f4'),
                                                    ('size', '2f4'), ('sub_tex_coords', '4f4'),
                                                    ('color', '4B')]))
        self.sprite_data = np.zeros(sprite_count, dtype=buffer_type)
        self.sprite_data['position'] = sprite_positions
        self.sprite_data['angle'] = sprite_angles
        self.sprite_data['size'] = sprite_sizes
        self.sprite_data['sub_tex_coords'] = sprite_coords
        self.sprite_data['color'] = sprite_colors
        self.gl_data_buf = shader.buffer(self.sprite_data.tobytes(),
                                         usage='stream')
        #
        #
        #

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
        self.vao = shader.vertex_array(self.program, vao_content)

    def rasterize(self, cached=True) -> Image:
        """
            Convert down from sprite outlines to a single pixelated image\n
            The image also acts as an intermediate for a VisualRenderer
        """
        sprite_count = len(self._queue)
        if sprite_count == 0:
            return
        atlas, tex_map, tex_imgs = self._extract_textures()
        total_width, max_height, comp_img = self._process_textures(tex_imgs)
        self.gl_texture = shader.texture((comp_img.width, comp_img.height),
                                         4, np.asarray(comp_img))
        if cached:
            self._cache_vao(total_width, max_height, atlas, tex_map)
        return comp_img

#
#
#
    def get_texture(self):
        pass

    def _apply_effects(self, image: Image) -> Image:
        return image

    def update(self):
        pass

    def on_group_changed(self, sender, *args):
        print(sender)
        command, item = args[0], args[1]
        if command == "add":
            sender.queue(args[1])
        elif command == "remove":
            sender.remove(args[1])

    def on_texture_changed(self, *args):
        self.texture_change(*args)
        self.rasterize()


class Sprite(GraphicDrawable, ArcadeSprite):
    def __init__(self, filename: str=None, scale: float=1, image_x: float=0, image_y: float=0,
                 image_width: float=0, image_height: float=0,
                 center_x: float=0, center_y: float=0,
                 repeat_count_x=1, repeat_count_y=1):
        GraphicDrawable.__init__(self)
        ArcadeSprite.__init__(self, filename, scale,
                 image_x, image_y,
                 image_width, image_height,
                 center_x, center_y,
                 repeat_count_x, repeat_count_y)
