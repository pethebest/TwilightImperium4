import pygame

from Tools import from_relative_to_absolute, get_scale
from Tools import BLACK, WHITE
from Player import ActionType

pygame.font.init()
largerFont = pygame.font.SysFont('Helvetica', 16)


class Button(pygame.sprite.Sprite):

    def __init__(self, color, width, height, text, text_size):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.text = text
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.font = pygame.font.SysFont("Arial", text_size)
        self.textSurf = self.font.render(text, 1, self.color)
        w = self.textSurf.get_width()
        h = self.textSurf.get_height()
        self.image.blit(self.textSurf, [width/2 - w/2, height/2 - h/2])

    def change_color(self, color):
        self.color = color
        self.textSurf = self.font.render(self.text, 1, self.color.value)
        w = self.textSurf.get_width()
        h = self.textSurf.get_height()
        self.image.blit(self.textSurf, [self.width / 2 - w / 2, self.height / 2 - h / 2])


class UserInterface:

    def __init__(self, current_player):
        self.current_player = current_player
        self.action_selection_buttons = pygame.sprite.Group()
        self.initiate_action_choice_buttons()

    def change_main_color(self, color):
        for button in self.action_selection_buttons:
            button.change_color(color)

    def initiate_action_choice_buttons(self):
        for i, action in enumerate(ActionType.subclasses):
            button = Button(self.current_player.color.value,
                            get_scale(),
                            get_scale()/2,
                            action,
                            14)
            button.rect.center = from_relative_to_absolute(0.90, 0.90 - 0.1*i)
            self.action_selection_buttons.add(button)

    def draw_current_player_tracker(self, screen):
        x_size, y_size = screen.get_size()
        current_turn = largerFont.render('Current Player is #%.0f - %s' % (self.current_player.agenda_order + 1,
                                                                           self.current_player.race.name),
                                         False, BLACK)
        screen.blit(current_turn, (80 / 100 * x_size, 5 / 100 * y_size))

    def draw(self, screen):
        self.action_selection_buttons.draw(screen)
        self.draw_current_player_tracker(screen)

