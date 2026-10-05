from fineprint.pdf_extract import normalize_text_with_map

def test_normalize_text():
    text = 'This is an “example” of a word-\nbreak and\nsome   spaces.'
    norm, indices = normalize_text_with_map(text)
    
    assert norm == 'this is an "example" of a wordbreak and some spaces.'
    assert len(norm) == len(indices)
    assert text[indices[0]] == 'T'
    
    text2 = "No—dash"
    norm2, ind2 = normalize_text_with_map(text2)
    assert norm2 == "no-dash"
