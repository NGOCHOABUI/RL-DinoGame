from Helpers import *
class Game_State:
    def __init__(self,agent,game):
        self._agent = agent
        self._game = game
        self._display = show_img() #display the processed image on screen using openCV, implemented using python coroutine 
        self._display.__next__() # initiliaze the display coroutine 
    def get_state(self,actions):
        actions_df.loc[len(actions_df)] = actions[1] # storing actions in a dataframe
        score = self._game.get_score() 
        reward = 0.1
        is_over = False #game over
        if actions[1] == 1:
            self._agent.jump()
        image = grab_screen(self._game._driver) 
        self._display.send(image) #display the image on screen
        if self._agent.is_crashed():
            scores_df.loc[len(loss_df)] = score # log the score when game is over
            self._game.restart()
            reward = -1
            is_over = True
        return image, reward, is_over #return the Experience tuple