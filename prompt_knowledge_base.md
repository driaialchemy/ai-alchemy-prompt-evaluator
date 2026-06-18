# AI Alchemy Prompt Evaluator Knowledge Base

Generated on 2026-06-17T17:00:11-07:00. This file is the compressed evaluator-ready reference created from the six source documents listed in `prompt_reference_manifest.json`. After this file exists, app logic should use this file rather than rereading the original source documents unless the user explicitly asks or the source files change.

## AI Alchemy Scoring Philosophy

AI Alchemy evaluates prompts by asking whether the prompt gives an AI system enough intent, context, structure, and guardrails to produce a useful, verifiable answer. High scores reward prompts that are clear, specific, scoped, audience-aware, format-aware, constraint-aware, and testable. Low scores identify missing ingredients that cause vague, generic, hallucinated, poorly formatted, or unverifiable output.

The evaluator should coach, not merely grade. A score should explain what is missing, why it matters, and which prompt pattern will most improve the result. The rewrite should preserve the user's intent while adding only the structure needed for the task.

## Seven Base Scoring Criteria

Score each criterion from 0 to 10.

| Criterion | Strong prompt behavior | Common weakness |
|---|---|---|
| clarity | Intent and desired action are unambiguous. | Vague verbs such as help, improve, analyze, or explain without a target outcome. |
| specificity | Includes concrete subject, scope, inputs, details, success criteria, and boundaries. | Broad request with no depth, audience, length, domain, assumptions, or constraints. |
| context | Provides background, user goal, audience, source material, scenario, and relevant facts. | The model must infer purpose, audience, or domain. |
| structure | Uses sections, ordered steps, scaffold, role/task/context/output layout, or other logical organization. | A one-line request for a complex task. |
| output_format | Names the desired deliverable: bullets, table, JSON, checklist, plan, code, rubric, memo, etc. | No format guidance, causing variable or hard-to-use output. |
| constraints | Defines limits, exclusions, style rules, source requirements, length, tools, assumptions, or must/avoid rules. | Missing guardrails, causing overreach, invented facts, or unusable scope. |
| examples | Supplies examples, sample input/output, tone samples, edge cases, or says examples are unnecessary for simple tasks. | No examples for style-sensitive, transformation, coding, data, or compliance tasks. |

Overall score should be the average of the seven criteria, adjusted slightly downward for serious hallucination risk, missing source requirements, or safety/verification gaps in high-stakes work.

## Prompt Scaffolds and When to Use Them

- RACE: Role, Action, Context, Expectation. Use for general business, writing, coaching, analysis, and strategy prompts that need a persona plus deliverable.
- COSTAR: Context, Objective, Style, Tone, Audience, Response. Use when voice, brand, audience, and response shape matter.
- STAR: Situation, Task, Action, Result. Use for behavioral examples, case studies, reflective summaries, resume/interview prompts, and performance narratives.
- ABCDE: Audience, Background, Constraints, Deliverable, Evaluation. Use for teaching, consulting, decision support, and prompts where success criteria matter.
- Altman style prompting: Goal, return format, warnings/constraints, context dump, step-by-step process, and quality bar. Use for high-precision outputs and advanced transformations.
- RISE: Role, Input, Steps, Expectation. Use for workflows where the model must transform user-provided material through an explicit method.
- ROSES: Role, Objective, Scenario, Expected solution, Steps. Use for problem-solving, planning, and advisory prompts needing context and an ordered path.
- Few-shot / example-based: Use when tone, style, classification, extraction, transformation, or edge cases are important.
- Chain-of-verification / reflection: Ask the model to check assumptions, cite uncertainty, validate claims, and identify missing information before finalizing.
- Socratic or flipped interaction: Ask the model to interview the user first when inputs are incomplete, stakes are high, or the task requires personalization.
- Tree-of-thought / alternative generation: Use for strategy, naming, planning, diagnosis, or design tasks where comparing options improves quality.

## Dr. White / Vanderbilt Prompt Patterns

Use Dr. Jules White / Vanderbilt-style patterns as advanced coaching recommendations when the prompt would benefit from a reusable interaction pattern:

- Persona pattern: Ask the model to act as a specific expert with relevant responsibilities and limits.
- Question refinement pattern: Ask the model to suggest a better version of the user's question before answering.
- Cognitive verifier pattern: Ask the model to break a complex question into subquestions, answer them, then synthesize.
- Audience persona pattern: Tailor output for a defined reader's knowledge, needs, and constraints.
- Flipped interaction pattern: The model asks targeted questions until enough information is available.
- Template pattern: Require output in a reusable structure or fill-in format.
- Fact-check list pattern: Require claims, evidence/source status, uncertainty, and verification steps.
- Reflection pattern: Ask the model to critique its answer against a rubric and revise.
- Alternative approaches pattern: Generate multiple approaches and compare tradeoffs.
- Context manager pattern: Tell the model what context to keep, ignore, summarize, or request.

## Systematic Prompting Techniques

- State the task type and success criteria.
- Separate instructions from source text using clear delimiters.
- Provide enough context but avoid irrelevant context stuffing.
- Ask for assumptions and unknowns when inputs are incomplete.
- Use stepwise workflows for analysis, research, code review, planning, and troubleshooting.
- Require evidence, citations, or source-grounding when factual accuracy matters.
- Add self-checks for completeness, contradiction, format compliance, and risk.
- Specify whether the model should ask clarifying questions or proceed with reasonable assumptions.
- For high-stakes domains, require verification, uncertainty labeling, and no invented sources.

## GEM Research Prompting Methods

For research prompts, recommend a research synthesis pattern:

1. Define the research question and decision the research supports.
2. Set scope: timeframe, geography, population, domain, inclusion/exclusion criteria.
3. Require source standards: primary sources, peer-reviewed literature, official docs, reputable reporting, or provided documents.
4. Ask for extraction: key claims, evidence, methods, limitations, and confidence.
5. Ask for synthesis: themes, disagreements, gaps, implications, and recommended next research.
6. Require citations or source list and distinguish evidence from inference.
7. Include verification needs and warnings about uncertain or changing facts.

## Software Engineering Prompt Patterns

For coding and engineering prompts, recommend a software engineering review pattern:

- State repository/module context, language/framework, runtime, and constraints.
- Provide exact error messages, failing tests, logs, reproduction steps, and expected behavior.
- Ask for minimal, scoped changes that follow existing patterns.
- Require tests or verification commands.
- For code review, prioritize bugs, regressions, security, performance, edge cases, and missing tests before style.
- For implementation, ask for plan, file changes, code edits, and test results.
- For debugging, ask for hypothesis list, inspection steps, root cause, fix, and regression coverage.
- For agent workflows, require guardrails: do not delete unrelated files, preserve existing behavior, check git diff, and report verification.

## Delimiter Guidance

Use delimiters when the prompt includes source material, data, examples, policies, code, logs, or nested instructions. Recommended delimiter styles:

- Triple backticks for code, logs, or literal text.
- XML-like tags such as `<context>`, `<source>`, `<task>`, `<constraints>`, `<output_format>` for complex prompts.
- Markdown headings for human-readable sections.
- JSON only when machine parsing is required.

Delimiter rules: explain what each delimited block is, tell the model whether to treat text inside as data rather than instructions, and keep output instructions outside source delimiters.

## Prompt Failure Modes

- Vague objective: the model cannot tell what success looks like.
- Missing audience: tone, depth, and terminology drift.
- Missing context: generic answer or wrong assumptions.
- Missing output format: useful content arrives in an unusable shape.
- Missing constraints: output is too long, too broad, noncompliant, or off-brand.
- Missing examples: style-sensitive tasks fail to match expected pattern.
- No source requirements: factual tasks may hallucinate or omit evidence.
- No verification: high-stakes or research prompts may overstate certainty.
- Instruction/source confusion: untrusted text can override the task without delimiters.
- Overloaded prompt: too many goals without priority or workflow.
- Hidden task type: code, research, strategy, writing, and tutoring need different scaffolds.

## Recommendation Rules

Recommend Clean Rewrite when:

- The user has a simple task with mostly clear intent.
- The main issues are wording, directness, and light context.
- A compact prompt is likely sufficient.

Recommend Structured Prompt when:

- The task has multiple requirements, audience needs, constraints, or deliverable sections.
- The prompt needs a scaffold such as RACE, COSTAR, ABCDE, RISE, or ROSES.
- The user benefits from reusable sections and clear output format.

Recommend Advanced Prompt when:

- The task involves research, software engineering, strategy, high-stakes accuracy, multi-step reasoning, agent workflows, or source-grounded synthesis.
- It needs verification, assumptions, citations, examples, edge cases, or guardrails.
- The risk of hallucination, incomplete work, or wrong assumptions is meaningful.

## Evaluator Decision Checklist

When evaluating a submitted prompt, determine whether it needs:

- role/persona: if expertise, tone, or audience adaptation matters.
- scaffold: if the task has more than one moving part.
- delimiters: if source text, examples, code, logs, or external material are included.
- output format: almost always, unless the task is conversational.
- examples: for style, extraction, classification, transformation, code, and edge cases.
- constraints: for length, scope, assumptions, exclusions, tools, tone, or compliance.
- verification: for factual, research, legal, medical, financial, technical, or high-impact tasks.
- fact checking/source requirements: for claims about the world, recent information, or research.
- reasoning method: for analysis, diagnosis, tradeoffs, planning, or comparison.
- software engineering review pattern: for code, repos, tests, PRs, debugging, architecture, or deployment.
- research synthesis pattern: for literature, market, policy, technical research, or document synthesis.
- agent workflow guardrails: for autonomous coding, file edits, deployment, data changes, or multi-step tool use.

## Source Extraction Notes

### AI_Alchemy_Prompt_Library.docx

Processed: True  
Extracted characters: 24399

Key extracted guidance lines:
- AI Alchemy Prompt Library
- Consolidated Frameworks, Prompt Patterns, Reasoning Methods, Research Prompts, and Software Engineering Patterns
- Purpose: This library consolidates the stored AI Alchemy prompting assets into one working reference. It is designed for prompt design, agent instruction, research synthesis, lesson planning, code review, and strategic consulting work.
- Choose a scaffold first when the task needs structure, audience fit, or delivery constraints.
- Choose one or more prompt patterns when the task needs a repeatable behavior such as verification, persona, synthesis, critique, or output automation.
- Choose a reasoning method when the task depends on analysis, judgment, uncertainty management, or decision quality.
- Choose a systematic or GEM research technique when the task is complex, research-heavy, multi-step, or agentic.
- Choose a software engineering pattern when directing a coding agent, evaluating repositories, debugging, testing, or designing development workflows.
- Prompt Selection Guide
- I. Prompt Scaffolding Frameworks
- II. Dr. Michael Seller / Dr. White Prompt Pattern Catalog
- Catalog note: This section combines the core Dr. White prompt patterns with the additional Vanderbilt-style and action-oriented patterns stored for AI Alchemy use.
- A. Core Dr. White Patterns
- B. Additional Stored Prompt Patterns
- III. Systematic Prompting Techniques
- Use case: Use these techniques when the task requires method selection, reliable reasoning, tool use, verification, or research-grade synthesis.
- IV. GEM Research Prompts
- Use case: Use these for advanced prompt research, newer reasoning architectures, multi-agent workflows, adaptive prompting, and complex task decomposition.

### gemresearchprompts.pdf

Processed: True  
Extracted characters: 11599

Key extracted guidance lines:
- 1. End-to-End DAG-Path (EEDP) Prompting
- the entire process from initial prompt to ﬁnal answer as a single, end-to-end
- 2. Buffer of Thoughts (BoT) Prompting
- within the prompt's context. This buffer is used to store key information,
- intermediate conclusions, or context that needs to be referenced across multiple
- steps of a complex task. For example, in a multi-step story writing task, the buffer
- might store character states or key plot points, and the prompt would instruct the
- 3. Reverse Chain-of-Thought (R-CoT) Prompting
- • Familiarity: This is a known, though less common, research concept.
- mathematical proofs where you start with what you want to prove and work
- 4. Contrastive Denoising with Noisy CoT (CD-CoT) Prompting
- • What it does: This is less of a direct prompting technique and more of a training
- multiple Chain-of-Thought examples, some of which are intentionally corrupted
- 5. Local Prompt Optimization (LPO) Prompting
- • Familiarity: This is a conceptual subset of the broader ﬁeld of automatic prompt
- • What it does: LPO focuses on optimizing speciﬁc parts of a large, complex prompt
- rather than rewriting the entire thing. For instance, in a multi-part prompt, LPO might
- iteratively test variations of only the "output formatting" section or the "persona"

### drwhite.pdf

Processed: True  
Extracted characters: 107906

Key extracted guidance lines:
- A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT
- Jules White, Quchen Fu, Sam Hays, Michael Sandborn, Carlos O lea, Henry Gilbert,
- {jules.white, quchen.fu, george.s.hays, michael.sandbor n, carlos.olea, henry.gilbert,
- ashraf.elnashar, jesse.spencer-smith, douglas.c.schmi dt}@vanderbilt.edu
- Abstract—Prompt engineering is an increasingly important
- (LLMs), such as ChatGPT. Prompts are instructions given to a n
- qualities (and quantities) of generated output. Prompts ar e also
- This paper describes a catalog of prompt engineering tech-
- niques presented in pattern form that have been applied to so lve
- common problems when conversing with LLMs. Prompt patterns
- are a knowledge transfer method analogous to software patte rns
- in a particular context, i.e., output generation and intera ction
- prompt engineering that apply LLMs to automate software de-
- velopment tasks. First, it provides a framework for documen ting
- patterns for structuring prompts to solve a range of problem s
- presents a catalog of patterns that have been applied succes sfully
- how prompts can be built from multiple patterns and illustra tes
- prompt patterns that beneﬁt from combination with other pro mpt

### softwareengineeringprompts.pdf

Processed: True  
Extracted characters: 32754

Key extracted guidance lines:
- handle ambiguous user instructions. However, effective prompt patterns remain
- prompt engineering patterns for software engineering. It is based on a systematic
- significant limitations in context length and inference capabilities. Our study
- the ongoing importance of well-designed prompts in optimizing task performance.
- Our findings highlight the critical role of prompt patterns in maximizing LLM’s
- ware engineering by integrating large language
- application of these approaches, the domain of prompt
- engineering, i.e., the practice of tailoring inputs to di-
- Software engineering translates human expertise
- into machine-readable formats, with prompt engi-
- ture,6 patterns have been widely adopted in software
- engineering and now extend to generative AI. 7 Given
- the field’s variability, abstract patterns offer adaptable
- Although the potential of LLMs in software engi-
- neering is being explored,8 systematic assessments of
- how to effectively employ prompt engineering across
- diverse software engineering contexts are scant. Exist-
- dated knowledge of prompt strategies and their impli-

### systematicsurveyprompts.pdf

Processed: True  
Extracted characters: 47918

Key extracted guidance lines:
- A Systematic Survey of Prompt Engineering in Large Language Models:
- 1Department of Computer Science And Engineering, Indian Institute of Technology Patna
- Prompt engineering has emerged as an indispens-
- instructions, known as prompts, to enhance model
- prompts allow seamless integration of pre-trained
- model behaviors solely based on the given prompt.
- Prompts can be natural language instructions that
- provide context to guide the model or learned vec-
- lack of systematic organization and understanding
- of the diverse prompt engineering methods and tech-
- in prompt engineering, categorized by application
- area. For each prompting approach, we provide a
- summary detailing the prompting methodology, its
- critical points of each prompting technique. This
- systematic analysis enables a better understanding
- ture research by illuminating open challenges and
- opportunities for prompt engineering.
- Prompt engineering has emerged as a crucial technique for

### claudesummaryprompt_engineering_reference.docx

Processed: True  
Extracted characters: 5275

Key extracted guidance lines:
- PROMPT ENGINEERING
- Personal Reference — Patterns · Scaffolds · Delimiters
- You are not activating hidden modes. Structured prompting shapes the model's attention, task interpretation, output structure, and reasoning path — reducing ambiguity so it follows your intent.
- The model predicts the next token based on context. Clear labels, roles, criteria, and format requirements bias it toward tokens associated with expert, focused responses.
- It is not opening a 'software engineering module.' It is being steered toward learned patterns from training examples that match the structure you supplied.
- 2. Patterns — How to Think
- Patterns tell the model what kind of thinking process and output behavior to use. Without them, the model may explain shallowly instead of reasoning deeply.
- Common Patterns
- Scaffolds give the model a workflow, helping it distinguish goal, role, source material, audience, constraints, output format, and evaluation criteria — things an unstructured prompt typically blurs together.
- Structured Prompt Anatomy
- 4. Delimiters — What Each Part Means
- Delimiters help the model separate instructions from content. Critical when providing source documents, code, emails, notes, transcripts, or competing drafts — anything where pasted content could be misread as a new instruction.
- Why It Matters — Injection Example
- The delimiters help the model treat that internal sentence as content to analyze, not a command to obey. Not magic security — but improves instruction hierarchy and reduces confusion.
- 6. What Structured Prompting Improves
- Depth — patterns encourage inspection of more dimensions
- Control — constraints reduce rambling
- Safety — delimiters reduce accidental instruction confusion

