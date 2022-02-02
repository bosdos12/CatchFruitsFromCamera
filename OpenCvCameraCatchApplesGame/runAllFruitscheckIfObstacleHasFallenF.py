# The function that goes through all the fruit objects and calls their checkIfObstacleHasFallen function;
def runAllFruitscheckIfObstacleHasFallenF(self, screenWidth, screenHeight):
    for fruitObject in self.allGameToCatchFruitObjectsArray:
        if fruitObject.checkIfObstacleHasFallen(screenWidth, screenHeight):
            self.playerHeartsCount -= 1
