def interpolate(pos_a, pos_b, factor):
    """
    Interpolate between two 3D positions (x, y, z) based on a factor, but only for X and Y coordinates.

    Args:
        pos_a: Tuple of (x, y, z) representing the start position
        pos_b: Tuple of (x, y, z) representing the end position
        factor: Float between 0 and 1 representing the interpolation factor
                0 = completely at pos_a
                1 = completely at pos_b

    Returns:
        Tuple of (x, y, z) representing the interpolated position
    """
    # Clamp factor between 0 and 1 to ensure valid interpolation
    factor = max(0, min(1, factor))

    # Extract coordinates
    x_a, y_a, z_a = pos_a
    x_b, y_b, z_b = pos_b

    # Interpolate X and Y, keep Z from pos_a
    x_interpolated = x_a + (x_b - x_a) * factor
    y_interpolated = y_a + (y_b - y_a) * factor

    # Return the interpolated position with z from pos_a
    return (x_interpolated, y_interpolated, z_a)


def extrapolate(pos_a, pos_b, factor):
    """
    Extrapolate pos_a away from pos_b based on a factor, but only for X and Y coordinates.

    Args:
        pos_a: Tuple of (x, y, z) representing the position to extrapolate from
        pos_b: Tuple of (x, y, z) representing the reference position to move away from
        factor: Float representing the extrapolation factor
                1 = unchanged position (pos_a)
                2 = doubles the distance between pos_a and pos_b
                0 = pos_a is at pos_b
                negative values = move toward and past pos_b

    Returns:
        Tuple of (x, y, z) representing the extrapolated position
    """
    # Extract coordinates
    x_a, y_a, z_a = pos_a
    x_b, y_b, z_b = pos_b

    # Calculate the vector from pos_b to pos_a (the direction to extrapolate)
    vector_x = x_a - x_b
    vector_y = y_a - y_b

    # Extrapolate X and Y based on the factor
    # factor=1 means no change, factor=2 means double the distance
    x_extrapolated = x_b + vector_x * factor
    y_extrapolated = y_b + vector_y * factor

    # Keep the Z coordinate from pos_a
    return (x_extrapolated, y_extrapolated, z_a)

def between(pos_a, pos_b, pos_c):
    new_pos_a = interpolate(pos_b, pos_c, factor=0.5)
    new_pos_a = (new_pos_a[0], new_pos_a[1], pos_a[2])
    return new_pos_a