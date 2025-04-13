from app_state import AppState
from interface import AppInterface

class AppContext:
    """
    Provides a context related to the app
    """

    def __init__(self, *, state: AppState, interface: AppInterface):
        self.state = state
        self.interface = interface

    @staticmethod
    def create():
        return AppContext(state=AppState.load(), interface=AppInterface())
