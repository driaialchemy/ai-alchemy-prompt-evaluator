# AI Alchemy Prompt Evaluator

A serverless web app for AI Alchemy (aialchemydr.com) that scores and rewrites AI prompts using a 7-criterion rubric. Built for Cloudflare Pages with a protected backend function.

---

## Live URL

**https://ai-alchemy-prompt-evaluator.pages.dev**

The site is deployed and live. The link to aialchemydr.com has been intentionally deferred — add it when ready.

---

## Repository

- **GitHub:** `https://github.com/driaialchemy/ai-alchemy-prompt-evaluator` (private)
- **Branch:** `main`
- **Auto-deploy:** Cloudflare Pages is connected to this repo. Every push to `main` triggers a new deployment.

---

## Project Structure

```
/
├── dist/
│   └── index.html          # Full frontend (self-contained, no build step)
├── functions/
│   └── evaluate.js         # Cloudflare Pages Function (serverless backend)
└── README.md
```

**Important:** `functions/` must stay at the repo root, not inside `dist/`. Cloudflare Pages resolves serverless functions from the repo root, not from the build output directory.

---

## How It Works

1. User pastes a prompt (up to 8,000 chars) and optional goal into the frontend
2. Frontend POSTs `{ prompt, goal }` to `/evaluate`
3. `functions/evaluate.js` runs server-side on Cloudflare's edge — it reads `ANTHROPIC_API_KEY` from environment and calls the Anthropic API
4. The API returns a JSON evaluation; the frontend renders the score ring, per-criterion bars, and an improved prompt

---

## Backend Function — `functions/evaluate.js`

- **Route:** `POST /evaluate`
- **Handler export:** `onRequestPost({ request, env })`
- **Model:** `claude-haiku-4-5` via `https://api.anthropic.com/v1/messages`
- **Max tokens:** 2000
- **API key:** read from `env.ANTHROPIC_API_KEY` — never hardcoded, never in any client file

### Evaluation rubric (7 criteria, scored 0–10 each)

| Criterion | Notes |
|-----------|-------|
| clarity | Is the intent unambiguous? |
| specificity | How precise/detailed is the instruction? |
| context | Is enough background provided? |
| structure | Is the prompt logically organized? |
| output_format | Is the desired output format specified? |
| constraints | Are limits/rules stated? |
| examples | Are examples included (or are they unnecessary)? |

### Response shape (JSON)

```json
{
  "overall": 7.4,
  "verdict": "One-sentence summary.",
  "criteria": {
    "clarity":       { "score": 8, "note": "..." },
    "specificity":   { "score": 6, "note": "..." },
    "context":       { "score": 7, "note": "..." },
    "structure":     { "score": 8, "note": "..." },
    "output_format": { "score": 7, "note": "..." },
    "constraints":   { "score": 6, "note": "..." },
    "examples":      { "score": 9, "note": "..." }
  },
  "improved_prompt": "Full rewritten prompt..."
}
```

---

## Frontend — `dist/index.html`

Self-contained single file. No npm, no bundler, no external JS/CSS dependencies.

| Feature | Detail |
|---------|--------|
| Prompt input | 8,000 char cap with live counter |
| Goal field | Optional context for targeted feedback |
| Score ring | Animated SVG — green ≥8, amber ≥5, red <5 |
| Criterion bars | Per-criterion score bars with notes |
| Improved prompt | Full rewrite with copy button |
| History | Last 20 evaluations stored in `localStorage` |
| Keyboard shortcut | `Ctrl/Cmd + Enter` to submit |

### Brand / Colors

| Token | Value |
|-------|-------|
| Primary purple dark | `#352a59` |
| Primary purple | `#4b3a7a` |
| Gold accent | `#c9a14a` |
| Background | `#faf8f3` |
| Body font | Segoe UI |
| Heading font | Georgia |

---

## Cloudflare Pages Configuration

| Setting | Value |
|---------|-------|
| Account ID | `3e005734f01c4c000bd9331751e99c8b` |
| Project name | `ai-alchemy-prompt-evaluator` |
| Build output directory | `dist` |
| Build command | *(none — plain HTML, no build step)* |
| Production branch | `main` |
| GitHub repo | `driaialchemy/ai-alchemy-prompt-evaluator` |

### Environment Variables (Cloudflare Pages → Settings → Variables and secrets)

| Variable | Value |
|----------|-------|
| `ANTHROPIC_API_KEY` | Set — do not expose or log |

To update the key: Cloudflare Dashboard → Workers & Pages → ai-alchemy-prompt-evaluator → Settings → Variables and secrets.

---

## Local Preview

```powershell
cd "C:\Users\msell\OneDrive\AIAlchemy\promptevaluator"
npx serve dist -l 3333
```

Then open `http://localhost:3333`. The backend function won't run locally without wrangler, so `/evaluate` calls will fail — use the live site for end-to-end testing.

---

## Local Streamlit App

This repository also includes a local Streamlit version of the AI Alchemy Prompt Evaluator.

The Streamlit app uses:

- `app.py` for the local UI and evaluator workflow
- `prompt_knowledge_base.md` as the compressed prompt-engineering reference
- `prompt_reference_manifest.json` as the one-time ingestion record
- `OPENAI_API_KEY` from the environment or Streamlit secrets

The original reference documents were ingested once into `prompt_knowledge_base.md`. Do not reread the original source documents unless they change or a new ingestion pass is intentionally requested.

### Run Streamlit locally

```powershell
cd "C:\Users\msell\OneDrive\AIAlchemy\promptevaluator"
pip install -r requirements.txt
$env:OPENAI_API_KEY="your_key_here"
streamlit run app.py
```

Alternatively, create `.streamlit/secrets.toml` locally:

```toml
OPENAI_API_KEY = "your_key_here"
```

The Streamlit app accepts:

- Prompt
- Optional goal
- Optional audience
- Optional task type
- Optional context
- Optional constraints
- Optional output format
- Optional verification, reflection, or fact-checking instructions

It returns:

- Overall score
- Scores for clarity, specificity, context, structure, output format, constraints, and examples
- Coaching diagnosis
- Clean Rewrite, Structured Prompt, and Advanced Prompt versions
- A best recommendation explaining which version to use

### Model & API call

- **Model:** `gpt-4.1-mini` (override with `OPENAI_MODEL` env var)
- Uses the OpenAI **Responses API** (`client.responses.create`)
- Output is forced to valid JSON via `text={"format": {"type": "json_object"}}`. The input string contains the word "json" because the Responses API requires it when using `json_object` format.

### Recommendation logic

The system prompt instructs the model to **choose the simplest option that fixes the prompt's weaknesses**, and to default to **Clean Rewrite** when in doubt:

- **Clean Rewrite** — already-clear prompts that just need tightening (most conversational/creative/simple prompts)
- **Structured Prompt** — genuinely complex, multi-step tasks that benefit from explicit role/scaffold/format
- **Advanced Prompt** — fact-checking, multi-source research, agent workflows, or high-stakes verification

This replaced the earlier behavior where the model nearly always defaulted to Structured Prompt.

### JSON parsing robustness

`extract_json()` parses the model response with `json.loads()`. If that fails, it applies two repairs as a fallback before re-parsing:

1. `_repair_json_strings()` — escapes literal newlines/tabs that appear inside string values (string-aware; does not touch structure between fields)
2. `_strip_trailing_commas()` — removes trailing commas before `}` or `]`

With `json_object` format now enforced at the API level, these repairs are rarely needed but remain as a safety net. On total failure the error message includes a 400-char window around the parse error for debugging.

### Notes

- The "Evaluate prompt" button is always active; empty-prompt validation happens on click (shows a warning rather than disabling the button).
- The Streamlit app uses `OPENAI_API_KEY` (OpenAI), distinct from the Cloudflare Pages app which uses `ANTHROPIC_API_KEY` (Anthropic). They are two separate evaluator implementations in this repo.

---

## Deploying Changes

```powershell
cd "C:\Users\msell\OneDrive\AIAlchemy\promptevaluator"
git add -A
git commit -m "your message"
git push origin main
```

Cloudflare Pages auto-deploys within ~60 seconds. Monitor at:
`https://dash.cloudflare.com/3e005734f01c4c000bd9331751e99c8b/pages/view/ai-alchemy-prompt-evaluator`

---

## Pending Tasks

- [ ] Add a button/link on **aialchemydr.com** pointing to `https://ai-alchemy-prompt-evaluator.pages.dev` (intentionally deferred by user)
- [ ] Optionally change the env var type from Plaintext to Secret in the Cloudflare dashboard for better security hygiene

---

## Security Notes

- `ANTHROPIC_API_KEY` is accessed **only** in `functions/evaluate.js` via `env.ANTHROPIC_API_KEY`
- It must **never** appear in `dist/index.html` or any file served to the browser
- All 11 repos under the `driaialchemy` GitHub account have been set to **private**
