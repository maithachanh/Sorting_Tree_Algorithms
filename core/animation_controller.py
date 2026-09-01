"""
Animation Controller managing playback, stepping forward/backward, speed and step scrub slider.
"""
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from config import SPEED_DEFAULT

class AnimationController(QObject):
    step_updated = pyqtSignal(object, int, int) # (step_state, current_step_idx, total_steps)
    play_state_changed = pyqtSignal(bool)       # is_playing
    animation_finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.steps = []
        self.current_idx = 0
        self.is_playing = False
        self.delay_ms = SPEED_DEFAULT

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._on_timer_tick)

    def load_generator(self, generator_func, *args, **kwargs):
        """Pre-evaluates the algorithm generator into a discrete step history."""
        self.pause()
        self.steps.clear()
        self.current_idx = 0

        gen = generator_func(*args, **kwargs)
        for state in gen:
            self.steps.append(state)

        if not self.steps:
            return

        # Emit initial step
        self.step_updated.emit(self.steps[0], 0, len(self.steps))

    def play(self):
        if not self.steps:
            return
        if self.current_idx >= len(self.steps) - 1:
            self.current_idx = 0
        self.is_playing = True
        self.play_state_changed.emit(True)
        self.timer.start(self.delay_ms)

    def pause(self):
        self.is_playing = False
        self.timer.stop()
        self.play_state_changed.emit(False)

    def toggle_play(self):
        if self.is_playing:
            self.pause()
        else:
            self.play()

    def step_forward(self):
        self.pause()
        if self.current_idx < len(self.steps) - 1:
            self.current_idx += 1
            self.step_updated.emit(self.steps[self.current_idx], self.current_idx, len(self.steps))
            if self.current_idx == len(self.steps) - 1:
                self.animation_finished.emit()

    def step_backward(self):
        self.pause()
        if self.current_idx > 0:
            self.current_idx -= 1
            self.step_updated.emit(self.steps[self.current_idx], self.current_idx, len(self.steps))

    def jump_to_step(self, idx):
        if not self.steps:
            return
        idx = max(0, min(idx, len(self.steps) - 1))
        self.current_idx = idx
        self.step_updated.emit(self.steps[self.current_idx], self.current_idx, len(self.steps))
        if self.current_idx == len(self.steps) - 1:
            self.pause()
            self.animation_finished.emit()

    def reset(self):
        self.pause()
        self.current_idx = 0
        if self.steps:
            self.step_updated.emit(self.steps[0], 0, len(self.steps))

    def set_speed(self, delay_ms):
        self.delay_ms = delay_ms
        if self.is_playing:
            self.timer.setInterval(self.delay_ms)

    def _on_timer_tick(self):
        if self.current_idx < len(self.steps) - 1:
            self.current_idx += 1
            self.step_updated.emit(self.steps[self.current_idx], self.current_idx, len(self.steps))
            if self.current_idx == len(self.steps) - 1:
                self.pause()
                self.animation_finished.emit()
        else:
            self.pause()
            self.animation_finished.emit()
