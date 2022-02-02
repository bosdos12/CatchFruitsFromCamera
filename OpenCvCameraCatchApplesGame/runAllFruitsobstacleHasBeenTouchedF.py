# This function takes the players coordinates, loops through each fruit object,
# Calls their "obstacleHasBeenTouchedF" and gives it the props from its own props;
# The only reason this is in another function is to make the code look cleaner (same as "runAllFruitsCheckIfObstacleHasFallenF");
def runAllFruitsobstacleHasBeenTouchedF(self, playerCoordinates, screenWidth):
    for fruitObject in self.allGameToCatchFruitObjectsArray:
        if fruitObject.obstacleHasBeenTouchedF(playerCoordinates, screenWidth):
            self.playerPointsCount += 1
        

