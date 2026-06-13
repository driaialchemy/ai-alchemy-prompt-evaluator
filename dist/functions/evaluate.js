export async function onRequestPost({ request, env }) {
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: "Invalid JSON body" }, 400);
  }

  const { prompt, goal } = body ?? {};

  if (!prompt || typeof prompt !== "string" || prompt.trim().length === 0) {
    return json({ error: "prompt is required" }, 400);
  }
  if (prompt.length > 8000) {
    return json({ error: "prompt exceeds 8000 character limit" }, 400);
  }

  const apiKey = env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    return json({ error: "Server misconfiguration: missing API key" }, 500);
  }

  const goalLine = goal && goal.trim()
    ? `The user's stated goal for this prompt: ${goal.trim()}\n\n`
    : "";

  const systemPrompt = `You are an expert prompt engineer at AI Alchemy. Evaluate the user's prompt below against best practices, then rewrite it as an improved version.

${goalLine}Score each criterion from 0 to 10:
clarity, specificity, context, structure, output_format, constraints, examples.
For "examples": if examples would not help this prompt, score 8-10 and note that examples are unnecessary here.

Respond with ONLY valid JSON, no markdown fences, exactly this shape:
{"overall":<0-10>,"verdict":"<one sentence>","criteria":{"clarity":{"score":<n>,"note":"<short>"},"specificity":{"score":<n>,"note":"<short>"},"context":{"score":<n>,"note":"<short>"},"structure":{"score":<n>,"note":"<short>"},"output_format":{"score":<n>,"note":"<short>"},"constraints":{"score":<n>,"note":"<short>"},"examples":{"score":<n>,"note":"<short>"}},"improved_prompt":"<full rewrite>"}`;

  const userMessage = `THE PROMPT TO EVALUATE:\n<<<\n${prompt}\n>>>`;

  let apiRes;
  try {
    apiRes = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": apiKey,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: "claude-haiku-4-5",
        max_tokens: 2000,
        system: systemPrompt,
        messages: [{ role: "user", content: userMessage }],
      }),
    });
  } catch (err) {
    return json({ error: "Failed to reach Anthropic API: " + err.message }, 502);
  }

  if (!apiRes.ok) {
    const errText = await apiRes.text().catch(() => "");
    return json({ error: `Anthropic API error ${apiRes.status}: ${errText}` }, 502);
  }

  const apiData = await apiRes.json();
  let raw = apiData?.content?.[0]?.text ?? "";

  // Strip accidental code fences
  raw = raw.replace(/^```[a-z]*\n?/i, "").replace(/\n?```$/i, "").trim();

  let result;
  try {
    result = JSON.parse(raw);
  } catch {
    return json({ error: "Model returned invalid JSON", raw }, 502);
  }

  return json(result, 200);
}

function json(data, status) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}
