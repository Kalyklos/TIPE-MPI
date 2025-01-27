class Card:
    def __init__ (self, c_type, name):
        """Init of the Card class

        Args:
            c_type (str): The type of the card (like "Creature", "Instant"...)
            name (str): The name of the card
        """
        self.c_type = c_type
        self.name = name