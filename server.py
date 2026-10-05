import os
import sys

# Ensure both sub-projects are in path so they can import their own modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, "threat-netra-main"))
sys.path.insert(0, os.path.join(current_dir, "src"))

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

# Import the FinePrint app
from fineprint_app import app as fineprint_app

# Import the Threat Netra app
from main import app as threat_netra_app

app = FastAPI(title="Threat Netra")

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Threat Netra</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>body { font-family: 'Inter', sans-serif; background-color: #f3f4f6; }</style>
    </head>
    <body class="min-h-screen flex items-center justify-center">
        <div class="bg-white p-10 rounded-2xl shadow-lg border border-gray-100 max-w-2xl text-center">
            <h1 class="text-4xl font-bold text-gray-900 mb-4 tracking-tight">Threat Netra</h1>
            <p class="text-gray-500 mb-10">A Swiss-Army Knife for Threat Intelligence</p>
            
            <div class="grid grid-cols-2 gap-6">
                <!-- FinePrint Card -->
                <a href="/fineprint" class="group block p-8 bg-blue-50 hover:bg-blue-600 rounded-xl transition-all duration-300 border border-blue-100 shadow-sm text-left">
                    <div class="text-blue-600 group-hover:text-white font-bold text-xl mb-2 transition-colors">FinePrint</div>
                    <p class="text-blue-800 group-hover:text-blue-100 text-sm transition-colors">Evidence-first AI analyst for consumer contracts. Upload and compare PDFs.</p>
                </a>
                
                <!-- OSINT Feed Analyzer Card -->
                <a href="/threat" class="group block p-8 bg-slate-900 hover:bg-slate-800 rounded-xl transition-all duration-300 border border-slate-800 shadow-sm text-left">
                    <div class="text-emerald-400 group-hover:text-emerald-300 font-bold text-xl mb-2 transition-colors">OSINT Feed Analyzer</div>
                    <p class="text-slate-400 group-hover:text-slate-300 text-sm transition-colors">Cyber Threat Intelligence (CTI) monitoring platform with live OSINT parsing.</p>
                </a>
            </div>
        </div>
    </body>
    </html>
    """

# Mount the sub-apps
app.mount("/fineprint", fineprint_app)
app.mount("/threat", threat_netra_app)

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
