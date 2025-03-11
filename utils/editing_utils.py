import numpy as np

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

def limit_range(pos_a, distance):
    """
    Places pos_a along the line connecting to the origin, at the specified distance.

    Parameters:
    pos_a (tuple or numpy.ndarray): Tuple or array of (x, y, z) representing the position.
    distance (float): Distance from the origin where the position should be.

    Returns:
    tuple: New position (x, y, z) at the specified distance from origin along the same direction.
    """
    # Convert input to numpy array if it's not already for XY
    pos_a_np = np.array(pos_a, dtype=float)[:2]

    # Calculate the current distance from origin (norm of the vector)
    current_distance = np.linalg.norm(pos_a_np)

    # Return if already within limit
    if current_distance <= distance:
        return pos_a

    # Calculate the unit vector in the direction of pos_a
    unit_vector = pos_a_np / current_distance

    # Scale the unit vector by the desired distance
    new_pos = unit_vector * distance

    # Return modified XY
    return (new_pos[0], new_pos[1], pos_a[2])


def between(pos_a, pos_b, pos_c):
    new_pos_a = interpolate(pos_b, pos_c, factor=0.5)
    new_pos_a = (new_pos_a[0], new_pos_a[1], pos_a[2])
    return new_pos_a

def near(pos_a, pos_b, distance):
    """
    Generate a random position near pos_b within the specified distance,
    with operations only on the XY plane using NumPy.

    Args:
        pos_a: Tuple of (x, y, z) representing the position to take Z from
        pos_b: Tuple of (x, y, z) representing the position to stay near
        distance: Float representing the maximum distance from pos_b on the XY plane

    Returns:
        Tuple of (x, y, z) representing the new random position
    """
    # Extract coordinates
    x_b, y_b, _ = pos_b
    _, _, z_a = pos_a

    # Generate a random angle in radians (0 to 2π)
    random_angle = np.random.random() * 2 * np.pi

    # Calculate the new X and Y coordinates using polar coordinates
    x_new = x_b + distance * np.cos(random_angle)
    y_new = y_b + distance * np.sin(random_angle)

    # Return the new position with Z from pos_a
    return (float(x_new), float(y_new), z_a)


def calculate_2d_bbox_fit(obj_a_bbox, target_bbox):
    """
    Calculate the maximum/minimum coordinates where a smaller bbox can fit within a larger bbox.

    Parameters:
    obj_a_bbox: tuple of (min, max) coordinates, each as 3D numpy arrays
    target_bbox: tuple of (min, max) coordinates, each as 3D numpy arrays

    Returns:
    tuple: (min_coords, max_coords) where each is a 2D numpy array (X,Y only)
    """
    # Extract min/max from both bounding boxes
    obj_min, obj_max = obj_a_bbox
    target_min, target_max = target_bbox

    # Calculate object dimensions
    obj_size = obj_max - obj_min

    # Calculate valid min/max positions where object can fit
    # Min position: target_min
    # Max position: target_max - obj_dims_2d
    valid_min = target_min.copy()
    valid_max = target_max - obj_size

    return valid_min, valid_max
