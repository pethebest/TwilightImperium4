from enum import Enum
from itertools import cycle


NB_OF_TURNS_FOR_STRATEGY_PICKS = {
    3: 2,
    4: 2,
    5: 1,
    6: 1}


class StrategyPhase:
    """
    Organizes the execution of a strategy phase
    """

    def __init__(self,
                 game,
                 player_list_from_speaker
                 ):
        pass


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
    def __init__(self, have_custodians_been_paid=False):
        self.have_custodians_been_paid = have_custodians_been_paid
        self.phaseFlow = PreCustodianPhaseFlow(current_phase=PhaseList.STRATEGY)

    def next_phase(self):
        is_next_round = self.phaseFlow.next()
        return is_next_round

    def pay_custodians(self):
        self.have_custodians_been_paid = True
        self.phaseFlow = PostCustodianPhaseFlow(current_phase=self.phaseFlow.current_phase)

