class HsvFilter:
    """
    A custom data structure to hold the state of an HSV filter.

    HSV stands for Hue, Saturation, and Value, which are the three components 
    that make up the HSV color model. The HSV color model is a way of 
    representing colors in terms of these three components, rather than 
    the Red-Green-Blue (RGB) color model that is commonly used.

    In computer vision and image processing, an HSV filter is a type of filter 
    that is applied to an image to isolate or extract certain colors based on 
    their hue, saturation, and value.
    
    An HsvFilter class, as shown in the code example you provided earlier, is 
    a custom data structure that holds the state of an HSV filter, including 
    the minimum and maximum values for each of the three components, as well 
    as values to add or subtract from saturation and value. The HsvFilter 
    class allows users to easily manipulate and store the configuration 
    settings for an HSV filter, which can be useful when performing 
    color-based operations on different images or when testing different 
    configurations to see which one works best.

    """

    def __init__(self, h_min: int = None, s_min: int = None, v_min: int = None,
                 h_max: int = None, s_max: int = None, v_max: int = None,
                 s_add: int = None, s_sub: int = None, v_add: int = None, v_sub: int = None):
        """
        Initializes the HsvFilter object with optional minimum and maximum HSV values
        and optional values to add or subtract from saturation and value.

        Args:
            h_min: Minimum hue value (0-180)
            s_min: Minimum saturation value (0-255)
            v_min: Minimum value value (0-255)
            h_max: Maximum hue value (0-180)
            s_max: Maximum saturation value (0-255)
            v_max: Maximum value value (0-255)
            s_add: Value to add to saturation
            s_sub: Value to subtract from saturation
            v_add: Value to add to value
            v_sub: Value to subtract from value
        """
        self.h_min = h_min
        self.s_min = s_min
        self.v_min = v_min
        self.h_max = h_max
        self.s_max = s_max
        self.v_max = v_max
        self.s_add = s_add
        self.s_sub = s_sub
        self.v_add = v_add
        self.v_sub = v_sub
