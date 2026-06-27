from typing import Optional, Dict


class DeviceRegistry:
    """
    Manages device registration securely.
    """

    def __init__(self) -> None:
        # Map of device_id to user_id
        self._devices: Dict[str, str] = {}

    def register_device(self, device_id: str, user_id: str) -> None:
        """
        Register a new device to a user.
        """
        if not device_id or not isinstance(device_id, str):
            raise ValueError("Invalid device_id")
        if not user_id or not isinstance(user_id, str):
            raise ValueError("Invalid user_id")

        self._devices[device_id] = user_id

    def get_device_user(self, device_id: str) -> Optional[str]:
        """
        Retrieve the user associated with a device.
        """
        if not device_id or not isinstance(device_id, str):
            return None
        return self._devices.get(device_id)

    def remove_device(self, device_id: str) -> None:
        """
        Remove a device securely.
        """
        if device_id in self._devices:
            del self._devices[device_id]
