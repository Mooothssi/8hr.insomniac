

class VisualRenderer:
    def _calculate_sprite_buffer(self):

        if len(self.sprite_list) == 0:
            return

        # Loop through each sprite and grab its position, and the texture it will be using.
        array_of_positions = []
        array_of_sizes = []
        array_of_colors = []
        array_of_angles = []

        for sprite in self.sprite_list:
            array_of_positions.append([sprite.center_x, sprite.center_y])
            array_of_angles.append(math.radians(sprite.angle))
            size_h = sprite.height / 2
            size_w = sprite.width / 2
            array_of_sizes.append([size_w, size_h])
            array_of_colors.append(sprite.color + (sprite.alpha, ))

        new_array_of_texture_names = []
        new_array_of_images = []
        new_texture = False
        if self.array_of_images is None:
            new_texture = True

        # print()
        # print("New texture start: ", new_texture)

        for sprite in self.sprite_list:

            if sprite._texture is None:
                raise Exception("Error: Attempt to draw a sprite without a texture set.")

            name_of_texture_to_check = sprite._texture.name
            if name_of_texture_to_check not in self.array_of_texture_names:
                new_texture = True
                # print("New because of ", name_of_texture_to_check)

            if name_of_texture_to_check not in new_array_of_texture_names:
                new_array_of_texture_names.append(name_of_texture_to_check)
                image = sprite._texture.image
                new_array_of_images.append(image)

        # print("New texture end: ", new_texture)
        # print(new_array_of_texture_names)
        # print(self.array_of_texture_names)
        # print()

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

            # TODO: This code isn't valid, but I think some releasing might be in order.
            # if self.texture is not None:
            #     shader.Texture.release(self.texture_id)

            # Make the composite image
            new_image = Image.new('RGBA', (total_width, max_height))

            x_offset = 0
            for image in self.array_of_images:
                new_image.paste(image, (x_offset, 0))
                x_offset += image.size[0]

            # Create a texture out the composite image
            self._texture = shader.texture(
                 (new_image.width, new_image.height),
                 4,
                 np.asarray(new_image)
            )

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
        for sprite in self.sprite_list:
            index = self.array_of_texture_names.index(sprite._texture.name)
            array_of_sub_tex_coords.append(tex_coords[index])

        # Create numpy array with info on location and such
        buffer_type = np.dtype([('position', '2f4'), ('angle', 'f4'), ('size', '2f4'),
                                ('sub_tex_coords', '4f4'), ('color', '4B')])
        self.sprite_data = np.zeros(len(self.sprite_list), dtype=buffer_type)
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

        vertices = np.array([
            #  x,    y,   u,   v
            -1.0, -1.0, 0.0, 0.0,
            -1.0, 1.0, 0.0, 1.0,
            1.0, -1.0, 1.0, 0.0,
            1.0, 1.0, 1.0, 1.0,
        ], dtype=np.float32
        )
        self.vbo_buf = shader.buffer(vertices.tobytes())
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
