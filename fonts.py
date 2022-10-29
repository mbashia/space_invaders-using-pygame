#checking fonts in your system
import pygame
pygame.init()
fonts = pygame.font.get_fonts()
print(len(fonts))
for f in fonts:
    print(f)