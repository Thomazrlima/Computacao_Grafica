"""Demonstrating functionality"""
import sys

from core.base import Base

class Test(Base):
    """Check keys"""
    def initialize(self):
        print("Initializing program...")

    def update(self):
        """debug printing"""
        if len(self.input.key_down_list) > 0:
            print( "Keys down:", self.input.key_down_list )
        if len(self.input.key_pressed_list) > 0:
            print( "Keys pressed:", self.input.key_pressed_list )
        if len(self.input.key_up_list) > 0:
            print( "Keys up:", self.input.key_up_list )

# instantiate this class and run the program
Test().run()
