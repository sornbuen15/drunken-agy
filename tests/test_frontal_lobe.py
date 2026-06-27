from drunken_team.services.frontal_lobe import (
    SpeechEngine,
    TelemetryBuffer,
    FrontalLobe,
)


def test_speech_engine_sanitize():
    engine = SpeechEngine()
    # Should keep only alphanumeric and basic punctuation
    sanitized = engine.sanitize_input("Warning: Intruder at sector 7G! rm -rf /")
    assert sanitized == "Warning Intruder at sector 7G! rm rf"


def test_speech_engine_speak():
    engine = SpeechEngine()
    result = engine.speak("Intruder detected!")
    assert result is True
    assert len(engine.spoken_history) == 1
    assert engine.spoken_history[0] == "Intruder detected!"


def test_telemetry_buffer_add_and_flush():
    buffer = TelemetryBuffer(max_buffer_size=2)
    buffer.add_event({"cpu_temp": 45})
    buffer.add_event({"cpu_temp": 50})

    assert len(buffer.buffer) == 2

    events = buffer.flush()
    assert len(events) == 2
    assert len(buffer.buffer) == 0


def test_telemetry_buffer_overflow():
    buffer = TelemetryBuffer(max_buffer_size=2)
    buffer.add_event({"id": 1})
    buffer.add_event({"id": 2})
    buffer.add_event({"id": 3})  # Should drop id=1

    assert len(buffer.buffer) == 2
    assert buffer.buffer[0]["id"] == 2
    assert buffer.buffer[1]["id"] == 3


def test_frontal_lobe_integration():
    lobe = FrontalLobe(max_telemetry_size=5)

    # Test speech warning
    assert lobe.trigger_warning("System Overheating") is True
    assert len(lobe.speech_engine.spoken_history) == 1

    # Test telemetry
    lobe.log_telemetry({"sensor": "heat", "value": 85})
    lobe.log_telemetry({"sensor": "heat", "value": 90})

    events = lobe.sync_telemetry()
    assert len(events) == 2
    assert events[0]["value"] == 85
