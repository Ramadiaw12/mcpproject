# 🤖 MCP Agent — Intelligent HR & Web Assistant

> *Un agent IA qui répond à vos questions RH et recherches web en langage naturel, propulsé par DeepSeek et LangGraph via le protocole MCP.*

![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)
![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2%2B-FF6B35?style=flat-square)
![MCP](https://img.shields.io/badge/MCP-1.0%20standard-6C3483?style=flat-square)
![DeepSeek](https://img.shields.io/badge/LLM-DeepSeek-00BCD4?style=flat-square)
![Status](https://img.shields.io/badge/status-active-brightgreen?style=flat-square)

---

## 🎯 En une phrase

Un serveur MCP exposant des outils RH et de recherche web, piloté par un agent LangGraph, accessible en langage naturel.

---

## 📸 Aperçu

> `[CAPTURE_ECRAN_1]`
> *→ Montrer l'interface MCP Inspector avec le serveur connecté et les deux outils visibles (`get_employee_infos`, `search`)*

---

## 🏗️ Architecture simplifiée

```
Vous (langage naturel)
        │
        ▼
┌───────────────────┐
│   Agent LangGraph  │  ←── Openai LLM (raisonnement)
└────────┬──────────┘
         │  appel d'outil via MCP
         ▼
┌───────────────────┐
│   Serveur MCP     │  ←── HTTP Streamable (SSE)
└────────┬──────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐  ┌────────┐
│  RH   │  │  Web   │
│ Tool  │  │ Search │
└───────┘  └────────┘
  Base       Tavily
 employés     API
    │           │
    └─────┬─────┘
          ▼
   Réponse structurée
```

L'agent décide **lui-même** quel outil utiliser en fonction de votre question — sans aucune configuration manuelle.

---

## 🚀 Ce que vous pouvez faire

### 👥 Cas RH — Infos employés

> **Vous :** "Quel est le salaire de Rahma ?"
>
> **Agent :** "Rahma a 34 ans et perçoit un salaire mensuel de **4 200 €**."

---

### 🌍 Cas recherche — Info en temps réel

> **Vous :** "Quelle est la température à Paris aujourd'hui ?"
>
> **Agent :** "D'après mes recherches, il fait actuellement **18°C** à Paris avec des éclaircies en après-midi."

---

### 🔀 Cas mixte — Analyse croisée

> **Vous :** "Compare le salaire de Rahma avec la moyenne française des développeurs."
>
> **Agent :** "Rahma gagne **4 200 €/mois**. Selon les dernières données disponibles, la moyenne nationale pour un développeur en France est de **3 850 €/mois**. Rahma est donc **9% au-dessus** de la moyenne."

---

## 🛠️ Tech stack

| Composant | Technologie | Pourquoi ce choix |
|-----------|-------------|-------------------|
| 🧠 LLM | API OpenAI | 
| 🔁 Agent | LangGraph | Contrôle total du flux, facile à étendre |
| 🔌 Protocole | MCP (Model Context Protocol) | Standard ouvert, compatible Claude Desktop & Co |
| 🌐 Transport | HTTP Streamable (SSE) | Streaming en temps réel, sans WebSocket |
| 🔍 Recherche web | Tavily API | Résultats propres, conçu pour les LLMs |
| 🛠️ Test | MCP Inspector | Debug visuel des appels d'outils |

---

## 📦 Installation

```bash
# 1. Cloner le projet
git clone https://github.com/Ramadiaw12/mcpproject.git && cd mcp-agent

# 2. Installer les dépendances Python

uv.lock
# 3. Configurer les clés API
cp .env.example .env  # puis renseigner DEEPSEEK_API_KEY et TAVILY_API_KEY
```

> ℹ️ Node.js est requis uniquement si vous utilisez MCP Inspector (`npm install -g @modelcontextprotocol/inspector`)

---

## ▶️ Utilisation

**Démarrer le serveur MCP :**
```bash
uv run mcpserver.py
```

**Lancer l'agent :**
```bash
uv run agentgraph.py "Quel est le salaire de Rahma ?"
```

**Tester avec MCP Inspector :**
```bash
npx @modelcontextprotocol/inspector http://localhost:24000
```

> `[CAPTURE_ECRAN_2]`
> *→ Montrer le terminal avec le serveur démarré et l'agent recevant une réponse en streaming*

---

## 💬 Exemples d'interactions

> `[CAPTURE_ECRAN_3]`
> *→ Montrer MCP Inspector avec un appel à `get_employee_infos` pour "Rahma" et la réponse JSON structurée*

**Réponse brute de l'outil `get_employee_infos` :**
```json
{
  "name": "Rahma",
  "age": 21,
  "salary": 4200
}
```

**Réponse brute de l'outil `search` :**
```json
{
  "query": "température Paris aujourd'hui",
  "results": [
    { "title": "Météo Paris - Aujourd'hui", "content": "18°C, partiellement nuageux..." }
  ]
}
```

> `[CAPTURE_ECRAN_4]`
> *→ Montrer un dialogue complet dans le terminal : question utilisateur → sélection d'outil par l'agent → réponse finale*

---

## 📈 Performance & limites

| Critère | Valeur | Note |
|---------|--------|------|
| ⚡ Temps de réponse moyen | ~2–4 secondes | Dépend de Tavily et DeepSeek |
| 💰 Coût par requête | ~$0.001–0.003 | DeepSeek est ~20x moins cher que GPT-4 |
| 👥 Employés supportés | Base locale statique | Extensible à une vraie BDD |
| 🌐 Recherches web | Limitées par quota Tavily | Plan gratuit : 1 000 req/mois |
| 🔧 Outils simultanés | Multi-outil supporté | LangGraph gère le séquençage |
| 🧩 Compatibilité | Tout client MCP standard | Claude Desktop, Continue, etc. |

---

## 🔮 Roadmap

| Version | Fonctionnalité | Statut |
|---------|----------------|--------|
| `v1.0` | Outils RH + recherche web, agent LangGraph | ✅ Disponible |
| `v1.1` | Connexion base de données PostgreSQL | 🔄 En cours |
| `v1.2` | Authentification OAuth2 sur le serveur MCP | 📅 Planifié |
| `v1.3` | Interface web (Streamlit) pour dialogues | 📅 Planifié |
| `v2.0` | Ajout d'outils : calendrier, email, CRM | 💡 Idée |
| `v2.1` | Support multi-agent (LangGraph Supervisor) | 💡 Idée |

---

## 🤝 Contribuer

Les contributions sont les bienvenues ! Voici comment participer :

1. **Fork** le repo et crée une branche : `git checkout -b feature/mon-outil`
2. **Ajoute ton outil** dans `tools/` en suivant la structure existante
3. **Teste** avec MCP Inspector avant de soumettre
4. **Ouvre une Pull Request** avec une description claire

> 💡 Les ajouts d'outils (météo, Slack, Notion, etc.) sont particulièrement appréciés !

---

## ❓ FAQ

**💰 Quel est le coût d'utilisation ?**
Pratiquement nul pour un usage personnel. DeepSeek coûte ~$0.001–0.003 par requête, et Tavily offre 1 000 recherches gratuites par mois.

**🔧 Peut-on ajouter ses propres outils ?**
Oui, très facilement. Il suffit de créer une nouvelle fonction dans `tools/` et de l'enregistrer dans le serveur MCP — une dizaine de lignes suffisent.

**🖥️ Est-ce compatible avec Claude Desktop ?**
Oui. Le serveur suit le standard MCP officiel. Il suffit d'ajouter l'URL du serveur dans la config de Claude Desktop.

**🗄️ Les données employés sont-elles sécurisées ?**
La démo utilise une base locale statique. En production, connectez votre propre BDD et ajoutez une couche d'authentification (voir roadmap v1.2).

**🔄 Peut-on utiliser un autre LLM que DeepSeek ?**
Oui. L'agent utilise l'interface compatible OpenAI — tout LLM supportant ce format fonctionne (GPT-4, Mistral, etc.).

---

## 📄 Licence

Distribué sous licence **MIT**. Voir le fichier [LICENSE](./LICENSE) pour les détails.

© 2025 — DIAWANE Ramatoulaye

---

## 🌟 Support & Contact

Si ce projet vous est utile, une ⭐ sur GitHub fait toujours plaisir !

| Canal | Lien |
|-------|------|
| 🐛 Bug / Feature request | https://github.com/Ramadiaw12/mcpproject
| 💼 LinkedIn | https://www.linkedin.com/in/ramatoulaye-diawane/
| 📧 Email | rdiawane2001@gmail.com |
