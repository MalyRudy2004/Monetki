import pytest
from monetki import calc, get_gold, calc_inflation

def test_calc():
    dummy_jar = {
    "1gr": {"amount": 100, "weight": 1.64, "diameter": 15.5, "height": 1.4},
    "2gr": {"amount": 50,  "weight": 2.13, "diameter": 17.5, "height": 1.4},
    "5gr": {"amount": 10,  "weight": 2.59, "diameter": 19.5, "height": 1.4},
    "total": {}
    }
    result_jar = calc(dummy_jar)
    assert result_jar["1gr"]["value"] == 1.0
    assert result_jar["2gr"]["value"] == 1.0
    assert result_jar["5gr"]["value"] == 0.5
    assert result_jar["total"]["amount"] == 160
    assert result_jar["total"]["value"] == 2.5

def test_get_gold():
    today, past = get_gold()
    assert type(today) is float
    assert type(past) is float
    assert today > 0
    assert past == 145.10

def test_calc_inflation(): 
    total_pln = 1000.0
    past_price = 100.0
    today_price = 200.0
    
    grams_past, grams_today, value_if_invested, lost_income = calc_inflation(total_pln, today_price, past_price)

    assert grams_past == 10.0
    assert grams_today == 5.0
    assert value_if_invested == 2000.0
    assert lost_income == 1000.0