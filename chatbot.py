#!/usr/bin/env python3
"""
Python CLI Chatbot using OpenAI API
Run: python chatbot.py
"""

import os
import sys
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

console = Console()

SYSTEM_PROMPT = """You are a helpful, friendly AI assistant. 
You provide clear, accurate, and thoughtful responses.
When sharing code, use proper formatting."""

def check_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        console.print(
            Panel(
                "[bold red]Error:[/bold red] OPENAI_API_KEY environment variable is not set.\n\n"
                "Please set it before running:\n"
                "  [cyan]export OPENAI_API_KEY=your-api-key-here[/cyan]\n\n"
                "Or add it as a Replit secret named [bold]OPENAI_API_KEY[/bold].",
                title="Missing API Key",
                border_style="red"
            )
        )
        sys.exit(1)
    return api_key


def print_welcome():
    console.print(
        Panel(
            "[bold cyan]Welcome to the OpenAI CLI Chatbot![/bold cyan]\n\n"
            "  [dim]Type your message and press Enter to chat.[/dim]\n"
            "  [dim]Commands:[/dim]\n"
            "  [dim]  /clear  — Clear conversation history[/dim]\n"
            "  [dim]  /quit   — Exit the chatbot[/dim]",
            border_style="cyan",
            padding=(1, 2),
        )
    )


def stream_response(client: OpenAI, messages: list[dict]) -> str:
    """Stream a response from the OpenAI API and return the full text."""
    console.print()
    console.print("[bold green]Assistant:[/bold green]")

    full_response = ""
    with client.chat.completions.stream(
        model="gpt-4o",
        messages=messages,
        max_completion_tokens=8192,
    ) as stream:
        for text in stream.text_stream:
            console.print(text, end="", highlight=False)
            full_response += text

    console.print()
    console.print()
    return full_response


def main():
    api_key = check_api_key()
    client = OpenAI(api_key=api_key)

    conversation_history: list[dict] = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    print_welcome()

    while True:
        try:
            user_input = Prompt.ask("[bold yellow]You[/bold yellow]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n\n[dim]Goodbye![/dim]")
            break

        if not user_input:
            continue

        if user_input.lower() in ("/quit", "/exit", "quit", "exit"):
            console.print("\n[dim]Goodbye![/dim]")
            break

        if user_input.lower() == "/clear":
            conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]
            console.clear()
            print_welcome()
            console.print("[dim]Conversation history cleared.[/dim]\n")
            continue

        conversation_history.append({"role": "user", "content": user_input})

        try:
            assistant_reply = stream_response(client, conversation_history)
            conversation_history.append(
                {"role": "assistant", "content": assistant_reply}
            )
        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {e}\n")
            conversation_history.pop()


if __name__ == "__main__":
    main()
