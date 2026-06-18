import json
import os
from pathlib import Path

import streamlit as st
from openai import APIConnectionError, APIError, APITimeoutError, OpenAI


APP_DIR = Path(__file__).parent
KNOWLEDGE_BASE_PATH = APP_DIR / "prompt_knowledge_base.md"
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

CRITERIA = [
    "clarity",
    "specificity",
    "context",
    "structure",
    "output_format",
    "constraints",
    "examples",
]

TASK_TYPES = [
    "",
    "Content generation",
    "Marketing",
    "Sales",
    "Forecasting",
    "Research",
    "Competitive analysis",
    "Strategic planning",
    "Business operations",
    "Customer support",
    "Training or education",
    "Data analysis",
    "Software engineering",
    "Code review",
    "Debugging",
    "Policy or compliance",
    "Grant or proposal writing",
    "Healthcare or clinical admin",
    "Finance or budgeting",
    "Agent workflow",
    "General",
]


@st.cache_data
def load_knowledge_base() -> str:
    if not KNOWLEDGE_BASE_PATH.exists():
        return ""
    return KNOWLEDGE_BASE_PATH.read_text(encoding="utf-8")


def get_api_key() -> str | None:
    secret_key = None
    try:
        secret_key = st.secrets.get("OPENAI_API_KEY")
    except Exception:
        pass
    return secret_key or os.getenv("OPENAI_API_KEY")


def build_system_prompt(knowledge_base: str) -> str:
    return f"""You are the AI Alchemy Prompt Evaluator.

Use the evaluator guidance below as your source of truth. Score the submitted prompt, diagnose the missing prompt ingredients, generate three improved prompt options, and recommend the best one.

<prompt_knowledge_base>
{knowledge_base}
</prompt_knowledge_base>

Return ONLY valid JSON with this exact shape:
{{
  "overall": 0,
  "criteria": {{
    "clarity": {{"score": 0, "note": ""}},
    "specificity": {{"score": 0, "note": ""}},
    "context": {{"score": 0, "note": ""}},
    "structure": {{"score": 0, "note": ""}},
    "output_format": {{"score": 0, "note": ""}},
    "constraints": {{"score": 0, "note": ""}},
    "examples": {{"score": 0, "note": ""}}
  }},
  "diagnosis": {{
    "what_is_missing": [],
    "why_it_matters": "",
    "recommended_scaffold": "",
    "recommended_pattern": "",
    "risk_or_verification_needs": ""
  }},
  "needs": {{
    "role_persona": false,
    "scaffold": false,
    "delimiters": false,
    "output_format": false,
    "examples": false,
    "constraints": false,
    "verification": false,
    "fact_checking": false,
    "source_requirements": false,
    "reasoning_method": false,
    "software_engineering_review_pattern": false,
    "research_synthesis_pattern": false,
    "agent_workflow_guardrails": false
  }},
  "improved_prompts": {{
    "clean_rewrite": "",
    "structured_prompt": "",
    "advanced_prompt": ""
  }},
  "best_recommendation": {{
    "choice": "Clean Rewrite",
    "why": ""
  }}
}}

Rules:
- Scores must be 0-10 numbers.
- Overall should reflect the seven criteria and any serious verification risk.
- Clean Rewrite should be compact and preserve the user's intent.
- Structured Prompt should use the best scaffold from the knowledge base.
- Advanced Prompt should add verification, source, reasoning, research, software, or agent guardrails only when useful.
- Do not invent source citations. Recommend source requirements when facts need verification.
- All JSON string values must use \\n for newlines — never literal line breaks inside a string value.

Recommendation guidance — choose the SIMPLEST option that actually fixes the prompt's weaknesses:
- Recommend "Clean Rewrite" when the original prompt is already clear and specific, just needs tightening in plain language. This is the right choice for most conversational, creative, or simple task prompts.
- Recommend "Structured Prompt" only when the task is genuinely complex, multi-step, or benefits from explicit role/scaffold/format structure (e.g. analysis reports, code review, research briefs).
- Recommend "Advanced Prompt" only when the task involves fact-checking, multi-source research, agent workflows, or high-stakes verification where guardrails are necessary.
- Default to "Clean Rewrite" when in doubt. Avoid over-engineering simple prompts.
"""


def extract_json(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.removeprefix("json").strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON object found in model response.")
    raw = cleaned[start : end + 1]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        repaired = _repair_json_strings(raw)
        repaired = _strip_trailing_commas(repaired)
        try:
            return json.loads(repaired)
        except json.JSONDecodeError as e:
            pos = e.pos or 0
            snippet = repaired[max(0, pos - 200) : pos + 200]
            raise ValueError(
                f"Could not parse model response as JSON: {e}\n\n"
                f"--- AROUND ERROR (chars {max(0,pos-200)}–{pos+200}) ---\n{snippet}"
            )


def _repair_json_strings(s: str) -> str:
    """Replace literal newlines and tabs inside JSON string values only."""
    result = []
    in_string = False
    i = 0
    while i < len(s):
        ch = s[i]
        if in_string:
            if ch == "\\":
                result.append(ch)
                i += 1
                if i < len(s):
                    result.append(s[i])
            elif ch == '"':
                in_string = False
                result.append(ch)
            elif ch == "\n":
                result.append("\\n")
            elif ch == "\r":
                result.append("\\r")
            elif ch == "\t":
                result.append("\\t")
            else:
                result.append(ch)
        else:
            if ch == '"':
                in_string = True
            result.append(ch)
        i += 1
    return "".join(result)


def _strip_trailing_commas(s: str) -> str:
    """Remove trailing commas before } or ] — assumes string values already repaired."""
    import re
    return re.sub(r",\s*([}\]])", r"\1", s)


def evaluate_prompt(
    api_key: str,
    knowledge_base: str,
    prompt: str,
    goal: str,
    audience: str,
    task_type: str,
    context: str,
    constraints: str,
    output_format: str,
    verification: str,
) -> dict:
    client = OpenAI(api_key=api_key)
    user_payload = {
        "prompt": prompt,
        "optional_goal": goal,
        "optional_audience": audience,
        "optional_task_type": task_type,
        "optional_context": context,
        "optional_constraints": constraints,
        "optional_output_format": output_format,
        "optional_verification_reflection_factcheck": verification,
    }
    response = client.responses.create(
        model=MODEL,
        max_output_tokens=3500,
        temperature=0.2,
        text={"format": {"type": "json_object"}},
        instructions=build_system_prompt(knowledge_base),
        input="Evaluate this prompt submission and respond with valid JSON:\n"
        f"<submission>{json.dumps(user_payload, ensure_ascii=False)}</submission>",
    )
    raw = response.output_text
    return extract_json(raw)


def connection_error_message(exc: Exception) -> str:
    if isinstance(exc, APITimeoutError):
        return (
            "The evaluation took too long to complete. Try again in a moment, or shorten the prompt slightly."
        )
    if isinstance(exc, APIConnectionError):
        return (
            "The evaluator could not connect to the AI service. Please check that your API key is set, "
            "then restart the app and try again."
        )
    if isinstance(exc, APIError):
        return f"The evaluator received an AI service error: {exc}"
    return f"Evaluation failed: {exc}"


def render_score(value: float) -> None:
    st.metric("Overall score", f"{value:.1f} / 10")
    st.progress(max(0, min(100, int(round(value * 10)))))


def render_criteria(criteria: dict) -> None:
    st.subheader("Scores")
    for name in CRITERIA:
        item = criteria.get(name, {})
        score = float(item.get("score", 0) or 0)
        note = item.get("note", "")
        st.write(f"**{name.replace('_', ' ').title()}**: {score:.1f}/10")
        st.progress(max(0, min(100, int(round(score * 10)))))
        if note:
            st.caption(note)


def render_diagnosis(result: dict) -> None:
    diagnosis = result.get("diagnosis", {})
    st.subheader("Coaching diagnosis")
    missing = diagnosis.get("what_is_missing") or []
    if missing:
        st.write("**What is missing:**")
        for item in missing:
            st.write(f"- {item}")
    st.write(f"**Why it matters:** {diagnosis.get('why_it_matters', '')}")
    st.write(f"**Recommended scaffold:** {diagnosis.get('recommended_scaffold', '')}")
    st.write(f"**Recommended pattern:** {diagnosis.get('recommended_pattern', '')}")
    st.write(
        f"**Risk or verification needs:** {diagnosis.get('risk_or_verification_needs', '')}"
    )

    needs = result.get("needs", {})
    active_needs = [
        key.replace("_", " ")
        for key, value in needs.items()
        if isinstance(value, bool) and value
    ]
    if active_needs:
        st.write("**Evaluator flags:** " + ", ".join(active_needs))


def render_rewrites(result: dict) -> None:
    rewrites = result.get("improved_prompts", {})
    st.subheader("Improved prompt options")
    labels = [
        ("Clean Rewrite", "clean_rewrite"),
        ("Structured Prompt", "structured_prompt"),
        ("Advanced Prompt", "advanced_prompt"),
    ]
    tabs = st.tabs([label for label, _ in labels])
    for tab, (label, key) in zip(tabs, labels):
        with tab:
            st.text_area(label, rewrites.get(key, ""), height=300, key=key)

    recommendation = result.get("best_recommendation", {})
    st.subheader("Best recommendation")
    st.success(
        f"Use **{recommendation.get('choice', 'Clean Rewrite')}**. "
        f"{recommendation.get('why', '')}"
    )


def main() -> None:
    st.set_page_config(page_title="AI Alchemy Prompt Evaluator")
    st.title("AI Alchemy Prompt Evaluator")
    st.caption("Score, diagnose, and strengthen prompts with the AI Alchemy evaluation framework.")

    knowledge_base = load_knowledge_base()
    if not knowledge_base:
        st.error("Missing prompt_knowledge_base.md. Run Phase 1 document ingestion first.")
        st.stop()

    if "evaluation_result" not in st.session_state:
        st.session_state.evaluation_result = None

    def clear_inputs() -> None:
        for key in [
            "prompt_to_evaluate",
            "goal",
            "target_reader",
            "task_type",
            "context",
            "constraints",
            "output_format",
            "verification",
        ]:
            if key in st.session_state:
                st.session_state[key] = "" if key != "task_type" else TASK_TYPES[0]
        st.session_state.evaluation_result = None

    prompt = st.text_area(
        "Prompt to evaluate",
        height=220,
        max_chars=8000,
        key="prompt_to_evaluate",
    )
    actions = st.columns([1, 4])
    with actions[0]:
        st.button("Clear prompt", on_click=clear_inputs, use_container_width=True)

    goal = st.text_input("Goal (optional)", key="goal")
    audience = st.text_area(
        "Audience (optional)",
        height=70,
        placeholder="Example: small business owners, sales team, executive audience",
        key="target_reader",
    )
    task_type = st.selectbox(
        "Task type (optional)",
        TASK_TYPES,
        key="task_type",
    )
    context = st.text_area(
        "Context (optional)",
        height=110,
        placeholder="Background, source material, business situation, assumptions, or details the evaluator should preserve.",
        key="context",
    )
    constraints = st.text_area(
        "Constraints (optional)",
        height=90,
        placeholder="Length limits, tone rules, exclusions, must-include items, compliance needs, tools, or boundaries.",
        key="constraints",
    )
    output_format = st.text_area(
        "Output format (optional)",
        height=90,
        placeholder="Example: table, checklist, JSON, memo, campaign brief, rubric, code review, forecast summary.",
        key="output_format",
    )
    verification = st.text_area(
        "Verification / reflection / fact-checking (optional)",
        height=100,
        placeholder="Example: cite sources, flag uncertainty, check assumptions, reflect against a rubric, verify claims before final answer.",
        key="verification",
    )

    submitted = st.button("Evaluate prompt", type="primary")
    if not submitted:
        if st.session_state.evaluation_result:
            result = st.session_state.evaluation_result
            render_score(float(result.get("overall", 0) or 0))
            render_criteria(result.get("criteria", {}))
            render_diagnosis(result)
            render_rewrites(result)
        return

    if not prompt.strip():
        st.warning("Please enter a prompt to evaluate.")
        return

    api_key = get_api_key()
    if not api_key:
        st.error(
            "The evaluator is not connected yet. Add your API key, restart the app, and try again."
        )
        return

    with st.spinner("Evaluating prompt..."):
        try:
            result = evaluate_prompt(
                api_key,
                knowledge_base,
                prompt,
                goal,
                audience,
                task_type,
                context,
                constraints,
                output_format,
                verification,
            )
        except Exception as exc:
            st.error(connection_error_message(exc))
            return

    st.session_state.evaluation_result = result
    render_score(float(result.get("overall", 0) or 0))
    render_criteria(result.get("criteria", {}))
    render_diagnosis(result)
    render_rewrites(result)


if __name__ == "__main__":
    main()
