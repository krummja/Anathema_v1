from __future__ import annotations
import numpy as np
import tcod.noise
from tcod._internal import (
    _CDataWrapper
)
from tcod.loader import ffi, lib


def _heightmap_cdata(array: np.ndarray) -> ffi.CData:
    """Return a new TCOD_heightmap_t instance using an array.
    Formatting is verified during this function.
    """
    if array.flags["F_CONTIGUOUS"]:
        array = array.transpose()
    if not array.flags["C_CONTIGUOUS"]:
        raise ValueError("array must be a contiguous segment.")
    if array.dtype != np.float32:
        raise ValueError("array dtype must be float32, not %r" % array.dtype)
    height, width = array.shape
    pointer = ffi.from_buffer("float *", array)
    return ffi.new("TCOD_heightmap_t *", (width, height, pointer))


def heightmap_new(w: int, h: int, order: str = "C") -> np.ndarray:
    """Return a new numpy.ndarray formatted for use with heightmap functions.
    `w` and `h` are the width and height of the array.
    `order` is given to the new NumPy array, it can be 'C' or 'F'.
    You can pass a NumPy array to any heightmap function as long as all the
    following are true::
    * The array is 2 dimensional.
    * The array has the C_CONTIGUOUS or F_CONTIGUOUS flag.
    * The array's dtype is `dtype.float32`.
    The returned NumPy array will fit all these conditions.
    .. versionchanged:: 8.1
        Added the `order` parameter.
    """
    if order == "C":
        return np.zeros((h, w), np.float32, order="C")
    elif order == "F":
        return np.zeros((w, h), np.float32, order="F")
    else:
        raise ValueError("Invalid order parameter, should be 'C' or 'F'.")


def heightmap_set_value(hm: np.ndarray, x: int, y: int, value: float) -> None:
    """Set the value of a point on a heightmap.
    .. deprecated:: 2.0
        `hm` is a NumPy array, so values should be assigned to it directly.
    """
    if hm.flags["C_CONTIGUOUS"]:
        hm[y, x] = value
    elif hm.flags["F_CONTIGUOUS"]:
        hm[x, y] = value
    else:
        raise ValueError("This array is not contiguous.")


def heightmap_add(hm: np.ndarray, value: float) -> None:
    """Add value to all values on this heightmap.
    Args:
        hm (numpy.ndarray): A numpy.ndarray formatted for heightmap functions.
        value (float): A number to add to this heightmap.
    .. deprecated:: 2.0
        Do ``hm[:] += value`` instead.
    """
    hm[:] += value


def heightmap_scale(hm: np.ndarray, value: float) -> None:
    """Multiply all items on this heightmap by value.
    Args:
        hm (numpy.ndarray): A numpy.ndarray formatted for heightmap functions.
        value (float): A number to scale this heightmap by.
    .. deprecated:: 2.0
        Do ``hm[:] *= value`` instead.
    """
    hm[:] *= value


def heightmap_clear(hm: np.ndarray) -> None:
    """Add value to all values on this heightmap.
    Args:
        hm (numpy.ndarray): A numpy.ndarray formatted for heightmap functions.
    .. deprecated:: 2.0
        Do ``hm.array[:] = 0`` instead.
    """
    hm[:] = 0


def heightmap_clamp(hm: np.ndarray, mi: float, ma: float) -> None:
    """Clamp all values on this heightmap between ``mi`` and ``ma``
    Args:
        hm (numpy.ndarray): A numpy.ndarray formatted for heightmap functions.
        mi (float): The lower bound to clamp to.
        ma (float): The upper bound to clamp to.
    .. deprecated:: 2.0
        Do ``hm.clip(mi, ma)`` instead.
    """
    hm.clip(mi, ma)


def heightmap_copy(hm1: np.ndarray, hm2: np.ndarray) -> None:
    """Copy the heightmap ``hm1`` to ``hm2``.
    Args:
        hm1 (numpy.ndarray): The source heightmap.
        hm2 (numpy.ndarray): The destination heightmap.
    .. deprecated:: 2.0
        Do ``hm2[:] = hm1[:]`` instead.
    """
    hm2[:] = hm1[:]


def heightmap_normalize(
    hm: np.ndarray, mi: float = 0.0, ma: float = 1.0
) -> None:
    """Normalize heightmap values between ``mi`` and ``ma``.
    Args:
        hm (numpy.ndarray): A numpy.ndarray formatted for heightmap functions.
        mi (float): The lowest value after normalization.
        ma (float): The highest value after normalization.
    """
    lib.TCOD_heightmap_normalize(_heightmap_cdata(hm), mi, ma)


def heightmap_lerp_hm(
    hm1: np.ndarray, hm2: np.ndarray, hm3: np.ndarray, coef: float
) -> None:
    """Perform linear interpolation between two heightmaps storing the result
    in ``hm3``.
    This is the same as doing ``hm3[:] = hm1[:] + (hm2[:] - hm1[:]) * coef``
    Args:
        hm1 (numpy.ndarray): The first heightmap.
        hm2 (numpy.ndarray): The second heightmap to add to the first.
        hm3 (numpy.ndarray): A destination heightmap to store the result.
        coef (float): The linear interpolation coefficient.
    """
    lib.TCOD_heightmap_lerp_hm(
        _heightmap_cdata(hm1),
        _heightmap_cdata(hm2),
        _heightmap_cdata(hm3),
        coef,
    )


def heightmap_add_hm(
    hm1: np.ndarray, hm2: np.ndarray, hm3: np.ndarray
) -> None:
    """Add two heightmaps together and stores the result in ``hm3``.
    Args:
        hm1 (numpy.ndarray): The first heightmap.
        hm2 (numpy.ndarray): The second heightmap to add to the first.
        hm3 (numpy.ndarray): A destination heightmap to store the result.
    .. deprecated:: 2.0
        Do ``hm3[:] = hm1[:] + hm2[:]`` instead.
    """
    hm3[:] = hm1[:] + hm2[:]


def heightmap_multiply_hm(
    hm1: np.ndarray, hm2: np.ndarray, hm3: np.ndarray
) -> None:
    """Multiplies two heightmap's together and stores the result in ``hm3``.
    Args:
        hm1 (numpy.ndarray): The first heightmap.
        hm2 (numpy.ndarray): The second heightmap to multiply with the first.
        hm3 (numpy.ndarray): A destination heightmap to store the result.
    .. deprecated:: 2.0
        Do ``hm3[:] = hm1[:] * hm2[:]`` instead.
        Alternatively you can do ``HeightMap(hm1.array[:] * hm2.array[:])``.
    """
    hm3[:] = hm1[:] * hm2[:]


def heightmap_add_hill(
    hm: np.ndarray, x: float, y: float, radius: float, height: float
) -> None:
    """Add a hill (a half spheroid) at given position.
    If height == radius or -radius, the hill is a half-sphere.
    Args:
        hm (numpy.ndarray): A numpy.ndarray formatted for heightmap functions.
        x (float): The x position at the center of the new hill.
        y (float): The y position at the center of the new hill.
        radius (float): The size of the new hill.
        height (float): The height or depth of the new hill.
    """
    lib.TCOD_heightmap_add_hill(_heightmap_cdata(hm), x, y, radius, height)


def heightmap_dig_hill(
    hm: np.ndarray, x: float, y: float, radius: float, height: float
) -> None:
    """
    This function takes the highest value (if height > 0) or the lowest
    (if height < 0) between the map and the hill.
    It's main goal is to carve things in maps (like rivers) by digging hills
    along a curve.
    Args:
        hm (numpy.ndarray): A numpy.ndarray formatted for heightmap functions.
        x (float): The x position at the center of the new carving.
        y (float): The y position at the center of the new carving.
        radius (float): The size of the carving.
        height (float): The height or depth of the hill to dig out.
    """
    lib.TCOD_heightmap_dig_hill(_heightmap_cdata(hm), x, y, radius, height)


def heightmap_rain_erosion(
    hm: np.ndarray,
    nbDrops: int,
    erosionCoef: float,
    sedimentationCoef: float,
    rnd: Optional[tcod.random.Random] = None,
) -> None:
    """Simulate the effect of rain drops on the terrain, resulting in erosion.
    ``nbDrops`` should be at least hm.size.
    Args:
        hm (numpy.ndarray): A numpy.ndarray formatted for heightmap functions.
        nbDrops (int): Number of rain drops to simulate.
        erosionCoef (float): Amount of ground eroded on the drop's path.
        sedimentationCoef (float): Amount of ground deposited when the drops
                                   stops to flow.
        rnd (Optional[Random]): A tcod.Random instance, or None.
    """
    lib.TCOD_heightmap_rain_erosion(
        _heightmap_cdata(hm),
        nbDrops,
        erosionCoef,
        sedimentationCoef,
        rnd.random_c if rnd else ffi.NULL,
    )


def heightmap_kernel_transform(
    hm: np.ndarray,
    kernelsize: int,
    dx: Sequence[int],
    dy: Sequence[int],
    weight: Sequence[float],
    minLevel: float,
    maxLevel: float,
) -> None:
    """Apply a generic transformation on the map, so that each resulting cell
    value is the weighted sum of several neighbour cells.
    This can be used to smooth/sharpen the map.
    Args:
        hm (numpy.ndarray): A numpy.ndarray formatted for heightmap functions.
        kernelsize (int): Should be set to the length of the parameters::
                          dx, dy, and weight.
        dx (Sequence[int]): A sequence of x coorinates.
        dy (Sequence[int]): A sequence of y coorinates.
        weight (Sequence[float]): A sequence of kernelSize cells weight.
                                  The value of each neighbour cell is scaled by
                                  its corresponding weight
        minLevel (float): No transformation will apply to cells
                          below this value.
        maxLevel (float): No transformation will apply to cells
                          above this value.
    See examples below for a simple horizontal smoothing kernel :
    replace value(x,y) with
    0.33*value(x-1,y) + 0.33*value(x,y) + 0.33*value(x+1,y).
    To do this, you need a kernel of size 3
    (the sum involves 3 surrounding cells).
    The dx,dy array will contain:
    * dx=-1, dy=0 for cell (x-1, y)
    * dx=1, dy=0 for cell (x+1, y)
    * dx=0, dy=0 for cell (x, y)
    * The weight array will contain 0.33 for each cell.
    Example:
        >>> import numpy as np
        >>> heightmap = np.zeros((3, 3), dtype=np.float32)
        >>> heightmap[:,1] = 1
        >>> dx = [-1, 1, 0]
        >>> dy = [0, 0, 0]
        >>> weight = [0.33, 0.33, 0.33]
        >>> tcod.heightmap_kernel_transform(heightmap, 3, dx, dy, weight,
        ...                                 0.0, 1.0)
    """
    cdx = ffi.new("int[]", dx)
    cdy = ffi.new("int[]", dy)
    cweight = ffi.new("float[]", weight)
    lib.TCOD_heightmap_kernel_transform(
        _heightmap_cdata(hm), kernelsize, cdx, cdy, cweight, minLevel, maxLevel
    )


def heightmap_add_voronoi(
    hm: np.ndarray,
    nbCoef: int,
    coef: Sequence[float],
    rnd: Optional[tcod.random.Random] = None,
) -> None:
    """Add values from a Voronoi diagram to the heightmap.
    Args:
        hm (numpy.ndarray): A numpy.ndarray formatted for heightmap functions.
        nbCoef (int): The diagram value is calculated from the nbCoef
                      closest sites.
        coef (Sequence[float]): The distance to each site is scaled by the
                                corresponding coef.
                                Closest site : coef[0],
                                second closest site : coef[1], ...
        rnd (Optional[Random]): A Random instance, or None.
    """
    nbPoints = len(coef)
    ccoef = ffi.new("float[]", coef)
    lib.TCOD_heightmap_add_voronoi(
        _heightmap_cdata(hm),
        nbPoints,
        nbCoef,
        ccoef,
        rnd.random_c if rnd else ffi.NULL,
    )


def heightmap_add_fbm(
    hm: np.ndarray,
    noise: tcod.noise.Noise,
    mulx: float,
    muly: float,
    addx: float,
    addy: float,
    octaves: float,
    delta: float,
    scale: float,
) -> None:
    """Add FBM noise to the heightmap.
    The noise coordinate for each map cell is
    `((x + addx) * mulx / width, (y + addy) * muly / height)`.
    The value added to the heightmap is `delta + noise * scale`.
    Args:
        hm (numpy.ndarray): A numpy.ndarray formatted for heightmap functions.
        noise (Noise): A Noise instance.
        mulx (float): Scaling of each x coordinate.
        muly (float): Scaling of each y coordinate.
        addx (float): Translation of each x coordinate.
        addy (float): Translation of each y coordinate.
        octaves (float): Number of octaves in the FBM sum.
        delta (float): The value added to all heightmap cells.
        scale (float): The noise value is scaled with this parameter.
    .. deprecated:: 8.1
        An equivalent array of noise samples can be taken using a method such
        as :any:`Noise.sample_ogrid`.
    """
    noise = noise.noise_c if noise is not None else ffi.NULL
    lib.TCOD_heightmap_add_fbm(
        _heightmap_cdata(hm),
        noise,
        mulx,
        muly,
        addx,
        addy,
        octaves,
        delta,
        scale,
    )


def heightmap_scale_fbm(
    hm: np.ndarray,
    noise: tcod.noise.Noise,
    mulx: float,
    muly: float,
    addx: float,
    addy: float,
    octaves: float,
    delta: float,
    scale: float,
) -> None:
    """Multiply the heightmap values with FBM noise.
    Args:
        hm (numpy.ndarray): A numpy.ndarray formatted for heightmap functions.
        noise (Noise): A Noise instance.
        mulx (float): Scaling of each x coordinate.
        muly (float): Scaling of each y coordinate.
        addx (float): Translation of each x coordinate.
        addy (float): Translation of each y coordinate.
        octaves (float): Number of octaves in the FBM sum.
        delta (float): The value added to all heightmap cells.
        scale (float): The noise value is scaled with this parameter.
    .. deprecated:: 8.1
        An equivalent array of noise samples can be taken using a method such
        as :any:`Noise.sample_ogrid`.
    """
    noise = noise.noise_c if noise is not None else ffi.NULL
    lib.TCOD_heightmap_scale_fbm(
        _heightmap_cdata(hm),
        noise,
        mulx,
        muly,
        addx,
        addy,
        octaves,
        delta,
        scale,
    )


def heightmap_dig_bezier(
    hm: np.ndarray,
    px: Tuple[int, int, int, int],
    py: Tuple[int, int, int, int],
    startRadius: float,
    startDepth: float,
    endRadius: float,
    endDepth: float,
) -> None:
    """Carve a path along a cubic Bezier curve.
    Both radius and depth can vary linearly along the path.
    Args:
        hm (numpy.ndarray): A numpy.ndarray formatted for heightmap functions.
        px (Sequence[int]): The 4 `x` coordinates of the Bezier curve.
        py (Sequence[int]): The 4 `y` coordinates of the Bezier curve.
        startRadius (float): The starting radius size.
        startDepth (float): The starting depth.
        endRadius (float): The ending radius size.
        endDepth (float): The ending depth.
    """
    lib.TCOD_heightmap_dig_bezier(
        _heightmap_cdata(hm),
        px,
        py,
        startRadius,
        startDepth,
        endRadius,
        endDepth,
    )


def heightmap_get_value(hm: np.ndarray, x: int, y: int) -> float:
    """Return the value at ``x``, ``y`` in a heightmap.
    .. deprecated:: 2.0
        Access `hm` as a NumPy array instead.
    """
    if hm.flags["C_CONTIGUOUS"]:
        return hm[y, x]  # type: ignore
    elif hm.flags["F_CONTIGUOUS"]:
        return hm[x, y]  # type: ignore
    else:
        raise ValueError("This array is not contiguous.")


def heightmap_get_interpolated_value(
    hm: np.ndarray, x: float, y: float
) -> float:
    """Return the interpolated height at non integer coordinates.
    Args:
        hm (numpy.ndarray): A numpy.ndarray formatted for heightmap functions.
        x (float): A floating point x coordinate.
        y (float): A floating point y coordinate.
    Returns:
        float: The value at ``x``, ``y``.
    """
    return float(
        lib.TCOD_heightmap_get_interpolated_value(_heightmap_cdata(hm), x, y)
    )


def heightmap_get_slope(hm: np.ndarray, x: int, y: int) -> float:
    """Return the slope between 0 and (pi / 2) at given coordinates.
    Args:
        hm (numpy.ndarray): A numpy.ndarray formatted for heightmap functions.
        x (int): The x coordinate.
        y (int): The y coordinate.
    Returns:
        float: The steepness at ``x``, ``y``.  From 0 to (pi / 2)
    """
    return float(lib.TCOD_heightmap_get_slope(_heightmap_cdata(hm), x, y))


def heightmap_get_normal(
    hm: np.ndarray, x: float, y: float, waterLevel: float
) -> Tuple[float, float, float]:
    """Return the map normal at given coordinates.
    Args:
        hm (numpy.ndarray): A numpy.ndarray formatted for heightmap functions.
        x (float): The x coordinate.
        y (float): The y coordinate.
        waterLevel (float): The heightmap is considered flat below this value.
    Returns:
        Tuple[float, float, float]: An (x, y, z) vector normal.
    """
    cn = ffi.new("float[3]")
    lib.TCOD_heightmap_get_normal(_heightmap_cdata(hm), x, y, cn, waterLevel)
    return tuple(cn)  # type: ignore


def heightmap_count_cells(hm: np.ndarray, mi: float, ma: float) -> int:
    """Return the number of map cells which value is between ``mi`` and ``ma``.
    Args:
        hm (numpy.ndarray): A numpy.ndarray formatted for heightmap functions.
        mi (float): The lower bound.
        ma (float): The upper bound.
    Returns:
        int: The count of values which fall between ``mi`` and ``ma``.
    .. deprecated:: 8.1
        Can be replaced by an equivalent NumPy function such as:
        ``numpy.count_nonzero((mi <= hm) & (hm < ma))``
    """
    return int(lib.TCOD_heightmap_count_cells(_heightmap_cdata(hm), mi, ma))


def heightmap_has_land_on_border(hm: np.ndarray, waterlevel: float) -> bool:
    """Returns True if the map edges are below ``waterlevel``, otherwise False.
    Args:
        hm (numpy.ndarray): A numpy.ndarray formatted for heightmap functions.
        waterlevel (float): The water level to use.
    Returns:
        bool: True if the map edges are below ``waterlevel``, otherwise False.
    """
    return bool(
        lib.TCOD_heightmap_has_land_on_border(_heightmap_cdata(hm), waterlevel)
    )


def heightmap_get_minmax(hm: np.ndarray) -> Tuple[float, float]:
    """Return the min and max values of this heightmap.
    Args:
        hm (numpy.ndarray): A numpy.ndarray formatted for heightmap functions.
    Returns:
        Tuple[float, float]: The (min, max) values.
    .. deprecated:: 2.0
        Use ``hm.min()`` or ``hm.max()`` instead.
    """
    mi = ffi.new("float *")
    ma = ffi.new("float *")
    lib.TCOD_heightmap_get_minmax(_heightmap_cdata(hm), mi, ma)
    return mi[0], ma[0]

