# Lynx — Build Plan

A personal "Jarvis-style" voice assistant. **MVP goal:** talk to it by voice like a normal LLM conversation, send email, and CRUD Google Calendar events — all from plain speech.

This file is the living roadmap. Each phase = one concept + one working demo. Tick boxes as we complete them.

---

## The learning contract 📚

- **You type the code.** I explain the concept, give the shape and API signatures, you write it, we run and debug together.
- **One concept per phase.** Each phase has a clear learning objective and ends with a runnable demo.
- **No giant code dumps.** We build files up a few functions at a time.
- **The agentic loop is the crown jewel** — the same pattern that powers Claude Code and every modern AI agent.

## The architecture (the map) 🗺️

```
┌──────────┐   listen()   ┌─────────────────┐   text    ┌──────────────────────┐
│  You     │ ───────────► │   audio.py   │ ────────► │       brain.py       │
│ (voice)  │              │ (STT: AssemblyAI)│         │  Claude API + agentic │
└──────────┘              └─────────────────┘           │  loop + tools        │
     ▲                                                └──────────┬───────────┘
     │  speak()                                                    │ tool_use
     │  (TTS: edge-tts)                                            ▼
┌──────────┐      text      ┌──────────────┐   calls    ┌──────────────┐
│ speakers │ ◄──────────────│   audio.py   │ ◄──────────│  tools.py    │
└──────────┘                └──────────────┘            │  email (SMTP)│
                                                         │  calendar    │
                                                         └──────────────┘
```

### The agentic loop (the core concept) ⭐

```
user message → send to Claude (with tool definitions)
  → Claude replies with EITHER final text OR a tool_use request
  → if tool_use: run the tool, send the result back to Claude
  → repeat until Claude gives final text → speak it
```

Claude never executes anything — it *requests* tool calls, and **your Python code** decides what runs. This boundary is the most important idea in the whole project.

---

## Phases

### Phase 0 — Scaffold & environment
**Learn:** why modular structure matters, virtual envs, git hygiene.
- [x] `git init`, `.gitignore` (secrets!), `requirements.txt`, `.env`, package layout
- [x] Install deps. `python -m lynx` prints a placeholder.
- **Demo:** clean project that runs; git tracks it; secrets stay out.

### Phase 1 — Lynx learns to speak (TTS)
**Learn:** text-to-speech pipeline, audio output, why we abstract `speak()`.
- [x] `speak(text)` using **edge-tts** → mp3 → play via macOS `afplay`.
- **Demo:** Lynx greets you out loud: *"Hello, I'm Lynx."*

### Phase 2 — Lynx learns to listen (STT)
**Learn:** microphone capture (sample rate, mono), cloud transcription (async job: upload → poll → text).
- [x] `listen()` using **sounddevice** to record + **AssemblyAI** to transcribe (recorded → WAV → MP3 → uploaded → text returned).
- [x] Push-to-talk for the MVP (press Enter to start/stop). Continuous listening & wake word are stretch goals.
- **Demo:** you say something, Lynx prints exactly what you said.

### Phase 3 — Voice loop with a mock brain
**Learn:** composing audio pieces into a loop; isolating audio bugs from AI bugs.
- [ ] Loop: `listen()` → echo → `speak()`. Terminate with "exit".
- **Demo:** a working voice conversation loop (dumb brain, proves the plumbing).

### Phase 4 — Lynx's brain (Claude API)
**Learn:** LLM API basics, streaming, system prompts, personas.
- [ ] Wire in the `anthropic` SDK, streaming responses, JARVIS-style persona in the system prompt.
- **Demo:** full voice conversation with real Claude.

### Phase 5 — The agentic loop + tool use ⭐
**Learn:** the loop that makes agents "do things" — tool definitions (JSON schema), the request/execute/return pattern.
- [ ] Teach with a trivial tool first: `get_current_time`.
- **Demo:** *"What time is it?"* → Lynx calls the tool and speaks the answer. (Magic moment — this is where it becomes an *agent*, not a chatbot.)

### Phase 6 — Email tool
**Learn:** SMTP, app passwords, putting a real capability behind a tool.
- [ ] `send_email(to, subject, body)` via `smtplib` + Gmail App Password.
- **Demo:** *"Send an email to <person> saying I'll be 10 minutes late"* → Lynx parses it, sends it, confirms out loud.

### Phase 7 — Google Calendar integration
**Learn:** OAuth 2.0, third-party API CRUD, multi-tool coordination.
- [ ] One-time OAuth token setup (`calendar_client.py`), then tools: `list_events`, `create_event`, `update_event`, `delete_event`.
- **Demo:** *"Create a meeting with Sarah Friday at 3pm"* → event appears in your Google Calendar; also list/update/delete by voice.

### Phase 8 — Polish & your next steps
**Learn:** recap — a mental model you keep.
- [ ] Recap of the architecture and every concept learned.
- [ ] Ideas you can grow into: long-term memory, wake word, continuous listening, web search, system automation, a desktop UI.

---

## Key files

```
requirements.txt     — anthropic, edge-tts, faster-whisper, sounddevice,
                       numpy, python-dotenv, google-api-python-client,
                       google-auth-oauthlib
lynx/
  __init__.py
  config.py          — loads .env secrets
  audio.py           — listen() (STT) + speak() (TTS)
  brain.py           — Claude API client + agentic loop
  tools.py           — functions Lynx can call (email, calendar, time)
  calendar_client.py — Google Calendar OAuth + raw CRUD
  main.py            — the voice chat loop (entry point)
.env                 — secrets, gitignored
.gitignore
README.md
```

## Prerequisites

- Python 3.11+ (`python3 --version` to check)
- `ANTHROPIC_API_KEY` in `.env` ✅
- Microphone + speakers, internet connection
- **Phase 6:** Gmail account with 2-Step Verification + an App Password
- **Phase 7:** Google Cloud project with Calendar API enabled + OAuth desktop client (one-time setup)

## Final MVP acceptance test ✅

1. `python -m lynx` → Lynx speaks a greeting.
2. Ask *"What time is it?"* → correct spoken answer (tool use works).
3. Ask Lynx to send an email → recipient receives it, Lynx confirms.
4. Ask Lynx to create an event → it appears in Google Calendar; repeat for list/update/delete.
