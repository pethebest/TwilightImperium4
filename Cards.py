class Card:
    """
    An abstract class for methods that are common to all cards
    """

    def __init__(self):
        pass


class ObjectiveCard(Card):
    """
    A class for objective cards
    """

    def __init__(self):
        Card.__init__(self)
