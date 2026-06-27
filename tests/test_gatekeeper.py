import pytest
from drunken_team.services.device_registry import DeviceRegistry
from drunken_team.services.entitlement import EntitlementService, Gatekeeper


def test_device_registration():
    registry = DeviceRegistry()
    registry.register_device("dev-1", "user-1")
    assert registry.get_device_user("dev-1") == "user-1"

    with pytest.raises(ValueError):
        registry.register_device("", "user-2")


def test_entitlement_service():
    ent = EntitlementService()
    assert not ent.is_user_subscribed("user-1")
    ent.set_subscription("user-1", True)
    assert ent.is_user_subscribed("user-1")


def test_gatekeeper_access():
    registry = DeviceRegistry()
    ent = EntitlementService()
    gatekeeper = Gatekeeper(registry, ent)

    # Register and subscribe
    registry.register_device("dev-1", "user-1")
    ent.set_subscription("user-1", True)

    # Should grant access
    assert gatekeeper.check_access("dev-1")

    # Unknown device -> fail closed
    assert not gatekeeper.check_access("dev-unknown")

    # Unsubscribed user -> fail closed
    ent.set_subscription("user-1", False)
    assert not gatekeeper.check_access("dev-1")
