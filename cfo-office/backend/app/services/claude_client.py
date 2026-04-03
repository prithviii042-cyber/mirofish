import anthropic
from app.config import Config


def get_client() -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)


def stream_response(messages: list, system: str = "", max_tokens: int = 16000):
    """Stream a Claude response with adaptive thinking. Yields text chunks."""
    client = get_client()
    with client.messages.stream(
        model=Config.CLAUDE_MODEL,
        max_tokens=max_tokens,
        thinking={"type": "adaptive"},
        system=system,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text


def complete(messages: list, system: str = "", max_tokens: int = 8000) -> str:
    """Single-shot Claude call. Returns full text response."""
    client = get_client()
    response = client.messages.create(
        model=Config.CLAUDE_MODEL,
        max_tokens=max_tokens,
        thinking={"type": "adaptive"},
        system=system,
        messages=messages,
    )
    for block in response.content:
        if block.type == "text":
            return block.text
    return ""
