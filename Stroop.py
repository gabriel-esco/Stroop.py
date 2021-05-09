import pygame
import copy
import random
import time
import csv

pygame.init()
#font = pygame.font.Font('arial.ttf', 25)
font = pygame.font.SysFont('trebuchetmsbolditalic', 25)

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE = (0, 0, 255)
GREEN = (50, 168, 82)
YELLOW = (245, 245, 73)
BLACK = (0,0,0)

#Ensure that words and colors are written in same order
WORDS = ['Blue', 'Red', 'Green', 'Yellow']
COLORS = [BLUE, RED, GREEN, YELLOW]

class StroopGame:

    def __init__(self, w=960, h=720):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Stroop Effect Experiment')
        self.clock = pygame.time.Clock()
        
        # init game
        self.gamemode = 0
        self.gameCounter = 0
        self.score = 0
        self.wrong = 0
        self.stats = []
        self._shuffle_words()
        self._update_ui()
        self.start = time.time()

    def _shuffle_words(self):
        #shuffle order of words to match them with directions randomly
        shuffledWords = random.sample(WORDS, len(WORDS))
        
        self.up = shuffledWords[0]
        self.down = shuffledWords[1]
        self.right = shuffledWords[2]
        self.left = shuffledWords[3]

        #choose random color to be correct answer
        wordChoice = random.choice(shuffledWords)
        self.wordChoice = wordChoice

        if self.up == wordChoice:
            self.correctAns = self.up
        elif self.down == wordChoice:
            self.correctAns = self.down
        elif self.right == wordChoice:
            self.correctAns = self.right
        elif self.left == wordChoice:
            self.correctAns = self.left
        
    def play_step(self):
        #start timer
        start = time.time()

        # search for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # analyze user input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.correctAns == self.left:
                    self.score += 1
                    result = 'Correct'
                elif event.key == pygame.K_RIGHT and self.correctAns == self.right:
                    self.score += 1
                    result = 'Correct'
                elif event.key == pygame.K_UP and self.correctAns == self.up:
                    self.score += 1
                    result = 'Correct'
                elif event.key == pygame.K_DOWN and self.correctAns == self.down:
                    self.score += 1
                    result = 'Correct'
                else:
                    self.wrong += 1
                    result = 'Wrong'
                
                self.gameCounter += 1

                #stop timer and store stats
                end = time.time()
                responseTime = end - game.start
                if copy.deepcopy(self.gamemode) == 0:
                    gamemode = 'No Distractors'
                else:
                    gamemode = 'Distractors'
                trial = copy.deepcopy(self.gameCounter)
                stats = [gamemode, str(trial), result, str(responseTime)]
                self.stats.append(stats)

                #shuffle words and update UI
                game._shuffle_words()
                game._update_ui()
                game.start = time.time()
                
        
    def _update_ui(self):
        #initialize display
        self.display.fill(BLACK)
        wordChoiceText = font.render(self.wordChoice, True, WHITE)
        self.display.blit(wordChoiceText, [480, 360])
        if self.gamemode == 0:
            gamemodeText = font.render('Gamemode: No Distractions', True, WHITE)
            self.display.blit(gamemodeText, [0,0])
        elif self.gamemode == 1:
            gamemodeText = font.render('Gamemode: Distractions', True, WHITE)
            self.display.blit(gamemodeText, [0,0])
        scoreText = font.render('Score: ' + str(self.score), True, WHITE)
        self.display.blit(scoreText, [0, 20])


        #no-distraction game mode word placement
        if self.gamemode == 0:
            topColor = COLORS[WORDS.index(self.up)]
            bottomColor = COLORS[WORDS.index(self.down)]
            leftColor = COLORS[WORDS.index(self.left)]
            rightColor = COLORS[WORDS.index(self.right)]
        
        #distraction game mode word placement
        elif self.gamemode == 1:
            #shuffle colors
            shuffledColors = random.sample(COLORS, len(COLORS))

            topColor = shuffledColors[WORDS.index(self.up)]
            bottomColor = shuffledColors[WORDS.index(self.down)]
            leftColor = shuffledColors[WORDS.index(self.left)]
            rightColor = shuffledColors[WORDS.index(self.right)]

        #create word display
        topText = font.render(self.up, True, topColor)
        self.display.blit(topText, [480, 200])
        bottomText = font.render(self.down, True, bottomColor)
        self.display.blit(bottomText, [480, 520])
        leftText = font.render(self.left, True, leftColor)
        self.display.blit(leftText, [320, 360])
        rightText = font.render(self.right, True, rightColor)
        self.display.blit(rightText, [640, 360])

        pygame.display.flip()
        
            

if __name__ == '__main__':
    #initialize work
    game = StroopGame()
    
    #set no-distraction gamemode
    game.gamemode = 0
    
    #run game until reaching 36 trials and store score 
    while True:
        game.play_step()
        if game.gameCounter == 20:
            break
    score = copy.deepcopy(game.score)

    #set distraction gamemode, reset score and counter
    game.gamemode = 1
    game.gameCounter = 0
    game.score = 0
    while True:
        game.play_step()
        if game.gameCounter == 20:
            break
    distracted_score = game.score
    
    #upload data to csv file
    with open('stroop_data.csv', mode='w') as stroop_file:
        stats = ['game_mode', 'trial', 'result', 'response_time']
        writer = csv.writer(stroop_file)
        for row in game.stats:
            writer.writerow(row)
    
    print('Final Non-Distracted Score', score)
    print('Final Distracted Score', distracted_score)
        
        
    pygame.quit()