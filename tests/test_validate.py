from fineprint.schemas import Finding, Term, Evidence, Document, Page
from fineprint.validate import validate_finding, validate_term

def test_validation():
    doc = Document(path="test.pdf", sha256="abc", pages=[
        Page(number=1, text="The fee is Rs. 500."),
        Page(number=2, text="Auto-renews at Rs. 1,199.")
    ])
    
    # 1. Exact
    f1 = Finding(id="1", category="fees", severity="info", title="t", page=1, source_text="The fee is Rs. 500.", explanation="e", potential_consequence="p")
    v1 = validate_finding(f1, doc)
    assert v1.verified
    assert v1.match_method == "exact"
    
    # 2. Page corrected
    f2 = Finding(id="2", category="fees", severity="info", title="t", page=1, source_text="Auto-renews at Rs. 1,199.", explanation="e", potential_consequence="p")
    v2 = validate_finding(f2, doc)
    assert v2.verified 
    assert v2.verified_page == 2
    assert v2.match_method == "page_corrected"
    
    # 3. Fuzzy match
    f3 = Finding(id="3", category="fees", severity="info", title="t", page=1, source_text="The fee is Rs 500", explanation="e", potential_consequence="p")
    v3 = validate_finding(f3, doc)
    assert v3.verified
    assert v3.match_method == "fuzzy"
    
    # 4. Rejected (hallucinated)
    f4 = Finding(id="4", category="fees", severity="info", title="t", page=1, source_text="Free for first year.", explanation="e", potential_consequence="p")
    assert not validate_finding(f4, doc).verified
    
    # 5. Term numeric check failure
    t1 = Term(value=1000, evidence=Evidence(page=1, source_text="The fee is Rs. 500."))
    assert not validate_term(t1, doc)
    
    # 6. Term numeric check pass
    t2 = Term(value=500, evidence=Evidence(page=1, source_text="The fee is Rs. 500."))
    assert validate_term(t2, doc)
