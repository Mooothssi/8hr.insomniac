import math
import numpy as np
from arcade import shader, FRAGMENT_SHADER, VERTEX_SHADER
from arcade import Sprite as ArcadeSprite
from collections import deque
from PIL import Image, ImageFilter
from ..events import Event
from typing import Tuple


class GraphicDrawable:
    def __init__(self):
        self.visible = True

    def register_z_order(self, z_index, relative=True):
        self.z_order = z_index
        self.z_order_relative = relative


class GLShader:
    _PROGRAM = None

    @staticmethod
    def get_program():
        if GLShader._PROGRAM is None:
            GLShader._PROGRAM = shader.program(vertex_shader=VERTEX_SHADER,
                                               fragment_shader=FRAGMENT_SHADER)
        return GLShader._PROGRAM

    @staticmethod
    def get_triangle_strip_vertices():
        return np.array([-1.0, -1.0, 0.0, 0.0,
                         -1.0, 1.0, 0.0, 1.0,
                         1.0, -1.0, 1.0, 0.0,
                         1.0, 1.0, 1.0, 1.0], 
                        dtype=np.float32)


class DrawableLayer:
    def __init__(self, maximum=500):
        self.effects = None
        self.visible = False
        self.texture_change = Event(self)
        self._queue = deque(maxlen=maximum)
        self._group_queue = deque(maxlen=maximum)
        self._tex_changed_flag = False
        self._merged = False
        self.vao = None
        self._img_info = None
        self.sprite_data = None
        self.gl_data_buf = None
        self.gl_texture = None
        self._tex_imgs = None
        self.comp_img = None
        self.merged_tex = []
        self.program = GLShader.get_program()

    def draw(self):
        self.visible = True

    def queue(self, item: GraphicDrawable, cached=False):
        index = len(self._queue)
        # item.register_z_order(index)
        self._queue.append(item)
        if cached:
            self.on_texture_changed("add", item)

    def queue_group(self, item, cached=False):
        item.texture_change += self.on_group_changed
        for i in item._queue:
            self.queue(i)
        if cached:
            self.on_texture_changed("add", item)

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

    def _extract_textures(self) -> Tuple[list, dict, list]:
        atlas_map = [(sprite, sprite._texture.name) for sprite in self._queue]
        tex_map = dict([(sprite._texture.name, sprite._texture.image) for sprite in self._queue])
        texture_images = [tex_map[tex_name] for tex_name in tex_map]
        return atlas_map, tex_map, texture_images

    def _process_textures(self, images: list):

        def _merge_down_to_image(total_width, max_height, images):
            #
            # SLUGGISH REGION: REDUCE AS MANY IMAGES AS POSSIBLE!
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

    def _map_textures_to_atlas(self, total_width, max_height, atlas: list, tex_map, normalized=True):
        tex_coords = {}
        start_x = 0.0
        if not normalized:
            total_width, max_height = 1, 1
        for tex_name, image in tex_map.items():
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

    def _cache_vao(self, ref_sprites, total_width, max_height, atlas, tex_map):
        sprite_count = len(ref_sprites)
        sprite_positions = []
        sprite_colors = []
        sprite_angles = []
        sprite_sizes = []
        for sprite in ref_sprites:
            sprite_positions.append([sprite.center_x, sprite.center_y])
            sprite_colors.append(sprite.color + (sprite.alpha, ))
            sprite_angles.append(math.radians(sprite.angle))
            sprite_sizes.append([sprite.width / 2, sprite.height / 2])

        sprite_coords = self._map_textures_to_atlas(total_width, max_height, atlas, tex_map)

        #
        # Creating OpenGL data buffer
        #
        sprite_data = np.zeros(sprite_count,
                               dtype=np.dtype([('position', '2f4'), ('angle', 'f4'),
                               ('size', '2f4'), ('sub_tex_coords', '4f4'),
                               ('color', '4B')]))
        sprite_data['position'] = sprite_positions
        sprite_data['angle'] = sprite_angles
        sprite_data['size'] = sprite_sizes
        sprite_data['sub_tex_coords'] = sprite_coords
        sprite_data['color'] = sprite_colors
        self.sprite_data = sprite_data.tobytes()
        self.gl_data_buf = shader.buffer(self.sprite_data,
                                         usage='stream')
        #
        #
        #

        self.vbo_buf = shader.buffer(GLShader.get_triangle_strip_vertices().tobytes())
        vbo_buf_desc = shader.BufferDescription(
            self.vbo_buf,
            '2f 2f',
            ('in_vert', 'in_texture')
        )
        pos_angle_scale_buf_desc = shader.BufferDescription(
            self.gl_data_buf,
            '2f 1f 2f 4f 4B',
            ('in_pos', 'in_angle', 'in_scale', 'in_sub_tex_coords', 'in_color'),
            normalized=['in_color'], instanced=True)

        vao_content = [vbo_buf_desc, pos_angle_scale_buf_desc]
        self.vao = shader.vertex_array(self.program, vao_content)

    def regenerate_vao_on_the_fly(self):
        self._cache_vao(*self._img_info)

    def rasterize(self, cached=True):
        """
            Convert down from sprite outlines to a single pixelated image\n
            The image also acts as an intermediate for a VisualRenderer
        """
        sprite_count = len(self._queue)
        if sprite_count == 0:
            return
        atlas, tex_map, tex_imgs = self._extract_textures()
        reset_flag = False
        if self._img_info is not None:
            if not set(self._img_info[2]).difference(atlas) == set():
                reset_flag = True
            else:
                self.gl_texture = shader.texture((self.comp_img.width, self.comp_img.height),
                                                    4, np.asarray(self.comp_img))
                if self._merged:
                    q = self._queue
                else:
                    q = self.merged_tex
                self._cache_vao(q, self._img_info[0], self._img_info[1], atlas, tex_map)
        else:
            reset_flag = True
        
        if reset_flag:
            total_width, max_height, comp_img = self._process_textures(tex_imgs)
            self.gl_texture = shader.texture((comp_img.width, comp_img.height),
                                              4, np.asarray(comp_img))
            if cached:
                self.comp_img = comp_img
                self._cache_vao(self._queue, comp_img.width, comp_img.height, atlas, tex_map)
                self._img_info = comp_img.width, comp_img.height, atlas
                self._tex_imgs = tex_imgs

    def merge_down(self):
        self.rasterize()
        positions = [(sprite.center_x, sprite.center_y) for sprite in self._queue]
        range = [(sprite.left, sprite.right) for sprite in self._queue]
        max_left = max([l for l, r in range])
        max_right = max([r for l, r in range])
        pos_x = [pos[0] for pos in positions]
        pos_y = [pos[1] for pos in positions]
        min_pos = min([x for x, y in positions]), min([y for x, y in positions])
        max_pos = max([x for x, y in positions]), max([y for x, y in positions])
        ind = -1

        tex_map = dict([(sprite._texture.name, sprite._texture.image) for sprite in self._queue])
        tex_coords = self._map_textures_to_atlas(self.comp_img.width, self.comp_img.height, self._img_info[2],
                                                 tex_map, normalized=False)
        x_offset, y_offset = 0, 0
        if min_pos[0] < 0:
            x_offset = abs(min_pos[0])
        if min_pos[1] < 0:
            y_offset = abs(min_pos[0])

        width = int(max_pos[0] + self._queue[pos_x.index(max_pos[0])].width - min_pos[0])
        height = int(max_pos[1] + self._queue[pos_x.index(max_pos[1])].height - min_pos[1])

        new_image = Image.new('RGBA', (width, height))  # Make a composite image
        for sprite in self._queue:
            new_image.paste(sprite.texture.image, (sprite.center_x + x_offset, sprite.center_y + y_offset), sprite.texture.image)
        new_image.save('test.png')

        temp_spr = Sprite()
        temp_spr.set_position(min_pos[0], min_pos[1])
        self.merged_tex = []
        self.merged_tex.append(temp_spr)

    def _apply_effects(self, image: Image) -> Image:
        return image.filter(ImageFilter.GaussianBlur(1.25))

    def update(self):
        pass

    def on_group_changed(self, sender, *args):
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
