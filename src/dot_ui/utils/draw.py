from numpy import array
from pygame import SRCALPHA, Rect, Surface
from .color_constants import BLACK
from .vectors import Vector2
from ..pg import gfxdraw, display, surfarray


class Draw:
    """
    Stores defaults for drawing as static variables
    """

    fill_color = BLACK
    stroke_color = BLACK
    fill = True
    stroke_width = 0

    offset = Vector2(0, 0)
    scale = Vector2(1, 1)

    surface = None


#  ---  Some functions for drawing various shapes  ---  #


def circle(
    x,
    y,
    radius,
    offset=None,
    scale=None,
    fill_color=None,
    stroke_color=None,
    fill=None,
    stroke_width=None,
    surface=None,
):
    """
    Draws a circle
    """

    # Get defaults
    if offset is None:
        offset = Draw.offset
    if scale is None:
        scale = Draw.scale
    if fill_color is None:
        fill_color = Draw.fill_color
    if stroke_color is None:
        stroke_color = Draw.stroke_color
    if fill is None:
        fill = Draw.fill
    if stroke_width is None:
        stroke_width = Draw.stroke_width
    if surface is None:
        surface = Draw.surface
    if surface is None:
        surface = display.get_surface()

    # Round values to integers
    x = round(x)
    y = round(y)
    radius = round(radius)

    # If the scale ratio is not 1:1, draw an ellipse
    if scale.x != scale.y:
        return ellipse(
            x,
            y,
            radius * 2,
            radius * 2,
            offset=offset,
            scale=scale,
            fill_color=fill_color,
            stroke_color=stroke_color,
            fill=fill,
            stroke_width=stroke_width,
            surface=surface,
        )

    # Scale and offset
    x, y = (x * scale.x + offset.x, y * scale.y + offset.y)
    radius *= scale.x

    # Draw
    if fill and not (
        # Don't fill if the shortcut drawing method is used and the stroke is opaque.
        # It would in this case be hidden and therefore redundant.
        stroke_width > 1
        and (len(fill_color) < 4 or fill_color[3] == 255)
        and (len(stroke_color) < 4 or stroke_color[3] == 255)
    ):
        _antialiased_filled_circle(x, y, radius, fill_color, surface)
    if stroke_width == 1:
        gfxdraw.aacircle(surface, int(x), int(y), int(radius), stroke_color)
    elif stroke_width > 1:
        # If the circle is filled with an opaque color, we can draw a bigger circle and
        # draw the fill on top of it
        if len(fill_color) < 4 or fill_color[3] == 255:
            _antialiased_filled_circle(
                x, y, radius + stroke_width / 2, stroke_color, surface
            )
            if fill:
                _antialiased_filled_circle(
                    x, y, radius - stroke_width / 2, fill_color, surface
                )
        # Otherwise, we need to draw the circle outline, which takes conversions to arrays
        else:
            _thick_circle_outline(x, y, radius, stroke_width, stroke_color, surface)


def _antialiased_filled_circle(x, y, radius, color, surface: Surface):
    """
    Internal function for drawing an antialiased filled circle
    """
    if radius > 0:
        gfxdraw.filled_circle(surface, round(x), round(y), round(radius), color)
        gfxdraw.aacircle(surface, round(x), round(y), round(radius), color)


def _thick_circle_outline(x, y, radius, thickness, color, surface: Surface):
    """
    Internal function for drawing a circle outline with a thickness
    """
    half_thickness = thickness / 2

    full_surface = Surface(
        (2 * radius + thickness + 2, 2 * radius + thickness + 2), SRCALPHA
    )
    full_surface.fill(color)

    try:
        alpha = color[3]
    except IndexError:
        alpha = 255

    alpha_surface = Surface((2 * radius + thickness + 2, 2 * radius + thickness + 2))
    _antialiased_filled_circle(
        radius + half_thickness,
        radius + half_thickness,
        radius + half_thickness,
        (alpha, 0, 0),
        alpha_surface,
    )
    _antialiased_filled_circle(
        radius + half_thickness,
        radius + half_thickness,
        radius - half_thickness,
        (0, 0, 0),
        alpha_surface,
    )

    erasing_array = surfarray.array3d(alpha_surface)

    surface_alpha = array(full_surface.get_view("A"), copy=False)
    surface_alpha[:, :] = erasing_array[:, :, 0]

    # Unload the alpha channel
    del surface_alpha

    surface.blit(
        full_surface, (x - radius - half_thickness, y - radius - half_thickness)
    )


# TODO add ellipse drawing
def ellipse(
    x,
    y,
    width,
    height,
    offset=None,
    scale=None,
    fill_color=None,
    stroke_color=None,
    fill=None,
    stroke_width=None,
    surface=None,
):
    raise NotImplementedError(
        "Drawing ellipses is not yet implemented. Did you try to stretch a circle?"
    )


def rect(
    x,
    y,
    width,
    height,
    offset=None,
    scale=None,
    fill_color=None,
    stroke_color=None,
    fill=None,
    stroke_width=None,
    surface=None,
):
    """
    Draws a rectangle
    """

    # Get defaults
    if offset is None:
        offset = Draw.offset
    if scale is None:
        scale = Draw.scale
    if fill_color is None:
        fill_color = Draw.fill_color
    if stroke_color is None:
        stroke_color = Draw.stroke_color
    if fill is None:
        fill = Draw.fill
    if stroke_width is None:
        stroke_width = Draw.stroke_width
    if surface is None:
        surface = Draw.surface
    if surface is None:
        surface = display.get_surface()

    # Round values to integers
    x = round(x)
    y = round(y)
    width = round(width)
    height = round(height)

    # Scale and offset
    x, y = (x * scale.x + offset.x, y * scale.y + offset.y)
    width *= scale.x
    height *= scale.y

    # Draw
    if fill:
        gfxdraw.box(surface, Rect(x, y, width, height), fill_color)
    if stroke_width == 1:
        gfxdraw.rectangle(surface, Rect(x, y, width, height), stroke_color)
    elif stroke_width > 1:
        # Draw four rectangles to draw the outline
        half_stroke_width = int(stroke_width / 2)
        gfxdraw.box(
            surface,
            Rect(
                x - half_stroke_width,
                y - half_stroke_width,
                width + stroke_width,
                stroke_width,
            ),
            stroke_color,
        )
        gfxdraw.box(
            surface,
            Rect(
                x - half_stroke_width,
                y - half_stroke_width,
                stroke_width,
                height + stroke_width,
            ),
            stroke_color,
        )
        gfxdraw.box(
            surface,
            Rect(
                x - half_stroke_width,
                y + height - half_stroke_width,
                width + stroke_width,
                stroke_width,
            ),
            stroke_color,
        )
        gfxdraw.box(
            surface,
            Rect(
                x + width - half_stroke_width,
                y - half_stroke_width,
                stroke_width,
                height + stroke_width,
            ),
            stroke_color,
        )