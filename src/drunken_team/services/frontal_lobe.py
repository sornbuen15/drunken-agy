import re
from typing import List, Dict, Any


class SpeechEngine:
    def __init__(self):
        # In a real system, this could initialize espeak, pyttsx3 or aplay
        self.is_ready = True
        self.spoken_history = []

    def sanitize_input(self, text: str) -> str:
        """
        Sanitize input text to prevent command injection or malicious characters
        before passing it to a shell/OS level speech synthesizer.
        """
        # Keep only alphanumeric characters, spaces, and basic punctuation
        sanitized = re.sub(r"[^a-zA-Z0-9\s.,?!]", "", text)
        return sanitized.strip()

    def speak(self, text: str) -> bool:
        """
        Speak the sanitized text.
        Returns True if successful, False otherwise.
        """
        sanitized_text = self.sanitize_input(text)
        if not sanitized_text:
            return False

        # Simulate speech
        self.spoken_history.append(sanitized_text)
        return True


class TelemetryBuffer:
    def __init__(self, max_buffer_size: int = 1000):
        self.buffer: List[Dict[str, Any]] = []
        self.max_buffer_size = max_buffer_size

    def add_event(self, event: Dict[str, Any]) -> bool:
        """
        Add a telemetry event to the buffer.
        If the buffer is full, drops the oldest event to prevent memory exhaustion (LRU approach).
        """
        if not event:
            return False

        if len(self.buffer) >= self.max_buffer_size:
            # Drop the oldest event to prevent OOM
            self.buffer.pop(0)

        self.buffer.append(event)
        return True

    def flush(self) -> List[Dict[str, Any]]:
        """
        Flushes the buffer and returns all events to be sent to the cloud.
        """
        events = self.buffer.copy()
        self.buffer.clear()
        return events


class FrontalLobe:
    """
    Main controller for Raspberry Pi edge execution capabilities.
    """

    def __init__(self, max_telemetry_size: int = 1000):
        self.speech_engine = SpeechEngine()
        self.telemetry = TelemetryBuffer(max_buffer_size=max_telemetry_size)

    def trigger_warning(self, message: str) -> bool:
        """
        Triggers a local speech warning.
        """
        return self.speech_engine.speak(message)

    def log_telemetry(self, data: Dict[str, Any]) -> bool:
        """
        Logs telemetry locally for offline buffering.
        """
        return self.telemetry.add_event(data)

    def sync_telemetry(self) -> List[Dict[str, Any]]:
        """
        Retrieves all buffered telemetry for cloud syncing.
        """
        return self.telemetry.flush()
