
import os
import json
from typing import List, Dict, Any, Tuple
import gradio as gr

# Optional: load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# --- Import the project code (robust fallbacks) ---
BusinessIdeaGenerator = None

# Preferred import (as documented in README)
try:
    from business_idea_analyzer import BusinessIdeaGenerator as _BIG
    BusinessIdeaGenerator = _BIG
except Exception:
    pass

# Fallback to direct modules in repo root
if BusinessIdeaGenerator is None:
    try:
        from business_generator import BusinessIdeaGenerator as _BIG
        BusinessIdeaGenerator = _BIG
    except Exception:
        pass

# Last-resort stub so the UI boots even if imports fail.
class _StubBIG:
    def __init__(self):
        pass

    def generate_ideas(self, industry: str = "", target_market: str = "", n:int=5) -> List[Dict[str, Any]]:
        base = [
            {"idea": f"{industry.title()} SaaS for {target_market} analytics", "rationale": "Pattern: industry + market pain points", "score": 0.62},
            {"idea": f"{industry.title()} marketplace for {target_market}", "rationale": "Two-sided network idea", "score": 0.57},
            {"idea": f"AI assistant for {target_market} in {industry}", "rationale": "Assistive productivity", "score": 0.55},
        ]
        return base[:max(1, n)]

    def assess_feasibility(self, idea: str, initial_investment: float = 0, target_roi: float = 0,
                           industry: str = "", target_market: str = "") -> Dict[str, Any]:
        # Naive scoring stub
        score = 0.5
        if "ai" in idea.lower(): score += 0.1
        if initial_investment and target_roi:
            cap_eff = min(1.0, (target_roi/100.0)) * 0.2
            score += cap_eff
        return {
            "idea": idea,
            "score": round(min(score, 0.95), 3),
            "market_outlook": "unknown",
            "risk_level": "medium",
            "sentiment": "neutral",
            "notes": "Stub mode (imports failed); wire your repo modules or set PYTHONPATH."
        }

# Instantiate
GeneratorCls = BusinessIdeaGenerator or _StubBIG
gen = GeneratorCls()

# --- Gradio callbacks ---
def ui_generate(industry: str, target_market: str, top_n: int):
    industry = (industry or "").strip()
    target_market = (target_market or "").strip()
    n = max(1, int(top_n or 5))
    try:
        # Try with n argument if supported
        ideas = gen.generate_ideas(industry=industry, target_market=target_market, n=n)
    except TypeError:
        # Fallback to just two args (per README example)
        ideas = gen.generate_ideas(industry=industry, target_market=target_market)
        # Normalize: ensure list[dict]
        if isinstance(ideas, dict):
            ideas = [ideas]
        ideas = ideas[:n]
    except Exception as e:
        raise gr.Error(f"Generation error: {e}")
    # Nice table
    rows = []
    for i, item in enumerate(ideas, 1):
        if isinstance(item, dict):
            idea = item.get("idea") or item.get("title") or str(item)
            score = item.get("score", "")
            rationale = item.get("rationale", "")
        else:
            idea, score, rationale = str(item), "", ""
        rows.append({"rank": i, "idea": idea, "score": score, "rationale": rationale})
    return rows

def ui_assess(idea: str, initial_investment: float, target_roi: float, industry: str, target_market: str):
    idea = (idea or "").strip()
    if not idea:
        raise gr.Error("Please enter an idea to assess.")
    try:
        result = gen.assess_feasibility(
            idea=idea,
            initial_investment=float(initial_investment or 0),
            target_roi=float(target_roi or 0),
            industry=(industry or "").strip(),
            target_market=(target_market or "").strip(),
        )
    except TypeError:
        # Graceful: some implementations may not accept all kwargs
        result = gen.assess_feasibility(
            idea=idea,
            initial_investment=float(initial_investment or 0),
            target_roi=float(target_roi or 0),
        )
    except Exception as e:
        raise gr.Error(f"Assessment error: {e}")

    # Keep both a pretty summary and raw JSON
    try:
        score = result.get("score", None)
        market = result.get("market_outlook", "—")
        risk = result.get("risk_level", "—")
        sent = result.get("sentiment", "—")
        summary = f"**Score:** {score}  \n**Market:** {market}  \n**Risk:** {risk}  \n**Sentiment:** {sent}"
    except Exception:
        summary = "See JSON output."
    return summary, result

def ui_batch(file_obj):
    if file_obj is None:
        raise gr.Error("Upload a CSV with columns: idea[, initial_investment, target_roi, industry, target_market]")
    import pandas as pd
    df = pd.read_csv(file_obj.name)
    # Flexible column detection
    cols = {c.lower(): c for c in df.columns}
    if "idea" not in cols:
        raise gr.Error("CSV must include a column named 'idea'. Optional: initial_investment,target_roi,industry,target_market.")
    rows = []
    for _, r in df.iterrows():
        idea = str(r[cols["idea"]])
        ii = float(r.get(cols.get("initial_investment",""), 0) or 0) if "initial_investment" in cols else 0.0
        roi = float(r.get(cols.get("target_roi",""), 0) or 0) if "target_roi" in cols else 0.0
        ind = str(r.get(cols.get("industry",""), "")) if "industry" in cols else ""
        tm = str(r.get(cols.get("target_market",""), "")) if "target_market" in cols else ""
        try:
            res = gen.assess_feasibility(idea=idea, initial_investment=ii, target_roi=roi, industry=ind, target_market=tm)
        except TypeError:
            res = gen.assess_feasibility(idea=idea, initial_investment=ii, target_roi=roi)
        except Exception as e:
            res = {"error": str(e)}
        flat = {"idea": idea, "initial_investment": ii, "target_roi": roi, "industry": ind, "target_market": tm}
        if isinstance(res, dict):
            for k,v in res.items():
                flat[f"out_{k}"] = v
        else:
            flat["out_result"] = str(res)
        rows.append(flat)
    out_df = pd.DataFrame(rows)
    out_path = "batch_assessment_results.csv"
    out_df.to_csv(out_path, index=False)
    return out_df, out_path

examples_generate = [
    ["technology", "small businesses", 5],
    ["healthcare", "millennials", 3],
    ["hospitality", "remote workers", 4],
]

examples_assess = [
    ["AI scheduling assistant for restaurants", 25000, 150, "hospitality", "SMBs"],
    ["Telehealth platform for rural clinics", 100000, 180, "healthcare", "rural patients"],
    ["Gamified budgeting app for Gen Z", 40000, 200, "fintech", "Gen Z"],
]

with gr.Blocks(title="Business Idea Analyzer & Generator", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 💡 Business Idea Analyzer & Generator\nGenerate ideas and assess feasibility. Works with your repo code if present; otherwise runs a lightweight stub.")
    with gr.Tab("Generate Ideas"):
        with gr.Row():
            industry = gr.Textbox(label="Industry", placeholder="e.g., technology")
            target_market = gr.Textbox(label="Target market", placeholder="e.g., small businesses")
            top_n = gr.Number(label="Ideas to return", value=5, precision=0)
        btn_g = gr.Button("Generate", variant="primary")
        ideas_table = gr.Dataframe(headers=["rank","idea","score","rationale"], label="Ideas")
        btn_g.click(ui_generate, inputs=[industry, target_market, top_n], outputs=ideas_table)
        gr.Examples(label="Try these", examples=examples_generate, inputs=[industry, target_market, top_n])

    with gr.Tab("Assess Idea"):
        idea_in = gr.Textbox(label="Idea", placeholder="Describe your business idea...", lines=3)
        with gr.Row():
            ii = gr.Number(label="Initial investment ($)", value=50000)
            roi = gr.Number(label="Target ROI (%)", value=200)
        with gr.Row():
            ind2 = gr.Textbox(label="Industry (optional)")
            tm2 = gr.Textbox(label="Target market (optional)")
        btn_a = gr.Button("Assess", variant="primary")
        summary = gr.Markdown()
        raw_json = gr.JSON(label="Raw assessment JSON")
        btn_a.click(ui_assess, inputs=[idea_in, ii, roi, ind2, tm2], outputs=[summary, raw_json])
        gr.Examples(label="Assessment examples", examples=examples_assess, inputs=[idea_in, ii, roi, ind2, tm2])

    with gr.Tab("Batch Assess (CSV)"):
        gr.Markdown("Upload a CSV with columns: **idea**[, initial_investment, target_roi, industry, target_market]")
        file_in = gr.File(label="Upload CSV")
        btn_b = gr.Button("Run batch")
        table_out = gr.Dataframe(label="Batch results")
        file_out = gr.File(label="Download CSV")
        btn_b.click(ui_batch, inputs=file_in, outputs=[table_out, file_out])

    gr.Markdown(
        "Tip: For live APIs (News/Finance/OpenAI), set env vars in `.env` or the Space settings. "
        "This demo gracefully falls back if imports/signatures differ."
    )

if __name__ == "__main__":
    demo.launch()
