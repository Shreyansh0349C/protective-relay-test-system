import pytest
import math
import numpy as np

def calculate_rms(samples):
    """Calculate RMS from an array of samples."""
    return math.sqrt(sum(s**2 for s in samples) / len(samples))

def test_rms_calculation():
    # Test sine wave RMS: peak 10.0 -> RMS should be 10.0 / sqrt(2) ≈ 7.071
    t = np.linspace(0, 2 * np.pi, 200, endpoint=False)
    sine_wave = 10.0 * np.sin(t)
    rms = calculate_rms(sine_wave)
    assert math.isclose(rms, 7.071, rel_tol=1e-2)

def test_command_validation():
    def validate_voltage_ref(voltage):
        if 0.0 <= voltage <= 400.0:
            return True
        return False

    assert validate_voltage_ref(230.0) == True
    assert validate_voltage_ref(450.0) == False
    assert validate_voltage_ref(-10.0) == False
