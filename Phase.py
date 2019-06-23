from enum import Enum
from itertools import cycle
import pygame

from Map import Map
from Cards import StrategyCardSet, StrategyCard

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


NB_OF_TURNS_FOR_STRATEGY_PICKS = {
    3: 2,
    4: 2,
    5: 1,
    6: 1}


class PhaseList(Enum):
    """
    ENUM of phase names
    """
    STRATEGY = 1
    ACTION = 2
    STATUS = 3
    AGENDA = 4


class PreCustodianPhaseFlow:
    """
    Before the Custodians have been paid, the cycle of phases excludes the agenda phase
    """
    def __init__(self, current_phase):
        self.current_phase = current_phase
        self.phase_cycle = cycle([PhaseList.STRATEGY, PhaseList.ACTION, PhaseList.STATUS])

    def next(self):
        """
        :return: False if the round is not over, True if it is
        """
        # Will there be a new round?
        new_round = False
        if self.current_phase is PhaseList.STATUS:
            new_round = True

        # get the iterator to the right spot
        while self.current_phase is not next(self.phase_cycle):
            pass
        self.current_phase = next(self.phase_cycle)

        return new_round


class PostCustodianPhaseFlow:
    """
    After the Custodians have been paid, the cycle of phases includes the agenda phase
    """
    def __init__(self, current_phase):
        self.current_phase = current_phase
        self.phase_cycle = cycle([PhaseList.STRATEGY, PhaseList.ACTION, PhaseList.STATUS, PhaseList.AGENDA])

    def next(self):
        """
        :return: False if the round is not over, True if it is
        """
        # Will there be a new round?
        new_round = False
        if self.current_phase is PhaseList.AGENDA:
            new_round = True

        # get the iterator to the right spot
        while self.current_phase is not next(self.phase_cycle):
            pass
        self.current_phase = next(self.phase_cycle)

        return new_round


class PhaseController:
    """
    Manages what phase it is, can be updated for custodians, and can change to next phase
    """
    def __init__(self, screen, player_list, have_custodians_been_paid=False):
        self.player_list = player_list
        self.have_custodians_been_paid = have_custodians_been_paid
        self.phaseFlow = PreCustodianPhaseFlow(current_phase=PhaseList.STRATEGY)
        self.phase = StrategyPhase(screen, player_list)  # initiate first phase

    def get_phase(self):
        return self.phaseFlow.current_phase

    def next_phase(self, screen):
        """
        Initializes a new phase, and returns True if the counter of turn needs updated
        :return:
        """
        self.phase.erase()  # erases completely the phase
        is_next_round = self.phaseFlow.next()
        if self.get_phase() == PhaseList.STRATEGY:
            self.phase = StrategyPhase(screen, self.player_list)
        if self.get_phase() == PhaseList.ACTION:
            self.phase = ActionPhase(screen, self.player_list)
        if self.get_phase() == PhaseList.STATUS:
            self.phase = StatusPhase(screen, self.player_list)
        if self.get_phase() == PhaseList.AGENDA:
            self.phase = AgendaPhase(screen, self.player_list)
        return is_next_round

    def pay_custodians(self):
        self.have_custodians_been_paid = True
        self.phaseFlow = PostCustodianPhaseFlow(current_phase=self.phaseFlow.current_phase)

    def handle_event(self, event, screen):
        if event.type == pygame.KEYDOWN:
            self.next_phase(screen)
        else:
            self.phase.handle_event(event, screen)


class StrategyPhase:
    """
    Handling the Strategy Phase of the game
    """

    def __init__(self, screen, player_list):
        """
        Initializing the Strategy Cards
        """

        # Generating the cards
        self.player_list = player_list
        self.available_strategy_cards = pygame.sprite.Group()
        for SC in StrategyCardSet:
            strategy_card_sprite = StrategyCard(SC)
            self.available_strategy_cards.add(strategy_card_sprite)

        # Locating them
        x_size, y_size = screen.get_size()
        y_pos = [y_size/3, 2*y_size/3]
        x_pos = [x_size/8, 3*x_size/8, 5*x_size/8, 7*x_size/8]
        locs = iter([(x, y) for x in x_pos for y in y_pos])
        for SC in self.available_strategy_cards:
            x_sc, y_sc = SC.image.get_size()
            SC.image = pygame.transform.smoothscale(SC.image, (int(x_size/8), int(x_size/8*y_sc/x_sc)))
            loc = next(locs)
            SC.update(rect=SC.image.get_rect(center=loc), image=SC.image)

    def handle_event(self, event, screen):
        pass

    def update(self, screen):
        self.available_strategy_cards.draw(screen)

    def erase(self):
        for SC in self.available_strategy_cards:
            SC.kill()


class ActionPhase:
    """
    Handling the Action Phase of the game
    """
    def __init__(self, screen, player_list):
        self.player_list = player_list
        self.map = Map(player_list, size=3)
        self.map.create_map()
        self.map.draw_tiles(screen)
        self.map.draw_hex_positions(screen)

    def handle_event(self, screen, event):
        pass

    def update(self, screen):
        # Updating MAP on hover
        for tile in self.map.tiles:
            r_hex = tile.image.get_rect(topleft=tile.pos)
            if r_hex.collidepoint(pygame.mouse.get_pos()):
                tile.update(pos=tile.pos, image=tile.image, color=BLACK)
            else:
                tile.update(pos=tile.pos, image=tile.image, color=WHITE)
        self.map.tiles.draw(screen)
        self.map.draw_players(screen)
        self.map.draw_hex_positions(screen)

    def erase(self, screen):
        pass


class StatusPhase:
    """
    Handling the Status Phase of the game
    """
    def __init__(self, player_list):
        self.player_list = player_list


class AgendaPhase:
    """
    Handling the Agenda Phase of the game
    """
    def __init__(self, player_list):
        self.player_list = player_list