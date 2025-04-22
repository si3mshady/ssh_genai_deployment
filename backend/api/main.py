from fastapi import FastAPI, UploadFile, File
import yaml, requests, time

app = FastAPI()

OLLAMA_URL = "http://ollama:11434/api/generate"
OLLAMA_MODEL = "mixtral"

with open("api/slo_config.yaml") as f:
    slo_config = yaml.safe_load(f)

@app.post("/analyze")
async def analyze_logs(file: UploadFile = File(...)):
    content = await file.read()
    logs = content.decode().splitlines()
    total = len(logs)
    errors = len([l for l in logs if "500" in l or "error" in l.lower()])
    availability = ((total - errors) / total) * 100

    prompt = f"[INST] Analyze logs:\n{logs[:10]}\nSummarize total requests, errors, availability, and latency. [/INST]"

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=300
        )
        response.raise_for_status()
        summary = response.json().get("response", "").strip()
    except Exception as e:
        summary = f"LLM execution failed: {e}"

    slo_avail = slo_config['availability']
    error_budget = 100 - slo_avail
    used_budget = max(0, availability - slo_avail)
    budget_remaining = max(0, error_budget - used_budget)

    return {
        "total_requests": total,
        "errors": errors,
        "availability": availability,
        "error_budget_remaining": budget_remaining,
        "summary": summary
    }
