import os
import shutil
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn

from fineprint.pdf_extract import extract_pdf
from fineprint.llm import GroqClient
from fineprint.analyze import analyze_document
from fineprint.costs import calc_costs

app = FastAPI(title="FinePrint Web")
templates = Jinja2Templates(directory="templates")

os.makedirs("uploads", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request})

@app.post("/analyze", response_class=HTMLResponse)
def analyze(request: Request, file: UploadFile = File(...)):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Process the PDF
    doc = extract_pdf(file_path)
    llm = GroqClient()
    result = analyze_document(doc, llm, use_cache=True)
    costs = calc_costs(result.terms)
    
    # Render results
    return templates.TemplateResponse(request=request, name="result.html", context={
        "request": request,
        "filename": file.filename,
        "findings": result.findings,
        "terms": result.terms,
        "costs": costs,
        "discarded": result.discarded_findings
    })

from fineprint.compare import compare_terms, generate_verdict

@app.post("/compare", response_class=HTMLResponse)
def compare_contracts(request: Request, file1: UploadFile = File(...), file2: UploadFile = File(...)):
    path1 = f"uploads/{file1.filename}"
    path2 = f"uploads/{file2.filename}"
    with open(path1, "wb") as buffer: shutil.copyfileobj(file1.file, buffer)
    with open(path2, "wb") as buffer: shutil.copyfileobj(file2.file, buffer)
    
    doc1 = extract_pdf(path1)
    doc2 = extract_pdf(path2)
    llm = GroqClient()
    
    res1 = analyze_document(doc1, llm, use_cache=True)
    res2 = analyze_document(doc2, llm, use_cache=True)
    
    rows = compare_terms(res1.terms, res2.terms)
    verdict = generate_verdict(rows, llm)
    
    return templates.TemplateResponse(request=request, name="compare_result.html", context={
        "request": request,
        "filename1": file1.filename,
        "filename2": file2.filename,
        "rows": rows,
        "verdict": verdict
    })

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
