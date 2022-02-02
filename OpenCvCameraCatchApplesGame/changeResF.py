# This function takes the live video capture and sets it to the desired resolution;
def changeResF(width, height, capture):
    # Live videos;
    capture.set(3, width)
    capture.set(4, height)