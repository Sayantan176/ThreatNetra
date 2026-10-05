from fineprint.samples import make_samples, verify_samples
import os

def test_make_samples():
    make_samples()
    assert os.path.exists("samples/PlanA.pdf")
    assert os.path.exists("samples/PlanB.pdf")
    verify_samples()
