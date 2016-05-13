import pytest
import citeTPC


def test_Gregory_Bigwood():
    results = citeTPC.findMembersPapers("Gregory%20Bigwood")
    print results

def test_Tristan_Henderson():
    results = citeTPC.findMembersPapers("Tristan%20Henderson")
    print results

def test_Iain_Parris_Privacy():
    results = citeTPC.findMembersPapers("Iain%20Parris%20Privacy")
    print results

