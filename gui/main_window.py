"""
Main Application Window managing the view stack navigation and dark theme.
"""
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from config import APP_TITLE, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from utils.theme import DARK_STYLESHEET

from gui.views.input_view import InputView
from gui.views.algorithm_select_view import AlgorithmSelectView
from gui.views.visualizer_view import VisualizerView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.setStyleSheet(DARK_STYLESHEET)

        # Central Widget & Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Navigation Stack
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # Initialize Views
        self.input_view = InputView()
        self.algo_select_view = AlgorithmSelectView()
        self.visualizer_view = VisualizerView()

        self.stack.addWidget(self.input_view)         # Index 0
        self.stack.addWidget(self.algo_select_view)   # Index 1
        self.stack.addWidget(self.visualizer_view)    # Index 2

        # Connect Navigation Signals
        self.input_view.continue_requested.connect(self._goto_algo_select)
        self.algo_select_view.back_to_input_requested.connect(self._goto_input)
        self.algo_select_view.algorithm_selected.connect(self._goto_visualizer)
        self.visualizer_view.back_to_algo_select.connect(self._goto_algo_select)
        self.visualizer_view.request_change_data.connect(self._goto_input)

        # Start at Input View
        self.stack.setCurrentIndex(0)

    def _goto_input(self):
        self.stack.setCurrentIndex(0)

    def _goto_algo_select(self):
        self.stack.setCurrentIndex(1)

    def _goto_visualizer(self, cat, key, name, meta):
        self.stack.setCurrentIndex(2)
        self.visualizer_view.start_simulation()
