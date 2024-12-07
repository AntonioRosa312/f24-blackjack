import pygame
import os
import sys

from generalDef import *

CHIP_WIDTH, CHIP_HEIGHT = 100, 100


class Chip:
    def __init__(self, chip_value):
        self.value = chip_value
        self.image = self.chip_image()
        self.button_rect = None
        self.button = self.chip_button()

    def chip_image(self):
        match self.value:
            # white
            case 1: return pygame.transform.scale(pygame.image.load("PNG-chips/chip$1.png"), (CHIP_WIDTH, CHIP_HEIGHT))
            # red
            case 5: return pygame.transform.scale(pygame.image.load("PNG-chips/chip$5.png"), (CHIP_WIDTH, CHIP_HEIGHT))
            # green
            case 25: return pygame.transform.scale(pygame.image.load("PNG-chips/chip$25.png"), (CHIP_WIDTH, CHIP_HEIGHT))
            # black
            case 100: return pygame.transform.scale(pygame.image.load("PNG-chips/chip$100.png"), (CHIP_WIDTH, CHIP_HEIGHT))
            # purple
            case 500: return pygame.transform.scale(pygame.image.load("PNG-chips/chip$500.png"), (CHIP_WIDTH, CHIP_HEIGHT))
            # maroon
            case 1000: return pygame.transform.scale(pygame.image.load("PNG-chips/chip$1000.png"), (CHIP_WIDTH, CHIP_HEIGHT))

    def chip_button(self):
        # Button position
        buttonX, buttonY = (WIDTH - self.image.get_width()) // 2, (HEIGHT - self.image.get_height()) // 2
        self.button_rect = pygame.Rect(buttonX, buttonY, self.image.get_width(), self.image.get_height())
        return (buttonX, buttonY)



# this creates a chip list with each different chip value
chip_list = [Chip(c) for c in (1,5)]#,25,100,500,100)] 



def argParse():
    if len(sys.argv) < 2:
        return False
    elif len(sys.argv) == 2:
        match sys.argv[1]:
            case "-ai":
                return True
            case "-standard":
                return False
            case _:
                print(f"ERROR: INCORRECT ARGUMENT \"{sys.argv[1]}\" PASSED, TRY \"-ai\" OR \"-standard\"\n")
                sys.exit(os.EX_OK) #Exit code 64: Command line usage error.
    else: 
        print("ERROR: INSUFFICIENT AMOUNT OF ARGUMENTS PASSED\n")
        sys.exit(os.EX_OK) #Exit code 64: Command line usage error.

