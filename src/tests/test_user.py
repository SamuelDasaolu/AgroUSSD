import pytest
from src.models.user import Farmer, Buyer
from src.utils import data_handler as dh


@pytest.fixture(autouse=True)
def reset_db():
    """Reset the users and orders JSON files before every test"""
    dh.save_user_data({"farmers": [], "buyers": []})
    dh.save_orders({"orders": []})
    yield


def test_farmer_registration():
    farmer = Farmer("Adamu", "+2348012345678", "1234")
    result = farmer.register()
    assert result is True
    assert farmer.user_id is not None


def test_buyer_registration_and_authentication():
    buyer = Buyer("Kemi", "+2348098765432", "5678")
    buyer.register()
    assert buyer.authenticate("5678") is True
    assert buyer.is_authenticated is True


def test_add_produce():
    farmer = Farmer("Adamu", "+2348012345678", "1234")
    farmer.register()
    farmer.authenticate("1234")
    farmer.add_produce("Tomatoes", 50)
    assert len(farmer.view_produce()) > 0


def test_place_order():
    farmer = Farmer("Adamu", "+2348012345678", "1234")
    farmer.register()
    farmer.authenticate("1234")
    farmer.add_produce("Tomatoes", 50)

    buyer = Buyer("Kemi", "+2348098765432", "5678")
    buyer.register()
    buyer.authenticate("5678")

    order = buyer.place_order(farmer.user_id, "Tomatoes", 20)
    assert order is not None
    assert order["quantity"] == 20
    assert order["product"] == "Tomatoes"
