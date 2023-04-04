import pygame
from skimage.metrics import structural_similarity
import imutils
import cv2

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255,0,0)

# Set up the screen
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spot the difference")

# Load the background image
background = pygame.image.load("Spot the difference/Assets/Images/UI/background.jpeg")

# Load the button image
easyBtn_img = pygame.image.load("Spot the difference/Assets/Images/UI/Easy_button.png")
mediumBtn_img = pygame.image.load("Spot the difference/Assets/Images/UI/Medium_button.png")
hardBtn_img = pygame.image.load("Spot the difference/Assets/Images/UI/Hard_button.png")

# Set up the font
font = pygame.font.Font("F:/pythonProject/Spot the difference/Assets/ARIAL.TTF", 26)
# Set up the buttons
EASY_BUTTON_X = SCREEN_WIDTH // 2 - 100
EASY_BUTTON_Y = SCREEN_HEIGHT // 3 + 100
EASY_BUTTON_RECT = easyBtn_img.get_rect()
easy_button = pygame.Rect(EASY_BUTTON_X, EASY_BUTTON_Y, EASY_BUTTON_RECT.width, EASY_BUTTON_RECT.height)


MEDIUM_BUTTON_X = SCREEN_WIDTH // 2 - 100
MEDIUM_BUTTON_Y = SCREEN_HEIGHT // 2 + 100
MEDIUM_BUTTON_RECT= mediumBtn_img.get_rect()
medium_button = pygame.Rect(MEDIUM_BUTTON_X, MEDIUM_BUTTON_Y, MEDIUM_BUTTON_RECT.width, MEDIUM_BUTTON_RECT.height)

HARD_BUTTON_X = SCREEN_WIDTH // 2 - 100
HARD_BUTTON_Y = SCREEN_HEIGHT // 1.5 + 100
HARD_BUTTON_RECT = hardBtn_img.get_rect()
hard_button = pygame.Rect(HARD_BUTTON_X, HARD_BUTTON_Y, HARD_BUTTON_RECT.width, HARD_BUTTON_RECT.height)
no_of_differences = 0
button_enabled = True
# Main game loop
running = True
mode = None
scores = 0
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and button_enabled:
            # Check if a button was clicked
            mouse_pos = pygame.mouse.get_pos()
            if easy_button.collidepoint(mouse_pos):
                mode = 'easy'
                button_enabled = False
            elif medium_button.collidepoint(mouse_pos):
                mode = 'medium'
                button_enabled = False
            elif hard_button.collidepoint(mouse_pos):
                mode = 'hard'
                button_enabled = False
            # Load the images according to the selected difficulty level
            if mode == 'easy':
                print('Easy mode selected')
                image_one = cv2.imread("Spot the difference/Assets/Images/Input/Input.jpeg")
                image_two = cv2.imread("Spot the difference/Assets/Images/Output/easy_output.jpeg")
            elif mode == 'medium':
                print('Medium mode selected')
                image_one = cv2.imread("Spot the difference/Assets/Images/Input/Input.jpeg")
                image_two = cv2.imread("Spot the difference/Assets/Images/Output/medium_output.jpeg")
            else:
                print('Hard mode selected')
                image_one = cv2.imread("Spot the difference/Assets/Images/Input/Input.jpeg")
                image_two = cv2.imread("Spot the difference/Assets/Images/Output/hard_output.jpeg")
            if mode is not None :
                screen_width = 1280
                screen_height = 640
                screen = pygame.display.set_mode((screen_width, screen_height)) 
                # Resize the images to a smaller size   
                image_one = cv2.resize(image_one, (640, 480))
                image_two = cv2.resize(image_two, (640, 480))
                
                gray1 = cv2.cvtColor(image_one, cv2.COLOR_BGR2GRAY)
                gray2 = cv2.cvtColor(image_two, cv2.COLOR_BGR2GRAY)

                # Compute the structural similarity between the images
                (score, diff) = structural_similarity(gray1, gray2, full=True)
                diff = (diff * 255).astype("uint8")

                # Threshold the difference image
                thresh = cv2.threshold(diff, 0, 128, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU) [1]

                # Find the contours in the thresholded image
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
        elif event.type == pygame.MOUSEBUTTONDOWN and mode is not None:
            for c in cnts:
                (x, y, w, h ) = cv2.boundingRect(c)
                rect_area = w*h
                if rect_area > 15:
                    no_of_differences += 1
            # Check if the user clicked on a difference
            pos = pygame.mouse.get_pos()
            for c in cnts:
                (x, y, w, h) = cv2.boundingRect(c)
                if x <= pos[0] <= x + w and y <= pos[1] <= y + h:
                    # Highlight the difference
                    cv2.rectangle(image_one, (x, y), (x + w, y + h), RED, 2)
                    cv2.rectangle(image_two, (x, y), (x + w, y + h), RED, 2)
                    # Increase the score
                    screen.fill(BLACK)
                    scores += 1
                    print("Score: {}".format(score))
            if scores == no_of_differences:
                running = False
                print("Victory!")

            
    if mode is None:
        # Draw the background
        screen.blit(background, (0, 0))
        
        # Draw the buttons 
        screen.blit(easyBtn_img, easy_button)
        screen.blit(mediumBtn_img, medium_button)
        screen.blit(hardBtn_img, hard_button)
    else:  
        # Transpose the images to switch the rows and columns
        image_one_transposed = cv2.transpose(image_one)
        image_two_transposed = cv2.transpose(image_two)
        
        # Convert the transposed images to surfaces
        image_one_surface = pygame.surfarray.make_surface(cv2.cvtColor(image_one_transposed, cv2.COLOR_BGR2RGB))
        image_two_surface = pygame.surfarray.make_surface(cv2.cvtColor(image_two_transposed, cv2.COLOR_BGR2RGB))
        
        # Draw the images on the screen
        screen.blit(image_one_surface, (0, 0))
        screen.blit(image_two_surface, (640, 0))
        
        # Draw the score on the screen  
       
        score_text = font.render("Score: {}".format(scores), True, WHITE)
        screen.blit(score_text, (screen_width // 2 - 80, screen_height - 50))
    
    # Update the screen
    pygame.display.update()

# Quit Py game
pygame.quit()
