import random


class ToCatchFruitObject:
    def __init__(self, imageObstacleObject, x, y, width, height):
        self.imageObstacleObject   = imageObstacleObject
        self.x                     = x
        self.y                     = y
        self.width                 = width
        self.height                = height
        # Taking coordinates as properties as an image object cannot have coordinates

        



    # This function receives the player coordinates and runs a collision detection with the fruit obstacle;
    # If there is no collision detection, nothing happens,
    # Otherwise, The current player gets +1 points in the runAllFruitsObstacleHasBeenTouchedF if a true is returned,
    # and the obstacle is placed above the screen to start falling again;
    def obstacleHasBeenTouchedF(self, playerCoordinates, screenWidth):
        # Horizontal;
        if (playerCoordinates["x"] >= self.x and playerCoordinates["x"] <= (self.x + self.width)):
            if (playerCoordinates["y"] >= self.y and playerCoordinates["y"] <= (self.y + self.height)):
                # Colision detected;
                
                # Respawning the fruit object
                self.reSpawnFruitObjectF(screenWidth)

                # Returning True;
                return True




    # The function to check if the obstacle is "below" the screen;
    # If it is, the obstacle gets put back to the starting point vertically and a random point horizontally,
    # Then the player looses one heart in the runAllFruitscheckIfObstacleHasFallenF if a true is returned;
    def checkIfObstacleHasFallen(self, screenWidth, screenHeight):
        if self.y >= screenHeight:
            # The object has completely fallen,

            # Respawning the fruit object
            self.reSpawnFruitObjectF(screenWidth)
            
            # Returning True;
            return True


    # The function for setting the location of the fruit object back to start, at (0 - self.height) height and a random horizontal position
    def reSpawnFruitObjectF(self, screenWidth):
        self.x = random.randint(0, (screenWidth - self.width))
        self.y = (0 - self.height)
            
        

