# MEMORY.md - Archivio a Lungo Termine

## Insight Rilevanti (2026-03-27)

### Skills e Capacità Disponibili
**Skill operative core:**
1. **ssh-remote-manager** — Gestione remota via SSH/Portainer (yenkis-ai, NasPi, msi)
2. **healthcheck** — Security hardening, firewall/SSH/update audits
3. **weather** — Current weather e forecasts via wttr.in/Open-Meteo
4. **gemini** — CLI per Q&A e generation (fallback gratuito)
5. **tmux** — Remote-control sessioni tmux via keystrokes
6. **node-connect** — Debug connessioni OpenClaw (QR/pairing failures)
7. **skill-creator** — Creare/migliorare skills (tidy up, audit, review)

**Tools nativi:**
- **web_search/web_fetch** — Ricerche Brave + extraction
- **cron** — Job scheduling e reminders
- **memory_search/memory_get** — Recall semantico MEMORY.md + memory/
- **sessions_spawn** — Sub-agents e ACP coding sessions
- **image_generate** — Image generation con modelli configurati
- **exec/process** — Shell commands e session management

### Homelab avanzato e Docker
- **Skill Homelab-Monitor**: Implementato script per gestione semplificata homelab. Include dashboard, script Python per salute container e restart semplificati.

### Lezioni Sicurezza Apprese
1. **Routing Modelli Risorse**: Heartbeat su modelli come Gemini per convenienza e mantenere costi efficienti.
2. **Strict Skill Trust**: VirusTotal per audit esterni prima skills community.
3. **Action Boundaries**: Sempre chiedere conferma per azioni distruttive o esterne

---

## 🎮 OGame AGI Project (2026-03-29-30)
**Status:** ✅ **COMPLETATO E DEPLOYED**

**GitHub:** https://github.com/Shinigallo/ogame-agi (commit dbb93a3)

**Architettura Smart Bot (90% token reduction):**
- Event-driven: AI calls solo su trigger (timer, thresholds, fleet return)
- Quick checks ogni 60s via DOM parsing (zero AI)
- Rule-based fallbacks per decisioni semplici
- OpenClaw cron integration per scheduling

**Smart Triggers implementati:**
- Building/research completion
- Resource thresholds (Metal >50K, Crystal >25K, Deuterium >12.5K)
- Fleet return notifications
- Emergency situations

**Docker Deployment:**
- Smart Bot: 512MB RAM, 0.2 CPU (`docker-compose.smart.yml`)
- Full Bot: 2GB RAM, 1.0 CPU (`docker-compose.bot.yml`)
- Portainer stack disponibile (`portainer-stack.yml`)

**Bot Suite:**
| Bot | Caratteristiche |
|-----|-----------------|
| `smart_ogame_bot.py` | Production default, event-driven |
| `ogame_bot.py` | Full AI-driven, continuous 5min cycles |

**Anti-Detection:** Randomized timing (3-8s), human-like patterns, session breaks, auto-fleetsave

**Account test:** TestAgent2026 / TestAGI2026! su Scorpius (s161-en.ogame.gameforge.com)

## ⚡ TurboQuant CUDA Setup (2026-03-28)
**Status:** ✅ Installato, ⚠️ compatibilità parziale

- **Installazione:** Ollama nativo v0.18.3 + TurboQuant binary standalone
- **VRAM efficiency:** -75% su TinyLlama (11 MiB vs ~40-50 standard context)
- **Problema:** Qwen3 14B e DeepSeek-R1 14B non compatibili (output corrotto/crash)
- **Storage:** /mnt/ollama-storage (97 GB modelli)
- **Prossimo step:** Testare modelli GGUF nativi da HuggingFace

## 🧠 Qwen 3.5:35b-A3B - TOP MODEL (2026-03-30)
**Status:** ✅ Nativo Ollama, pienamente funzionante

**Specs:**
- **Architecture:** MoE (35B totali parametri, 3B attivi)
- **Size:** 23 GB storage, ~28 GB RAM load
- **Deployment:** Ollama nativo barebone (no container overhead)
- **Features:** Thinking process visibile, meta-cognizione, auto-riflessione

**Performance:**
- First load: ~2-3 minuti
- Italian support: Perfetto
- Zero rate limits, disponibile 24/7
- Zero costi (locale)

**RAM Management:**
- Containers fermati per load: Windows VM (4.2GB), ComfyUI (762MB), Obsidian (733MB), Open-WebUI (793MB)
- ⚠️ Richiede 28GB RAM totali

**Dario ha approvato esplicitamente integrazione** ✅

**Gerarchia modelli (TOOLS.md):**
1. qwen3.5:35b-a3b (TOP) → Ragionamento complesso, thinking trasparente
2. qwen3:14b → Bilanciato qualità/velocità
3. qwen3.5:9b → Sub-task standard
4. Copilot Pro → Fallback capabilities specifiche
5. Gemini CLI → Fallback gratuito

## 📊 Plugin OpenClaw Consigliati (2026-03-29 Reddit Scout)
**Priorità alta** — allineati con pet peeve costi:
1. **`manifest`** — Routing automatico verso modelli economici (Gemini Flash Lite)
2. **`cost-tracker`** — Visibility spese per sessione/sub-agent
3. **`OpenClaw Nerve`** — Dashboard real-time multi-agent

## 🧠 Lezioni Operative Aggiornate
4. **Verificare prima di alertare** — Un allarme falso è peggio di nessun allarme. Check stato corrente vs memory.
5. **Container-free validation** — Logica AI/testable anche senza Docker. Non aspettare il container per validare il core.
6. **HTML fallback** — Quando PDF tools mancano, HTML + browser print è sempre disponibile.
7. **Gemini Flash Lite** — Nuovo standard per task leggeri (reddit scout conferma)
8. **Event-driven AI > Polling** — Token savings massivi. AI per complessità, rule-based per routine (OGame Smart Bot: 90% reduction).
9. **RAM management before large model load** — Fermare containers non essenziali prima di caricare modelli >20GB.
10. **Native > Container for AI** — Ollama nativo elimina overhead e dependency issues. Performance superiori.