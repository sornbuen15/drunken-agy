from typing import Dict


class EntitlementService:
    """
    Service to check real-time subscription entitlement.
    """

    def __init__(self) -> None:
        # Mock subscription data: map of user_id to active status
        self._subscriptions: Dict[str, bool] = {}

    def set_subscription(self, user_id: str, active: bool) -> None:
        """
        Update a user's subscription status.
        """
        if not user_id or not isinstance(user_id, str):
            raise ValueError("Invalid user_id")
        self._subscriptions[user_id] = active

    def is_user_subscribed(self, user_id: str) -> bool:
        """
        Check if a user has an active subscription.
        """
        if not user_id or not isinstance(user_id, str):
            return False
        return self._subscriptions.get(user_id, False)


class Gatekeeper:
    """
    Combines device registry and entitlement to act as the primary stream guard.
    """

    def __init__(self, registry, entitlement_service) -> None:
        self.registry = registry
        self.entitlement_service = entitlement_service

    def check_access(self, device_id: str) -> bool:
        """
        Verify if the given device stream should be allowed access.
        Fails closed by default.
        """
        if not device_id:
            return False

        user_id = self.registry.get_device_user(device_id)
        if not user_id:
            return False

        return self.entitlement_service.is_user_subscribed(user_id)
