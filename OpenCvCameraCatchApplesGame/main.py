from drawBoxF import drawBox
import pygame
import cv2    as     cv
import os
import json
import random
from   PIL    import Image as PilImage
from pygame.constants import SCRAP_SELECTION, WINDOWHITTEST

# Importing created functions;
from changeResF                               import changeResF
from dropFruitsByDropSpeedF                   import dropFruitsByDropSpeedF
from runAllFruitscheckIfObstacleHasFallenF    import runAllFruitscheckIfObstacleHasFallenF
from runAllFruitsobstacleHasBeenTouchedF      import runAllFruitsobstacleHasBeenTouchedF
from getMousePositionAndReturnAsDictionaryXYF import getMousePositionAndReturnAsDictionaryXYF


# Importing error functions;
from errorsToCall import cameraIsInvalidF

# Import classes;
from ToCatchFruitObject import ToCatchFruitObject




# Initialising pygame and related stuff;
pygame.init()
pygame.font.init()
pygame.mixer.init()



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~;
# Colors;
RED    = [255, 0, 0]
GREEN  = [0, 255, 0]
BLUE   = [0, 0, 255]
YELLOW = [255 ,255 ,0]
ORANGE = [255, 165, 0]
WHITE  = [255, 255, 255]
BLACK  = [0, 0, 0]










# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~;
# GLOBAL APP DATA;
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~;

# Importing app settings;
with open("./Data/Settings/settings.json") as jsonSettingsUnReaded:
    JSONAPPDATA               = json.load(jsonSettingsUnReaded)
    JSONWIDGETSETTINGS        = JSONAPPDATA["GameWidgetSettings"]
    GAMELOGICSETTINGS         = JSONAPPDATA["GameLogicSettings"]
    PLAYEREHADBBOXCOORDINATES = JSONAPPDATA["GameTrackingSettings"]["playerHeadBboxCoordinates"]

# Widget data;
WIDGETTITLE = JSONWIDGETSETTINGS["WIDGETTITLE"]
WIDTH       = JSONWIDGETSETTINGS["WIDTH"]
HEIGHT      = JSONWIDGETSETTINGS["HEIGHT"]


# Game general data;
MAXFPS = JSONWIDGETSETTINGS["MAXFPS"]


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~;
# Display object settings;
DEFAULINFOTEXTFONT = pygame.font.SysFont("Comic Sans Ms", 30)
PLAYERINFOTEXTFONT = pygame.font.SysFont("Comic Sans Ms", 50)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~;
# Tracking data;
# Players BBOX coordinates;
playerBboxToTakeCoordinates = {
                               "x1": ((JSONWIDGETSETTINGS["WIDTH"] // 2)  - (PLAYEREHADBBOXCOORDINATES["w"] // 2)),
                               "y1": ((JSONWIDGETSETTINGS["HEIGHT"] // 2) - (PLAYEREHADBBOXCOORDINATES["h"] // 2)), 
                               "x2": ((JSONWIDGETSETTINGS["WIDTH"] // 2)  + (PLAYEREHADBBOXCOORDINATES["w"] // 2)),
                               "y2": ((JSONWIDGETSETTINGS["HEIGHT"] // 2) + (PLAYEREHADBBOXCOORDINATES["h"] // 2))}



class MainApp():
    def __init__(self):
        # In the init function, just initialising the basic game variables/values/data;

        # Game state keepers;
        self.gameIsRunning                   = True # The state of game running or not; Can be used for game pauses;
        self.gameMaxFruitsCount              = GAMELOGICSETTINGS["gameMaxFruitsCount"] # The maxium amount of fruits that can be displayed on the screen;
        self.allGameToCatchFruitObjectsArray = []   # The array holding the game fruit objects, the objects are initialised in a different function;
        self.playerHeartsCount               = GAMELOGICSETTINGS["playerHeartsCount"] # The player hearts state keeper;
        self.playerPointsCount               = 0    # Player points state keeper;


        

        # Creating the camera capture;
        try:
            self.cameraCapture = cv.VideoCapture(0)
            # Setting the capture dimensions to 1280x720;
            changeResF(WIDTH, HEIGHT, self.cameraCapture)
        except:
            cameraIsInvalidF()


        # Creating the fps cap;
        self.gameClock = pygame.time.Clock()
            
        # App window;
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))

        # First, making sure the players head is centered;
        self.makeSurePlayersHeadIsInTheCenterF()
        
        # Now, creating the tracker;
        self.initialiseTrackerF()


        # Initialising the fruits;
        self.initialiseFruitsF()



        # Widget settings;
        pygame.display.set_caption(WIDGETTITLE)


    
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~;
        # The init function is just for basic data initialisations,
        # The actual game starts in the self.mainGameLoopFunction;
        self.mainGameLoopFunction()








    def mainGameLoopFunction(self):
        
        # Starting the game loop;
        while self.gameIsRunning:

            # Updating the game clock numbers/data;
            self.gameClock.tick(MAXFPS)


            # Looping through all the events detected by pygame;
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                
                # Actual inputs;






            # First of all, setting the camera capture to an app state property to be able to access the *CURRENT* frame throughout the whole app;
            # The fps is capped to 60fps so at max the video will also be 60fps (given the camera supports 60fps);
            # If the cameraFrame isn't valid, giving the invalid camera error;
            cameraFrameIsValid, self.currentCameraFrameUnFlipped = self.cameraCapture.read()
            if cameraFrameIsValid:
                # Camera captured frame is valid;
                # The rest of the code is written here  as we don't want it to be run if the camera doesnt work properly;

                # Flipping the camera frame horizontally;
                self.currentCameraFrame = cv.flip(self.currentCameraFrameUnFlipped, 1)

                # Setting the player head/hand bounding box on the frame;
                trackerUpdateReturnSuccessState, trackerUpdateReturnBoundingBox = self.playerTracker.update(self.currentCameraFrame)
                if trackerUpdateReturnSuccessState:
                    #print(trackerUpdateReturnBoundingBox)
                    drawBox(self.currentCameraFrame, trackerUpdateReturnBoundingBox)
                else:
                    cv.putText(self.currentCameraFrame, "Lost", (75, 75), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)


                # Checking if fruits are all in a valid height;
                runAllFruitscheckIfObstacleHasFallenF(self=self, screenWidth=WIDTH, screenHeight=HEIGHT)

                # Checking if theres any player collision with the fruits;
                runAllFruitsobstacleHasBeenTouchedF(self=self,
                                                    playerCoordinates = getMousePositionAndReturnAsDictionaryXYF(pygame.mouse.get_pos()),
                                                    screenWidth       = WIDTH)

                # Dropping the fruits by the drop speed;
                dropFruitsByDropSpeedF(self.allGameToCatchFruitObjectsArray, GAMELOGICSETTINGS["gameObjectDropSpeed"])
                
                # Calling the self.reRenderScreenF;
                self.reRenderScreenF()
            else:
                cameraIsInvalidF()
            

    
    # The reRenderScreenF,
    # It will be called at the end of each mainGameLoop iteration;
    # First, it will take an image from the camera and set it as the background
    def reRenderScreenF(self):
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~;
        # Rendering the camera video to the pygame window;

        # Now the actual frame is rendered;
        # Firstly, changing the opencv captured frame to a pil image;
        toPillFirstStepColorConversion = cv.cvtColor(self.currentCameraFrame, cv.COLOR_BGR2RGBA)
        # Creating the pill image by changing the image binaries to the pill "style/way";
        pilImage              = PilImage.fromarray(toPillFirstStepColorConversion)
        # Creating a raw image string from the pil image to be able to display it in pygame;
        rawPilImageString = pilImage.tobytes("raw", "RGBA")

        # Loading the rawPilImageString as a pygame image;
        toRenderInPygameCameraFrame = pygame.transform.scale(pygame.image.fromstring(rawPilImageString, (self.currentCameraFrame.shape[1], self.currentCameraFrame.shape[0]), "RGBA"), (WIDTH, HEIGHT))
        # Displaying the loaded image;
        self.WIN.blit(toRenderInPygameCameraFrame, (0, 0))



        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~;
        # More "Overlay" type stuff displayed below;

        # Displaying the fruits;
        for fruitObjectToDisplay in self.allGameToCatchFruitObjectsArray:
            self.WIN.blit(fruitObjectToDisplay.imageObstacleObject, (fruitObjectToDisplay.x, fruitObjectToDisplay.y))
        
        # Displaying the current FPS;
        fpsText = DEFAULINFOTEXTFONT.render(f"FPS: [{str(int(self.gameClock.get_fps()))}]", False, RED)
        self.WIN.blit(fpsText, (10, 10))

        # Displaying the current player points;
        playerPointsText = PLAYERINFOTEXTFONT.render(f"P: {str(self.playerPointsCount)}", False, GREEN)
        self.WIN.blit(playerPointsText, (10, 40))

        # Displaying the current player hearts;
        playerHeartsText = PLAYERINFOTEXTFONT.render(f"H: {str(self.playerHeartsCount)}", False, GREEN)
        self.WIN.blit(playerHeartsText, (10, 90))

        # Updating the screen;
        pygame.display.update()



    # The function for initialising the fruits, its called before the mainGameLoop starts;
    # Its called only once throughout the whole runtime;
    def initialiseFruitsF(self):
        # Firstly, finding all the files in the ./Data/Images/Fruits/ directory,
        # Then putting them in an array, getting the length of the array and generating random numbers between (0 and fruitimagesArray.length-1);
        # Using those numbers as indexes for the fruitImagesArray values, that way being able to give a random fruit to each fruit object;
        fruitimagesArray = os.listdir("./Data/Images/Fruits")
        
        # Adding the fruits to the fruitsImagesArray;
        for i in range(self.gameMaxFruitsCount):
            # Creating the random coordinates of the image to sent it as coordinate properties;
            # Horizontal location is random;
            objectX      = random.randint(0, (WIDTH - GAMELOGICSETTINGS["gameFruitObjectSize"]["width"]))
            objectY      = (0 - GAMELOGICSETTINGS["gameFruitObjectSize"]["height"])
            objectWidth  = GAMELOGICSETTINGS["gameFruitObjectSize"]["width"]
            objectHeight = GAMELOGICSETTINGS["gameFruitObjectSize"]["height"]

            self.allGameToCatchFruitObjectsArray.append(ToCatchFruitObject(
                imageObstacleObject = pygame.transform.scale(
                    pygame.image.load(f"./Data/Images/Fruits/{str(fruitimagesArray[random.randint(0, len(fruitimagesArray)-1)])}"),
                (objectWidth, objectHeight)),
                x      = objectX,
                y      = objectY,
                width  = objectWidth,
                height = objectHeight
            ))


    # This function creates a cv2 window, puts a rectangle in the center,
    # Asks the player to put their head in it and start, then the window closes,
    # rectangles inside/data info is sent to the tracker and the player head tracking is started;
    def makeSurePlayersHeadIsInTheCenterF(self):
        while True:
            captureIsSuccessfull, singleFrameToShowUnReady = self.cameraCapture.read()
            singleFrameToShow = cv.flip(cv.resize(singleFrameToShowUnReady, (WIDTH, HEIGHT)), 1)
            
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~;
            # Firstlu, drawing the basic info on the map;
            # (User BBox rect specifying which area will be sent as data to the tracker and some user information text);
            
            # Bbox area rect;
            cv.rectangle(singleFrameToShow, (playerBboxToTakeCoordinates["x1"], playerBboxToTakeCoordinates["y1"]),
                                            (playerBboxToTakeCoordinates["x2"], playerBboxToTakeCoordinates["y2"]), BLUE, 3)

            # Giving the user the "click q when your head is centered" text info;
            cv.putText(singleFrameToShow, "Press 'Q' once your head/hand is", 
                       (60, 75), cv.FONT_HERSHEY_COMPLEX, 2, RED, 5)
            cv.putText(singleFrameToShow, "completely within the center", 
                       (120, 135), cv.FONT_HERSHEY_COMPLEX, 2, RED, 5)
            cv.putText(singleFrameToShow, "red rectangle.", 
                       (400, 195), cv.FONT_HERSHEY_COMPLEX, 2, RED, 5)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~;

            
            
            
            # Displaying the user searching window;
            cv.imshow("usersearching", singleFrameToShow)
            
            
            if cv.waitKey(1) & 0xff == ord('q'):
                # Setting the bounding box;
                self.playerBoundingBox = (playerBboxToTakeCoordinates["x1"], playerBboxToTakeCoordinates["y1"], PLAYEREHADBBOXCOORDINATES["w"], PLAYEREHADBBOXCOORDINATES["h"])
                

                cv.destroyWindow("usersearching")
                break

    # The function for initialising the tracker;
    def initialiseTrackerF(self):
        self.playerTracker = cv.TrackerMOSSE_create()
        success, trackerInitialisationFrameUnFlipped = self.cameraCapture.read()
        trackerInitialisationFrame = cv.flip(trackerInitialisationFrameUnFlipped, 1)
        print(self.playerBoundingBox)
        self.playerTracker.init(trackerInitialisationFrame, self.playerBoundingBox)

        





# NOTE NOTE NOTE NOTE NOTE TODO TODO TODO TODO TODO WHAT THE FUCK WHAT THE FUCK WHAT THE FUCKING FUCKING FUCK FUCK TODO TODO NOTE NOTE NOTE FUCK.




        
        




if __name__ == "__main__":
    # First making sure we get the players hand coordinates, 
    # After we get the HEAD (YES, HEAD, NOT HAND.) position starting the game with MainApp and passing in the user hand coordinates in it;
    MainApp()


