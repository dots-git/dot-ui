from ..libraries import *
from ..widgets.widgets import *


class DefaultRenderer:
    """A class for rendering Renderer content"""

    _corner_radius = 7
    _shadow_radius = 30
    _shadow_opacity = .7
    _shadow_offset = Vector2(4, 4)
    _color = Color.DARK_GRAY

    # Precomputed shadow slices to allow for
    # high quality shadows with sensible performance
    _slice_block_size = 10

    _shadow_slices = {}

    @staticmethod
    def initialize():
        DefaultRenderer.update()

    @staticmethod
    def update():
        DefaultRenderer._precompute_shadow_slices()

    @staticmethod
    def set_default_color(color):
        DefaultRenderer._color = color

    @staticmethod
    def set_corner_radius(radius, update=False):
        """Change the corner radius. Requires calling update() to take full effect if update is False"""
        DefaultRenderer._corner_radius = radius
        if update:
            DefaultRenderer.update()

    @staticmethod
    def set_shadow_radius(radius, update=False):
        """Change the shadow radius. Requires calling update() to take full effect if update is False"""
        DefaultRenderer._shadow_radius = radius
        if update:
            DefaultRenderer.update()

    def set_shadow_offset(offset: Vector2):
        """Change the shadow offset"""
        DefaultRenderer._DefaultRenderer._shadow_offset = offset

    @staticmethod
    def _precompute_shadow_slices(shadow_opacity, pseudo_radius):
        print("Precomputing shadow slices")
        cutoff_at = 0.5 / 255
        surface_size = int(
            sqrt(-log(cutoff_at)) * DefaultRenderer._shadow_radius
            + pseudo_radius
            - DefaultRenderer._shadow_radius
        )

        bottom_right = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)

        for x in range(surface_size):
            for y in range(surface_size):
                distance = sqrt(x * x + y * y)
                actual_distance = (
                    distance - pseudo_radius + DefaultRenderer._shadow_radius
                )
                if actual_distance < 0:
                    alpha = 1
                else:
                    alpha = (
                        exp(-((actual_distance / DefaultRenderer._shadow_radius) ** 2))
                        * 255
                        * shadow_opacity
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
                actual_distance = (
                    distance - pseudo_radius + DefaultRenderer._shadow_radius
                )
                if actual_distance < 0:
                    alpha = 1
                else:
                    alpha = (
                        exp(-((actual_distance / DefaultRenderer._shadow_radius) ** 2))
                        * 255
                        * shadow_opacity
                    )
                    mod = alpha % 1
                    alpha = int(alpha) + (
                        1 if alpha < 254 and mod > random.random() else 0
                    )
                right.set_at((x, y), (0, 0, 0, alpha))
            top = pygame.transform.rotate(right, 90)
            bottom = pygame.transform.rotate(right, -90)
            left = pygame.transform.rotate(right, 180)

            right_block = pygame.Surface(
                (surface_size, DefaultRenderer._slice_block_size), pygame.SRCALPHA
            )
            for x in range(surface_size):
                for y in range(DefaultRenderer._slice_block_size):
                    distance = x
                    actual_distance = (
                        distance - pseudo_radius + DefaultRenderer._shadow_radius
                    )
                    if actual_distance < 0:
                        alpha = 1
                    else:
                        alpha = (
                            exp(
                                -(
                                    (actual_distance / DefaultRenderer._shadow_radius)
                                    ** 2
                                )
                            )
                            * 255
                            * shadow_opacity
                        )
                        mod = alpha % 1
                        alpha = int(alpha) + (
                            1 if alpha < 254 and mod > random.random() else 0
                        )
                    right_block.set_at((x, y), (0, 0, 0, alpha))
            top_block = pygame.transform.rotate(right_block, 90)
            bottom_block = pygame.transform.rotate(right_block, -90)
            left_block = pygame.transform.rotate(right_block, 180)

            DefaultRenderer._shadow_slice_top = top
            DefaultRenderer._shadow_slice_bottom = bottom
            DefaultRenderer._shadow_slice_left = left
            DefaultRenderer._shadow_slice_right = right

            DefaultRenderer._shadow_slice_top_block = top_block
            DefaultRenderer._shadow_slice_bottom_block = bottom_block
            DefaultRenderer._shadow_slice_left_block = left_block
            DefaultRenderer._shadow_slice_right_block = right_block

            DefaultRenderer._shadow_slice_top_left = top_left
            DefaultRenderer._shadow_slice_top_right = top_right
            DefaultRenderer._shadow_slice_bottom_left = bottom_left
            DefaultRenderer._shadow_slice_bottom_right = bottom_right

            DefaultRenderer._shadow_slices[pseudo_radius] = {
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
                "bottom_right": bottom_right
            }

    @staticmethod
    def _draw_rect_shadow(x, y, width, height, surface: Surface):
        x, y, width, height = [int(v) for v in (x, y, width, height)]

        actual_radius = DefaultRenderer._corner_radius
        if actual_radius > int(width / 2):
            actual_radius = int(width / 2)
        if actual_radius > int(height / 2):
            actual_radius = int(height / 2)
        
        min_size = min(width, height)
        pseudo_radius = max(actual_radius, DefaultRenderer._shadow_radius)

        shadow_opacity = (min_size / 2 / pseudo_radius)**1
        shadow_opacity = 1 if shadow_opacity >= 1 else shadow_opacity

        if not pseudo_radius in DefaultRenderer._shadow_slices.keys():
            DefaultRenderer._precompute_shadow_slices(shadow_opacity, pseudo_radius)
        DefaultRenderer._shadow_slices[pseudo_radius]["used"] = True

        slice_size = DefaultRenderer._shadow_slices[pseudo_radius][
            "bottom_right"
        ].get_size()[0]
        
        radius_offset = min(DefaultRenderer._shadow_radius - actual_radius, int(min_size / 2))

        keys = [key for key in DefaultRenderer._shadow_slices[pseudo_radius].keys()]

        for key in keys:
            if key != 'used':
                DefaultRenderer._shadow_slices[pseudo_radius][key].set_alpha(shadow_opacity * 255)

        surface.blit(
            DefaultRenderer._shadow_slices[pseudo_radius]["top_left"],
            (
                DefaultRenderer._shadow_offset.x + x - slice_size + radius_offset,
                DefaultRenderer._shadow_offset.y + y - slice_size + radius_offset,
            ),
        )
        surface.blit(
            DefaultRenderer._shadow_slices[pseudo_radius][
                "bottom_right"
            ],
            (
                DefaultRenderer._shadow_offset.x + x - radius_offset + width,
                DefaultRenderer._shadow_offset.y + y - radius_offset + height,
            ),
        )
        surface.blit(
            DefaultRenderer._shadow_slices[pseudo_radius]["top_right"],
            (
                DefaultRenderer._shadow_offset.x + x - radius_offset + width,
                DefaultRenderer._shadow_offset.y + y - slice_size + radius_offset,
            ),
        )
        surface.blit(
            DefaultRenderer._shadow_slices[pseudo_radius]["bottom_left"],
            (
                DefaultRenderer._shadow_offset.x + x - slice_size + radius_offset,
                DefaultRenderer._shadow_offset.y + y - radius_offset + height,
            ),
        )

        x_range_to_fill = width - 2 * radius_offset
        x_block_amt = int(x_range_to_fill / DefaultRenderer._slice_block_size)
        x_block_end = x_block_amt * DefaultRenderer._slice_block_size

        y_range_to_fill = height - 2 * radius_offset
        y_block_amt = int(y_range_to_fill / DefaultRenderer._slice_block_size)
        y_block_end = y_block_amt * DefaultRenderer._slice_block_size

        top_block = DefaultRenderer._shadow_slices[pseudo_radius]["top_block"]
        bottom_block = DefaultRenderer._shadow_slices[pseudo_radius]["bottom_block"]
                
        for i in range(x_block_amt):
            surface.blit(
                top_block,
                (
                    DefaultRenderer._shadow_offset.x
                    + x
                    + radius_offset
                    + i * DefaultRenderer._slice_block_size,
                    DefaultRenderer._shadow_offset.y + y - slice_size + radius_offset,
                ),
            )
            surface.blit(
                bottom_block,
                (
                    DefaultRenderer._shadow_offset.x
                    + x
                    + radius_offset
                    + i * DefaultRenderer._slice_block_size,
                    DefaultRenderer._shadow_offset.y + y - radius_offset + height,
                ),
            )

        left_block = DefaultRenderer._shadow_slices[pseudo_radius]["left_block"]
        right_block = DefaultRenderer._shadow_slices[pseudo_radius]["right_block"]
        for i in range(y_block_amt):
            surface.blit(
                left_block,
                (
                    DefaultRenderer._shadow_offset.x + x - slice_size + radius_offset,
                    DefaultRenderer._shadow_offset.y
                    + y
                    + radius_offset
                    + i * DefaultRenderer._slice_block_size,
                ),
            )
            surface.blit(
                right_block,
                (
                    DefaultRenderer._shadow_offset.x + x - radius_offset + width,
                    DefaultRenderer._shadow_offset.y
                    + y
                    + radius_offset
                    + i * DefaultRenderer._slice_block_size,
                ),
            )

        top = DefaultRenderer._shadow_slices[pseudo_radius]["top"]
        bottom = DefaultRenderer._shadow_slices[pseudo_radius]["bottom"]

        for i in range(x_block_end, x_range_to_fill):
            surface.blit(
                top,
                (
                    DefaultRenderer._shadow_offset.x + x + radius_offset + i,
                    DefaultRenderer._shadow_offset.y + y - slice_size + radius_offset,
                ),
            )
            surface.blit(
                bottom,
                (
                    DefaultRenderer._shadow_offset.x + x + radius_offset + i,
                    DefaultRenderer._shadow_offset.y + y - radius_offset + height,
                ),
            )

        left = DefaultRenderer._shadow_slices[pseudo_radius]["left"]
        right = DefaultRenderer._shadow_slices[pseudo_radius]["right"]
        
        for i in range(y_block_end, y_range_to_fill):
            surface.blit(
                left,
                (
                    DefaultRenderer._shadow_offset.x + x - slice_size + radius_offset,
                    DefaultRenderer._shadow_offset.y + y + radius_offset + i,
                ),
            )
            surface.blit(
                right,
                (
                    DefaultRenderer._shadow_offset.x + x - radius_offset + width,
                    DefaultRenderer._shadow_offset.y + y + radius_offset + i,
                ),
            )

        fill_surface_width = width - 2 * radius_offset
        fill_surface_height = height - 2 * radius_offset
        if fill_surface_width > 0 < fill_surface_height:
            fill_surface = pygame.Surface(
                (fill_surface_width, fill_surface_height), pygame.SRCALPHA
            )
            fill_surface.fill((0, 0, 0))
            fill_surface.set_alpha(
                shadow_opacity * 255
            )
            surface.blit(
                fill_surface,
                (
                    DefaultRenderer._shadow_offset.x + x + radius_offset,
                    DefaultRenderer._shadow_offset.y + y + radius_offset,
                ),
            )

    @staticmethod
    def tick():
        keys = [key for key in DefaultRenderer._shadow_slices.keys()]
        for key in keys:
            if DefaultRenderer._shadow_slices[key]['used'] != True:
                DefaultRenderer._shadow_slices.pop(key)
            else:
                DefaultRenderer._shadow_slices[key]['used'] = False

    @staticmethod
    def render(widget: Widget, delta: float):
        if isinstance(widget, Container):
            widget.surface.fill(DefaultRenderer._color.t)
            shadow_surface = pygame.Surface((width(), height()), pygame.SRCALPHA)
            for child in widget.floating_widgets:
                DefaultRenderer._draw_rect_shadow(
                    child.pos.x, child.pos.y, child.size.x, child.size.y, shadow_surface
                )
            shadow_surface.set_alpha(DefaultRenderer._shadow_opacity * 255)
            widget.surface.blit(shadow_surface, (0, 0))
            for child in widget.floating_widgets:
                DefaultRenderer.render(child, delta)
                widget.surface.blit(
                    rounded(child.surface, DefaultRenderer._corner_radius),
                    (child.pos.x, child.pos.y),
                )
        else:
            widget.surface.fill(DefaultRenderer._color.t)
