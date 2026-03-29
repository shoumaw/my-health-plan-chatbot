import json
import logging
import os

from groq import Groq

from .prompts import TOOL_CALLING_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

MAX_SBC_CHARS = 15_000
GROQ_MODEL = "llama-3.3-70b-versatile"


def get_ai_response(
    *,
    enrolled_plans: list[dict],
    user_message: str,
    history: list | None = None,
) -> str:
    """
    Send a user message to Groq with full conversation history and tool calling.
    enrolled_plans is a list of dicts with keys: name, sbc_text (str or None).
    The model calls get_plan_details on demand — once per plan if comparing multiple.
    Raises groq.APIError subclasses on API failures.
    """
    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    plan_names = [p["name"] for p in enrolled_plans]
    plans_by_name = {p["name"]: p for p in enrolled_plans}

    system_prompt = TOOL_CALLING_SYSTEM_PROMPT.format(plan_names=", ".join(plan_names))

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_plan_details",
                "description": "Retrieve the benefits and coverage details for a specific enrolled plan.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "plan_name": {
                            "type": "string",
                            "description": f"The exact plan name. Must be one of: {', '.join(plan_names)}",
                        }
                    },
                    "required": ["plan_name"],
                },
            },
        }
    ]

    prior_turns = [
        {"role": m["role"], "content": m["content"]}
        for m in (history or [])
        if m.get("role") in ("user", "assistant") and m.get("content")
    ]

    messages = [
        {"role": "system", "content": system_prompt},
        *prior_turns,
        {"role": "user", "content": user_message},
    ]

    # Call 1 — model decides whether to call the tool
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )

    assistant_message = response.choices[0].message

    if not assistant_message.tool_calls:
        return assistant_message.content

    # Append assistant's tool call(s) to the conversation
    messages.append(assistant_message)

    # Execute each tool call and append results
    for tool_call in assistant_message.tool_calls:
        args = json.loads(tool_call.function.arguments)
        plan_name = args.get("plan_name", "")
        plan = plans_by_name.get(plan_name)

        if plan and plan.get("sbc_text"):
            result = plan["sbc_text"][:MAX_SBC_CHARS]
        else:
            result = f"No benefits document is available for {plan_name}."

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result,
        })

    # Call 2 — model answers using the tool results
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        max_tokens=1024,
        messages=messages,
    )

    return response.choices[0].message.content
