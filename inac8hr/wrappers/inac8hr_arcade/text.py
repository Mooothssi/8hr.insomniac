from typing import Tuple
from typing import List
from typing import Union
from .sprite import Sprite, Texture
from arcade.text import Text
from arcade.color import BLACK
import PIL
from PIL import ImageFilter

RGB = Union[Tuple[int, int, int], List[int]]
RGBA = Union[Tuple[int, int, int, int], List[int]]
Color = Union[RGB, RGBA]
Point = Union[Tuple[float, float], List[float]]


class PILText:

    cache = {}

    @staticmethod
    def render_text(text: str,
              start_x: float, start_y: float,
              color: Color,
              font_size: float = 12,
              width: int = 0,
              align: str = "left",
              font_name=('calibri', 'arial'),
              bold: bool = False,
              italic: bool = False,
              anchor_x: str = "left",
              anchor_y: str = "baseline",
              rotation: float = 0) -> Sprite:

        font_size *= 1.25
        scale_up = 5
        scale_down = 5
        font_size *= scale_up
        key = f"{text}{color}{font_size}{width}{align}{font_name}{bold}{italic}"
        label = Text()

        # Figure out the font to use
        font = None

        # Font was specified with a string
        if isinstance(font_name, str):
            try:
                font = PIL.ImageFont.truetype(font_name, int(font_size))
            except OSError:
                # print(f"1 Can't find font: {font_name}")
                pass

            if font is None:
                try:
                    temp_font_name = f"{font_name}.ttf"
                    font = PIL.ImageFont.truetype(temp_font_name, int(font_size))
                except OSError:
                    # print(f"2 Can't find font: {temp_font_name}")
                    pass

        # We were instead given a list of font names, in order of preference
        else:
            for font_string_name in font_name:
                try:
                    font = PIL.ImageFont.truetype(font_string_name, int(font_size))
                    # print(f"3 Found font: {font_string_name}")
                except OSError:
                    # print(f"3 Can't find font: {font_string_name}")
                    pass

                if font is None:
                    try:
                        temp_font_name = f"{font_name}.ttf"
                        font = PIL.ImageFont.truetype(temp_font_name, int(font_size))
                    except OSError:
                        # print(f"4 Can't find font: {temp_font_name}")
                        pass

                if font is not None:
                    break

        # Default font if no font
        if font is None:
            font_names = ("arial.ttf",
                        "/usr/share/fonts/truetype/freefont/FreeMono.ttf",
                        '/System/Library/Fonts/SFNSDisplay.ttf')
            for font_string_name in font_names:
                try:
                    font = PIL.ImageFont.truetype(font_string_name, int(font_size))
                    break
                except OSError:
                    # print(f"5 Can't find font: {font_string_name}")
                    pass

        # This is stupid. We have to have an image to figure out what size
        # the text will be when we draw it. Of course, we don't know how big
        # to make the image. Catch-22. So we just make a small image we'll trash
        text_image_size = (10, 10)
        image = PIL.Image.new("RGBA", text_image_size)
        draw = PIL.ImageDraw.Draw(image)

        # Get size the text will be
        text_image_size = draw.multiline_textsize(text, font=font)

        # Create image of proper size
        text_height = text_image_size[1]
        text_width = text_image_size[0]

        if text_width == 0:
            return None

        image_start_x = 0
        if width == 0:
            width = text_image_size[0]
        else:
            # Wait! We were given a field width.
            if align == "center":
                # Center text on given field width
                field_width = width * scale_up
                text_image_size = field_width, text_height
                image_start_x = (field_width - text_width) // 2
                width = field_width
            else:
                image_start_x = 0

        # If we draw a y at 0, then the text is drawn with a baseline of 0,
        # cutting off letters that drop below the baseline. This shoves it
        # up a bit.
        image_start_y = - font_size * scale_up * 0.02
        image = PIL.Image.new("RGBA", text_image_size)
        draw = PIL.ImageDraw.Draw(image)

        # Convert to tuple if needed, because the multiline_text does not take a
        # list for a color
        if isinstance(color, list):
            color = tuple(color)
        draw.multiline_text((image_start_x, image_start_y), text, color, align=align, font=font)
        image = image.resize((width // scale_down, text_height // scale_down), resample=PIL.Image.LANCZOS)

        text_sprite = Sprite()
        text_sprite._texture = Texture(key)
        text_sprite._texture.image = image

        text_sprite.image = image
        text_sprite.texture_name = key
        text_sprite.width = image.width
        text_sprite.height = image.height

        if anchor_x == "left":
            text_sprite.center_x = start_x + text_sprite.width / 2
        elif anchor_x == "center":
            text_sprite.center_x = start_x
        elif anchor_x == "right":
            text_sprite.right = start_x
        else:
            raise ValueError(f"anchor_x should be 'left', 'center', or 'right'. Not '{anchor_x}'")

        if anchor_y == "top":
            text_sprite.center_y = start_y + text_sprite.height / 2
        elif anchor_y == "center":
            text_sprite.center_y = start_y
        elif anchor_y == "bottom" or anchor_y == "baseline":
            text_sprite.bottom = start_y
        else:
            raise ValueError(f"anchor_x should be 'top', 'center', 'bottom', or 'baseline'. Not '{anchor_y}'")

        text_sprite.angle = rotation

        return text_sprite

    @staticmethod
    def determine_dimensions(control, text: str,
                             font_size: float = 12,
                             width: int = 0,
                             align: str = "left",
                             font_name=('calibri', 'arial'),
                             bold: bool = False,
                             italic: bool = False,
                             anchor_x: str = "left",
                             anchor_y: str = "baseline",
                             rotation: float = 0
                             ):
        font_size *= 1.25
        scale_up = 5
        scale_down = 5
        font_size *= scale_up
        label = Text()

        # Figure out the font to use
        font = None

        # Font was specified with a string
        if isinstance(font_name, str):
            try:
                font = PIL.ImageFont.truetype(font_name, int(font_size))
            except OSError:
                # print(f"1 Can't find font: {font_name}")
                pass

            if font is None:
                try:
                    temp_font_name = f"{font_name}.ttf"
                    font = PIL.ImageFont.truetype(temp_font_name, int(font_size))
                except OSError:
                    # print(f"2 Can't find font: {temp_font_name}")
                    pass

        # We were instead given a list of font names, in order of preference
        else:
            for font_string_name in font_name:
                try:
                    font = PIL.ImageFont.truetype(font_string_name, int(font_size))
                    # print(f"3 Found font: {font_string_name}")
                except OSError:
                    # print(f"3 Can't find font: {font_string_name}")
                    pass

                if font is None:
                    try:
                        temp_font_name = f"{font_name}.ttf"
                        font = PIL.ImageFont.truetype(temp_font_name, int(font_size))
                    except OSError:
                        # print(f"4 Can't find font: {temp_font_name}")
                        pass

                if font is not None:
                    break

        # Default font if no font
        if font is None:
            font_names = ("arial.ttf",
                        "/usr/share/fonts/truetype/freefont/FreeMono.ttf",
                        '/System/Library/Fonts/SFNSDisplay.ttf')
            for font_string_name in font_names:
                try:
                    font = PIL.ImageFont.truetype(font_string_name, int(font_size))
                    break
                except OSError:
                    # print(f"5 Can't find font: {font_string_name}")
                    pass

        # This is stupid. We have to have an image to figure out what size
        # the text will be when we draw it. Of course, we don't know how big
        # to make the image. Catch-22. So we just make a small image we'll trash
        text_image_size = (10, 10)
        image = PIL.Image.new("RGBA", text_image_size)
        draw = PIL.ImageDraw.Draw(image)

        # Get size the text will be
        text_image_size = draw.multiline_textsize(text, font=font)

        # Create image of proper size
        text_height = text_image_size[1]
        text_width = text_image_size[0]

        if text_width == 0:
            return control.width, text_height

        image_start_x = 0
        if width == 0:
            width = text_image_size[0]
        else:
            # Wait! We were given a field width.
            if align == "center":
                # Center text on given field width
                field_width = width * scale_up
                text_image_size = field_width, text_height
                image_start_x = (field_width - text_width) // 2
                width = field_width
            else:
                image_start_x = 0

        # If we draw a y at 0, then the text is drawn with a baseline of 0,
        # cutting off letters that drop below the baseline. This shoves it
        # up a bit.
        image_start_y = - font_size * scale_up * 0.02
        image = PIL.Image.new("RGBA", text_image_size)
        draw = PIL.ImageDraw.Draw(image)

        draw.multiline_text((image_start_x, image_start_y), text, BLACK, align=align, font=font)
        image = image.resize((width // scale_down, text_height // scale_down), resample=PIL.Image.LANCZOS)

        text_sprite = Sprite()
        text_sprite.image = image
        text_sprite.width = image.width
        text_sprite.height = image.height

        return text_sprite.width, text_sprite.height

    @staticmethod
    def draw_text(control, text: str,
                  start_x: float, start_y: float,
                  color: Color,
                  font_size: float = 12,
                  width: int = 0,
                  align: str = "left",
                  font_name=('calibri', 'arial'),
                  bold: bool = False,
                  italic: bool = False,
                  anchor_x: str = "left",
                  anchor_y: str = "baseline",
                  rotation: float = 0,
                  blur_factor=0
                  ):
        # Scale the font up, so it matches with the sizes of the old code back
        # when Pyglet drew the text.
        font_size *= 1.25

        # Text isn't anti-aliased, so we'll draw big, and then shrink
        scale_up = 5
        scale_down = 5

        font_size *= scale_up

        # If the cache gets too large, dump it and start over.
        if len(PILText.cache) > 5000:
            PILText.cache = {}

        key = f"{text}{color}{font_size}{width}{align}{font_name}{bold}{italic}"
        if key in PILText.cache:
            label = PILText.cache[key]
            text_sprite = label.text_sprite_list[0]

            if anchor_x == "left":
                text_sprite.center_x = start_x + text_sprite.width / 2
            elif anchor_x == "center":
                text_sprite.center_x = start_x
            elif anchor_x == "right":
                text_sprite.right = start_x
            else:
                raise ValueError(f"anchor_x should be 'left', 'center', or 'right'. Not '{anchor_x}'")

            if anchor_y == "top":
                text_sprite.center_y = start_y - text_sprite.height / 2
            elif anchor_y == "center":
                text_sprite.center_y = start_y
            elif anchor_y == "bottom" or anchor_y == "baseline":
                text_sprite.bottom = start_y
            else:
                raise ValueError(f"anchor_x should be 'left', 'center', or 'right'. Not '{anchor_y}'")

            text_sprite.angle = rotation
        else:
            label = Text()

            # Figure out the font to use
            font = None

            # Font was specified with a string
            if isinstance(font_name, str):
                try:
                    font = PIL.ImageFont.truetype(font_name, int(font_size))
                except OSError:
                    # print(f"1 Can't find font: {font_name}")
                    pass

                if font is None:
                    try:
                        temp_font_name = f"{font_name}.ttf"
                        font = PIL.ImageFont.truetype(temp_font_name, int(font_size))
                    except OSError:
                        # print(f"2 Can't find font: {temp_font_name}")
                        pass

            # We were instead given a list of font names, in order of preference
            else:
                for font_string_name in font_name:
                    try:
                        font = PIL.ImageFont.truetype(font_string_name, int(font_size))
                        # print(f"3 Found font: {font_string_name}")
                    except OSError:
                        # print(f"3 Can't find font: {font_string_name}")
                        pass

                    if font is None:
                        try:
                            temp_font_name = f"{font_name}.ttf"
                            font = PIL.ImageFont.truetype(temp_font_name, int(font_size))
                        except OSError:
                            # print(f"4 Can't find font: {temp_font_name}")
                            pass

                    if font is not None:
                        break

            # Default font if no font
            if font is None:
                font_names = ("arial.ttf",
                            "/usr/share/fonts/truetype/freefont/FreeMono.ttf",
                            '/System/Library/Fonts/SFNSDisplay.ttf')
                for font_string_name in font_names:
                    try:
                        font = PIL.ImageFont.truetype(font_string_name, int(font_size))
                        break
                    except OSError:
                        # print(f"5 Can't find font: {font_string_name}")
                        pass

            # This is stupid. We have to have an image to figure out what size
            # the text will be when we draw it. Of course, we don't know how big
            # to make the image. Catch-22. So we just make a small image we'll trash
            text_image_size = (10, 10)
            image = PIL.Image.new("RGBA", text_image_size)
            draw = PIL.ImageDraw.Draw(image)

            # Get size the text will be
            text_image_size = draw.multiline_textsize(text, font=font)

            # Create image of proper size
            text_height = text_image_size[1]
            text_width = text_image_size[0]

            image_start_x = 0
            if width == 0:
                width = text_image_size[0]
            else:
                # Wait! We were given a field width.
                if align == "center":
                    # Center text on given field width
                    field_width = width * scale_up
                    text_image_size = field_width, text_height
                    image_start_x = (field_width - text_width) // 2
                    width = field_width
                else:
                    image_start_x = 0

            # If we draw a y at 0, then the text is drawn with a baseline of 0,
            # cutting off letters that drop below the baseline. This shoves it
            # up a bit.
            image_start_y = - font_size * scale_up * 0.02
            image = PIL.Image.new("RGBA", text_image_size)
            draw = PIL.ImageDraw.Draw(image)

            # Convert to tuple if needed, because the multiline_text does not take a
            # list for a color
            if isinstance(color, list):
                color = tuple(color)
            draw.multiline_text((image_start_x, image_start_y), text, color, align=align, font=font)
            image = image.resize((width // scale_down, text_height // scale_down), resample=PIL.Image.LANCZOS)
            if blur_factor > 0:
                image = image.filter(ImageFilter.GaussianBlur(blur_factor))

            text_sprite = Sprite()
            text_sprite._texture = Texture(key)
            text_sprite._texture.image = image

            text_sprite.image = image
            text_sprite.texture_name = key
            text_sprite.width = image.width
            text_sprite.height = image.height

            if anchor_x == "left":
                text_sprite.center_x = start_x + text_sprite.width / 2
            elif anchor_x == "center":
                text_sprite.center_x = start_x
            elif anchor_x == "right":
                text_sprite.right = start_x
            else:
                raise ValueError(f"anchor_x should be 'left', 'center', or 'right'. Not '{anchor_x}'")

            if anchor_y == "top":
                text_sprite.center_y = start_y + text_sprite.height / 2
            elif anchor_y == "center":
                text_sprite.center_y = start_y
            elif anchor_y == "bottom" or anchor_y == "baseline":
                text_sprite.bottom = start_y
            else:
                raise ValueError(f"anchor_x should be 'top', 'center', 'bottom', or 'baseline'. Not '{anchor_y}'")

            text_sprite.angle = rotation

            from arcade.sprite_list import SpriteList
            label.text_sprite_list = SpriteList()
            label.text_sprite_list.append(text_sprite)

            PILText.cache[key] = label
        control.width = text_sprite.width
        label.text_sprite_list.draw()

