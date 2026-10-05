from decimal import Decimal
from fineprint.costs import format_inr, calc_costs, CostLine
from fineprint.schemas import Terms, Term, Evidence

def test_format_inr():
    assert format_inr(Decimal('999')) == "₹999"
    assert format_inr(Decimal('12488')) == "₹12,488"
    assert format_inr(Decimal('112488')) == "₹1,12,488"

def test_calc_costs():
    terms = Terms(
        monthly_price=Term(value=999, evidence=Evidence(page=1, source_text="")),
        term_months=Term(value=12, evidence=Evidence(page=1, source_text="")),
        setup_fee=Term(value=500, evidence=Evidence(page=1, source_text="")),
        auto_renews=Term(value=True, evidence=Evidence(page=2, source_text="")),
        renewal_price_monthly=Term(value=1199, evidence=Evidence(page=2, source_text=""))
    )
    
    costs = calc_costs(terms)
    assert len(costs) == 2
    assert costs[0].amount == Decimal('12488')
    assert costs[1].amount == Decimal('2400')
