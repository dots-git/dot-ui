from ..libraries import *
from ..widgets.widgets import *


class DefaultRenderer:
    """A class for rendering Renderer content"""

    _corner_radius = 5
    _shadow_radius = 10
    _shadow_opacity = 0.7
    _shadow_offset = Vector2(4, 4)
    _color = Color.DARK_GRAY

    # Precomputed shadow slices to allow for
    # high quality shadows with sensible performance
    _slice_block_size = 10

    _shadow_slices = {
    }

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
    def _precompute_shadow_slices(radius, pseudo_radius):
        print("Precomputing shadow slices")
        cutoff_at = 0.5 / 255
        surface_size = int(
            sqrt(-log(cutoff_at)) * DefaultRenderer._shadow_radius + pseudo_radius - DefaultRenderer._shadow_radius
        )

        bottom_right = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)

        shadow_opacity = radius / DefaultRenderer._shadow_radius * DefaultRenderer._shadow_opacity
        shadow_opacity = 1 if shadow_opacity >= 1 else shadow_opacity

        for x in range(surface_size):
            for y in range(surface_size):
                distance = sqrt(x * x + y * y)
                actual_distance = distance - pseudo_radius + DefaultRenderer._shadow_radius
                if actual_distance < 0:
                    alpha = 1
                else:
                    alpha = (
                        exp(-((actual_distance / DefaultRenderer._shadow_radius) ** 2))
                        * 255
                        * shadow_opacity
                    )
                    mod = alpha % 1
                    alpha = int(alpha) + (1 if alpha < 254 and mod > random.random() else 0)
                bottom_right.set_at((x, y), (0, 0, 0, alpha))

            top_left = pygame.transform.rotate(bottom_right, 180)
            top_right = pygame.transform.rotate(bottom_right, 90)
            bottom_left = pygame.transform.rotate(bottom_right, -90)

            right = pygame.Surface((surface_size, 1), pygame.SRCALPHA)
            y = 0
            for x in range(surface_size):
                distance = x
                actual_distance = distance - pseudo_radius + DefaultRenderer._shadow_radius
                if actual_distance < 0:
                    alpha = 1
                else:
                    alpha = (
                        exp(-((actual_distance / DefaultRenderer._shadow_radius) ** 2)) * 255 * shadow_opacity
                    )
                    mod = alpha % 1
                    alpha = int(alpha) + (1 if alpha < 254 and mod > random.random() else 0)
                right.set_at((x, y), (0, 0, 0, alpha))
            top = pygame.transform.rotate(right, 90)
            bottom = pygame.transform.rotate(right, -90)
            left = pygame.transform.rotate(right, 180)


            right_block = pygame.Surface((surface_size, DefaultRenderer._slice_block_size), pygame.SRCALPHA)
            for x in range(surface_size):
                for y in range(DefaultRenderer._slice_block_size):
                    distance = x
                    actual_distance = distance - pseudo_radius + DefaultRenderer._shadow_radius
                    if actual_distance < 0:
                        alpha = 1
                    else:
                        alpha = (
                            exp(-((actual_distance / DefaultRenderer._shadow_radius) ** 2)) * 255 * shadow_opacity
                        )
                        mod = alpha % 1
                        alpha = int(alpha) + (1 if alpha < 254 and mod > random.random() else 0)
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

            DefaultRenderer._shadow_slices[radius, pseudo_radius] = {
                'used': True,
                'top': top,
                'bottom': bottom,
                'left': left,
                'right': right,
                'top_block': top_block,
                'bottom_block': bottom_block,
                'left_block': left_block,
                'right_block': right_block,
                'top_left': top_left,
                'top_right': top_right,
                'bottom_left': bottom_left,
                'bottom_right': bottom_right
            }

    @staticmethod
    def _draw_rect_shadow(x, y, width, height, surface: Surface):
        actual_radius = DefaultRenderer._corner_radius
        if actual_radius > width / 2:
            actual_radius = width / 2
        if actual_radius > height / 2:
            actual_radius = height / 2
        
        pseudo_radius = max(actual_radius, DefaultRenderer._shadow_radius)
        
        if not (actual_radius, pseudo_radius) in DefaultRenderer._shadow_slices.keys():
            DefaultRenderer._precompute_shadow_slices(actual_radius, pseudo_radius)
        DefaultRenderer._shadow_slices[actual_radius, pseudo_radius]['used'] = True

        slice_size = DefaultRenderer._shadow_slices[actual_radius, pseudo_radius]['bottom_right'].get_size()[0]
        radius_offset = DefaultRenderer._shadow_radius - actual_radius

        surface.blit(
            DefaultRenderer._shadow_slices[actual_radius, pseudo_radius]['top_left'],
            (
                DefaultRenderer._shadow_offset.x + x - slice_size + radius_offset,
                DefaultRenderer._shadow_offset.y + y - slice_size + radius_offset,
            )
        )
        surface.blit(
            DefaultRenderer._shadow_slices[actual_radius, pseudo_radius]['bottom_right'],
            (
                DefaultRenderer._shadow_offset.x + x - radius_offset + width, 
                DefaultRenderer._shadow_offset.y + y - radius_offset + height
            )
        )
        surface.blit(
            DefaultRenderer._shadow_slices[actual_radius, pseudo_radius]['top_right'],
            (
                DefaultRenderer._shadow_offset.x + x - radius_offset + width, 
                DefaultRenderer._shadow_offset.y + y - slice_size + radius_offset, 
            )
        )
        surface.blit(
            DefaultRenderer._shadow_slices[actual_radius, pseudo_radius]['bottom_left'],
            (
                DefaultRenderer._shadow_offset.x + x - slice_size + radius_offset, 
                DefaultRenderer._shadow_offset.y + y - radius_offset + height
            )
        )

        x_range_to_fill = width - 2 * radius_offset
        x_block_amt = int(x_range_to_fill / DefaultRenderer._slice_block_size)
        x_block_end = x_block_amt * DefaultRenderer._slice_block_size
        
        y_range_to_fill = height - 2 * radius_offset
        y_block_amt = int(y_range_to_fill / DefaultRenderer._slice_block_size)
        y_block_end = y_block_amt * DefaultRenderer._slice_block_size

        for i in range(x_block_amt):
            surface.blit(
                DefaultRenderer._shadow_slices[actual_radius, pseudo_radius]['top_block'],
                (
                    DefaultRenderer._shadow_offset.x + x + radius_offset + i * DefaultRenderer._slice_block_size, 
                    DefaultRenderer._shadow_offset.y + y - slice_size + radius_offset
                )
            )
            surface.blit(
                DefaultRenderer._shadow_slices[actual_radius, pseudo_radius]['bottom_block'],
                (
                    DefaultRenderer._shadow_offset.x + x + radius_offset + i * DefaultRenderer._slice_block_size, 
                    DefaultRenderer._shadow_offset.y + y - radius_offset + height
                )
            )

        for i in range(x_block_end, x_range_to_fill):
            surface.blit(
                DefaultRenderer._shadow_slices[actual_radius, pseudo_radius]['top'],
                (
                    DefaultRenderer._shadow_offset.x + x + radius_offset + i, 
                    DefaultRenderer._shadow_offset.y + y - slice_size + radius_offset
                )
            )
            surface.blit(
                DefaultRenderer._shadow_slices[actual_radius, pseudo_radius]['bottom'],
                (
                    DefaultRenderer._shadow_offset.x + x + radius_offset + i, 
                    DefaultRenderer._shadow_offset.y + y - radius_offset + height
                )
            )

        for i in range(y_block_amt):
            surface.blit(
                DefaultRenderer._shadow_slices[actual_radius, pseudo_radius]['left_block'],
                (
                    DefaultRenderer._shadow_offset.x + x - slice_size + radius_offset, 
                    DefaultRenderer._shadow_offset.y + y + radius_offset + i * DefaultRenderer._slice_block_size
                )
            )
            surface.blit(
                DefaultRenderer._shadow_slices[actual_radius, pseudo_radius]['right_block'],
                (
                    DefaultRenderer._shadow_offset.x + x - radius_offset + width, 
                    DefaultRenderer._shadow_offset.y + y + radius_offset + i * DefaultRenderer._slice_block_size
                )
            )
        
        for i in range(y_block_end, y_range_to_fill):
            surface.blit(
                DefaultRenderer._shadow_slices[actual_radius, pseudo_radius]['left'],
                (
                    DefaultRenderer._shadow_offset.x + x - slice_size + radius_offset, 
                    DefaultRenderer._shadow_offset.y + y + radius_offset + i
                )
            )
            surface.blit(
                DefaultRenderer._shadow_slices[actual_radius, pseudo_radius]['right'],
                (
                    DefaultRenderer._shadow_offset.x + x - radius_offset + width, 
                    DefaultRenderer._shadow_offset.y + y + radius_offset + i
                )
            )

        fill_surface = pygame.Surface((width - 2 * radius_offset, height - 2 * radius_offset))
        fill_surface.set_alpha(0.7 * 255)
        surface.blit(
            fill_surface, 
            (
                DefaultRenderer._shadow_offset.x + x + radius_offset, DefaultRenderer._shadow_offset.y + y + radius_offset
            )
        )



    @staticmethod
    def tick():
        for key in DefaultRenderer._shadow_slices.keys():
            if not DefaultRenderer._shadow_slices[key]['used']:
                DefaultRenderer._shadow_slices.pop(key)

    @staticmethod
    def render(widget: Widget, delta: float):
        if isinstance(widget, Container):
            widget.surface.fill(DefaultRenderer._color.t)
            for child in widget.floating_widgets:
                DefaultRenderer._draw_rect_shadow(child.pos.x, child.pos.y, child.size.x, child.size.y, widget.surface)
                DefaultRenderer.render(child, delta)
                widget.surface.blit(child.surface, (child.pos.x, child.pos.y))
        else:
            widget.surface.fill(DefaultRenderer._color.t)