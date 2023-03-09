class EdgeFilter:
    """
    Custom data structure to hold the configuration settings for a Canny edge filter.
    """
    def __init__(self, kernel_size: int = None, erode_iterations: int = None, 
                 dilate_iterations: int = None, canny_threshold1: int = None, 
                 canny_threshold2: int = None):
        """
        Constructor method for the EdgeFilter class.
        
        :param kernel_size: The size of the kernel to use for morphological operations.
        :param erode_iterations: The number of times to apply the erosion operation to the image.
        :param dilate_iterations: The number of times to apply the dilation operation to the image.
        :param canny_threshold1: The lower threshold value for the Canny edge detection algorithm.
        :param canny_threshold2: The upper threshold value for the Canny edge detection algorithm.
        """
        self.kernel_size = kernel_size
        self.erode_iterations = erode_iterations
        self.dilate_iterations = dilate_iterations
        self.canny_threshold1 = canny_threshold1
        self.canny_threshold2 = canny_threshold2
