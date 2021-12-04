class MapSizeError(Exception):
    def __init__(self, width: int, height: int) -> None:
        msg = "Field of the map cannot be less than 2."
        msg += f"Your field is {width}x{height}={width*height}"
        super().__init__(msg)

