import logging
import os

from groq import Groq

from .prompts import BENEFITS_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

MAX_SBC_CHARS = 15_000
GROQ_MODEL = "llama-3.3-70b-versatile"


def get_ai_response(*, plan_name: str, sbc_text: str, user_message: str) -> str:
    """
    Send a user message to Groq along with the plan's SBC text as context.
    Returns the assistant's reply as a plain string.
    Raises groq.APIError subclasses on API failures.
    """
    truncated_sbc = sbc_text[:MAX_SBC_CHARS]

    system_prompt = BENEFITS_SYSTEM_PROMPT.format(
        plan_name=plan_name,
        sbc_text=truncated_sbc,
    )

    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        max_tokens=1024,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )

    return response.choices[0].message.content
