from cmath import inf
from typing import Tuple
from ..libraries import *
from ..widgets.widgets import *


class DotRenderer:
    """A class for rendering Renderer content"""

    _corner_radius = 7
    _shadow_radius = 20
    _shadow_opacity = 0.6
    _shadow_offset = Vector2(7, 7)
    _color = Color.DARK_GRAY
    # 0: No shadow, 1: shadow around entire text body, 2: shadow around each word (recommended), 3: shadow around each character
    _text_shadow_detail = 1

    # Precomputed shadow slices to allow for
    # high quality shadows with sensible performance
    _slice_block_size = 10

    _shadow_slices = {}

    _shadow_surfaces = {}

    @staticmethod
    def initialize():
        DotRenderer.update()

    @staticmethod
    def update():
        DotRenderer._shadow_slices = {}
        DotRenderer._shadow_surfaces = {}

    @staticmethod
    def set_default_color(color):
        DotRenderer._color = color

    @staticmethod
    def set_corner_radius(radius, update=False):
        """Change the corner radius. Requires calling update() to take full effect if update is False"""
        DotRenderer._corner_radius = radius
        if update:
            DotRenderer.update()

    @staticmethod
    def set_shadow_radius(radius, update=False):
        """Change the shadow radius. Requires calling update() to take full effect if update is False"""
        DotRenderer._shadow_radius = radius
        if update:
            DotRenderer.update()

    @staticmethod
    def set_shadow_offset(offset: Vector2):
        """Change the shadow offset"""
        DotRenderer._shadow_offset = offset

    @staticmethod
    def set_shadow_opacity(opacity: float):
        """Change the shadow opacity"""
        DotRenderer._shadow_opacity = opacity

    @staticmethod
    def _precompute_shadow_slices(pseudo_radius):
        print("Computing shadow slices")
        cutoff_at = 0.5 / 255
        surface_size = int(
            sqrt(-log(cutoff_at)) * DotRenderer._shadow_radius
            + pseudo_radius
            - DotRenderer._shadow_radius
        )

        bottom_right = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)

        for x in range(surface_size):
            for y in range(surface_size):
                distance = sqrt(x * x + y * y)
                actual_distance = distance - pseudo_radius + DotRenderer._shadow_radius
                if actual_distance < 0:
                    alpha = 255
                else:
                    alpha = (
                        exp(-((actual_distance / DotRenderer._shadow_radius) ** 2))
                        * 255
                    )
                    mod = alpha % 1
                    alpha = int(alpha) + (
                        1 if alpha < 254 and mod > random.random() else 0
                    )
                bottom_right.set_at((x, y), (0, 0, 0, alpha))

        top_left = pygame.transform.rotate(bottom_right, 180)
        top_right = pygame.transform.rotate(bottom_right, 90)
        bottom_left = pygame.transform.rotate(bottom_right, -90)

        right = pygame.Surface((surface_size, 1), pygame.SRCALPHA)
        y = 0
        for x in range(surface_size):
            distance = x
            actual_distance = distance - pseudo_radius + DotRenderer._shadow_radius
            if actual_distance < 0:
                alpha = 255
            else:
                alpha = (
                    exp(-((actual_distance / DotRenderer._shadow_radius) ** 2)) * 255
                )
                mod = alpha % 1
                alpha = int(alpha) + (1 if alpha < 254 and mod > random.random() else 0)
            right.set_at((x, y), (0, 0, 0, alpha))

        top = pygame.transform.rotate(right, 90)
        bottom = pygame.transform.rotate(right, -90)
        left = pygame.transform.rotate(right, 180)

        right_block = pygame.Surface(
            (surface_size, DotRenderer._slice_block_size), pygame.SRCALPHA
        )
        for x in range(surface_size):
            for y in range(DotRenderer._slice_block_size):
                distance = x
                actual_distance = distance - pseudo_radius + DotRenderer._shadow_radius
                if actual_distance < 0:
                    alpha = 255
                else:
                    alpha = (
                        exp(-((actual_distance / DotRenderer._shadow_radius) ** 2))
                        * 255
                    )
                    mod = alpha % 1
                    alpha = int(alpha) + (
                        1 if alpha < 254 and mod > random.random() else 0
                    )
                right_block.set_at((x, y), (0, 0, 0, alpha))
        top_block = pygame.transform.rotate(right_block, 90)
        bottom_block = pygame.transform.rotate(right_block, -90)
        left_block = pygame.transform.rotate(right_block, 180)

        DotRenderer._shadow_slice_top = top
        DotRenderer._shadow_slice_bottom = bottom
        DotRenderer._shadow_slice_left = left
        DotRenderer._shadow_slice_right = right

        DotRenderer._shadow_slice_top_block = top_block
        DotRenderer._shadow_slice_bottom_block = bottom_block
        DotRenderer._shadow_slice_left_block = left_block
        DotRenderer._shadow_slice_right_block = right_block

        DotRenderer._shadow_slice_top_left = top_left
        DotRenderer._shadow_slice_top_right = top_right
        DotRenderer._shadow_slice_bottom_left = bottom_left
        DotRenderer._shadow_slice_bottom_right = bottom_right

        DotRenderer._shadow_slices[pseudo_radius] = {
            "used": True,
            "top": top,
            "bottom": bottom,
            "left": left,
            "right": right,
            "top_block": top_block,
            "bottom_block": bottom_block,
            "left_block": left_block,
            "right_block": right_block,
            "top_left": top_left,
            "top_right": top_right,
            "bottom_left": bottom_left,
            "bottom_right": bottom_right,
        }

    @staticmethod
    def _get_shadow(
        x, y, width, height, opacity_multiplier, radius=None
    ) -> Tuple[Surface, int, int]:

        x, y, width, height = [int(v) for v in (x, y, width, height)]

        if radius is None:
            radius = DotRenderer._corner_radius
        if radius > int(width / 2):
            radius = int(width / 2)
        if radius > int(height / 2):
            radius = int(height / 2)

        min_size = min(width, height)
        pseudo_radius = max(radius, DotRenderer._shadow_radius)

        shadow_opacity = min_size / 2 / pseudo_radius
        shadow_opacity = 1 if shadow_opacity >= 1 else shadow_opacity

        if not pseudo_radius in DotRenderer._shadow_slices.keys():
            DotRenderer._precompute_shadow_slices(pseudo_radius)
        DotRenderer._shadow_slices[pseudo_radius]["used"] = True

        slice_size = DotRenderer._shadow_slices[pseudo_radius][
            "bottom_right"
        ].get_size()[0]

        radius_offset = min(
            max(DotRenderer._shadow_radius - radius, radius),
            int(min_size / 2),
        )

        surface_key = (
            str(int(width))
            + " "
            + str(int(height))
            + " "
            + str(int(opacity_multiplier))
            + " "
            + str(int(pseudo_radius))
        )
        if surface_key in DotRenderer._shadow_surfaces.keys():
            DotRenderer._shadow_surfaces[surface_key]["used"] = True
            return (
                DotRenderer._shadow_surfaces[surface_key]["surface"],
                DotRenderer._shadow_offset.x + x - slice_size + radius_offset,
                DotRenderer._shadow_offset.y + y - slice_size + radius_offset,
            )
        print(
            f"Assembling shadow surface {surface_key, DotRenderer._shadow_surfaces.keys()}"
        )

        keys = [key for key in DotRenderer._shadow_slices[pseudo_radius].keys()]

        for key in keys:
            if key != "used":
                DotRenderer._shadow_slices[pseudo_radius][key].set_alpha(
                    shadow_opacity * 255 * opacity_multiplier
                )

        shadow_surface = pygame.Surface(
            (
                width + 2 * slice_size - 2 * radius_offset,
                height + 2 * slice_size - 2 * radius_offset,
            ),
            pygame.SRCALPHA,
        )

        shadow_surface.blit(
            DotRenderer._shadow_slices[pseudo_radius]["top_left"],
            (
                0,
                0,
            ),
        )
        shadow_surface.blit(
            DotRenderer._shadow_slices[pseudo_radius]["bottom_right"],
            (
                width - 2 * radius_offset + slice_size,
                height - 2 * radius_offset + slice_size,
            ),
        )
        shadow_surface.blit(
            DotRenderer._shadow_slices[pseudo_radius]["top_right"],
            (
                width - 2 * radius_offset + slice_size,
                0,
            ),
        )
        shadow_surface.blit(
            DotRenderer._shadow_slices[pseudo_radius]["bottom_left"],
            (
                0,
                height - 2 * radius_offset + slice_size,
            ),
        )

        x_range_to_fill = width - 2 * radius_offset
        x_block_amt = int(x_range_to_fill / DotRenderer._slice_block_size)
        x_block_end = x_block_amt * DotRenderer._slice_block_size

        y_range_to_fill = height - 2 * radius_offset
        y_block_amt = int(y_range_to_fill / DotRenderer._slice_block_size)
        y_block_end = y_block_amt * DotRenderer._slice_block_size

        top_block = DotRenderer._shadow_slices[pseudo_radius]["top_block"]
        bottom_block = DotRenderer._shadow_slices[pseudo_radius]["bottom_block"]

        for i in range(x_block_amt):
            shadow_surface.blit(
                top_block,
                (
                    i * DotRenderer._slice_block_size + slice_size,
                    0,
                ),
            )
            shadow_surface.blit(
                bottom_block,
                (
                    i * DotRenderer._slice_block_size + slice_size,
                    height - 2 * radius_offset + slice_size,
                ),
            )

        left_block = DotRenderer._shadow_slices[pseudo_radius]["left_block"]
        right_block = DotRenderer._shadow_slices[pseudo_radius]["right_block"]
        for i in range(y_block_amt):
            shadow_surface.blit(
                left_block,
                (
                    0,
                    i * DotRenderer._slice_block_size + slice_size,
                ),
            )
            shadow_surface.blit(
                right_block,
                (
                    width - 2 * radius_offset + slice_size,
                    i * DotRenderer._slice_block_size + slice_size,
                ),
            )

        top = DotRenderer._shadow_slices[pseudo_radius]["top"]
        bottom = DotRenderer._shadow_slices[pseudo_radius]["bottom"]

        for i in range(x_block_end, x_range_to_fill):
            shadow_surface.blit(
                top,
                (
                    i + slice_size,
                    0,
                ),
            )
            shadow_surface.blit(
                bottom,
                (
                    i + slice_size,
                    height - 2 * radius_offset + slice_size,
                ),
            )

        left = DotRenderer._shadow_slices[pseudo_radius]["left"]
        right = DotRenderer._shadow_slices[pseudo_radius]["right"]

        for i in range(y_block_end, y_range_to_fill):
            shadow_surface.blit(
                left,
                (
                    0,
                    i + slice_size,
                ),
            )
            shadow_surface.blit(
                right,
                (
                    width - 2 * radius_offset + slice_size,
                    i + slice_size,
                ),
            )

        fill_surface_width = width - 2 * radius_offset
        fill_surface_height = height - 2 * radius_offset
        if 0 < min(fill_surface_height, fill_surface_width):
            fill_surface = pygame.Surface(
                (fill_surface_width, fill_surface_height), pygame.SRCALPHA
            )
            fill_surface.fill((0, 0, 0))
            fill_surface.set_alpha(shadow_opacity * opacity_multiplier * 255)
            shadow_surface.blit(
                fill_surface,
                (
                    slice_size,
                    slice_size,
                ),
            )

        DotRenderer._shadow_surfaces[surface_key] = {
            "surface": shadow_surface,
            "used": True,
        }

        return (
            shadow_surface,
            DotRenderer._shadow_offset.x + x - slice_size + radius_offset,
            DotRenderer._shadow_offset.y + y - slice_size + radius_offset,
        )

    @staticmethod
    def tick():
        keys = [key for key in DotRenderer._shadow_slices.keys()]
        for key in keys:
            if DotRenderer._shadow_slices[key]["used"] != True:
                DotRenderer._shadow_slices.pop(key)
            else:
                DotRenderer._shadow_slices[key]["used"] = False
        keys = [key for key in DotRenderer._shadow_surfaces.keys()]
        for key in keys:
            if DotRenderer._shadow_surfaces[key]["used"] != True:
                DotRenderer._shadow_surfaces.pop(key)
            else:
                DotRenderer._shadow_surfaces[key]["used"] = False

    @staticmethod
    def render(widget: Widget, delta: float):
        widget.surface.fill(
            widget.background_color.t
            if widget.background_color
            else DotRenderer._color.t
        )

        widget.shadow_surfaces = []

        if (
            not widget.background_color or widget.background_color[3] != 0
        ) and not isinstance(widget, Window):
            pos = widget.pos.copy()
            if widget.size.x < 0:
                pos.x = pos.x + widget.size.x
            if widget.size.y < 0:
                pos.y = pos.y + widget.size.y
            widget.shadow_surfaces.append(
                DotRenderer._get_shadow(
                    pos.x,
                    pos.y,
                    abs(widget.size.x),
                    abs(widget.size.y),
                    widget.opacity,
                )
            )

        if isinstance(widget, Container):
            shadow_surface = pygame.Surface((width(), height()), pygame.SRCALPHA)
            for child in widget.child_list:
                DotRenderer.render(child, delta)
                for surface, x, y in child.shadow_surfaces:
                    widget.surface.blit(surface, (x, y))

            shadow_surface.set_alpha(DotRenderer._shadow_opacity * 255)
            widget.surface.blit(shadow_surface, (0, 0))
            for child in widget.child_list:
                pos = child.pos.copy()
                if child.size.x < 0:
                    pos.x = pos.x + child.size.x
                if child.size.y < 0:
                    pos.y = pos.y + child.size.y
                widget.surface.blit(
                    rounded(child.surface, DotRenderer._corner_radius),
                    (round(pos.x), round(pos.y)),
                )
        elif isinstance(widget, Text):
            text_surface = widget.font.render(widget.text, True, widget.color.t)

            text_surface_size = Vector2(text_surface.get_size())
            widget_center = widget.size / 2
            centered_pos = widget_center - text_surface_size / 2
            widget_bottom_right = widget.size
            pos_bottom_right = widget_bottom_right - text_surface_size
            pos = Vector2()
            if widget.alignment_x == "center":
                pos.x += centered_pos.x
            if widget.alignment_x == "right":
                pos.x += pos_bottom_right.x
            if widget.alignment_y == "center":
                pos.y += centered_pos.y
            if widget.alignment_y == "bottom":
                pos.y += pos_bottom_right.y
            widget.surface.blit(text_surface, pos.round().asarray())
            metrics = widget.font.metrics(widget.text)

            pos += widget.pos

            if DotRenderer._text_shadow_detail == 1:
                character_heights = [char[3] for char in metrics]
                height_avg = sum(character_heights) / len(character_heights)

                y_offset = (text_surface_size.y - height_avg) / 2

                widget.shadow_surfaces.append(
                    DotRenderer._get_shadow(
                        pos.x,
                        pos.y + y_offset,
                        text_surface_size.x,
                        height_avg,
                        widget.opacity * 0.5,
                        inf,
                    )
                )

            if DotRenderer._text_shadow_detail == 3:
                char_pos = 0
                for char in metrics:
                    widget.shadow_surfaces.append(
                        DotRenderer._get_shadow(
                            pos.x + char[0] + char_pos,
                            pos.y + widget.font_size - char[3],
                            char[1],
                            char[3],
                            widget.opacity * 0.5,
                            inf,
                        )
                    )
                    char_pos += char[4]

        else:
            pass
