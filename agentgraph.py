# Importation des bibliothèques nécessaires pour l'agent LangChain
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI 
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.messages import HumanMessage
import asyncio
from IPython.display import Markdown

# Chargement des variables d'environnement (clé API OpenAI, etc.)
# override=True permet d'écraser les variables existantes
load_dotenv(override=True)

# Configuration du client MCP (Model Context Protocol)
# Je me connecte à un serveur MCP local qui fournit des outils
mcp_client = MultiServerMCPClient(
    {
        "mcpserver": {
        "transport": "streamable_http",  # Utilisation du protocole HTTP streaming
        "url": "http://localhost:24000/mcp",  # URL du serveur MCP local
        }
    }
)


async def main():
    # Récupération des outils disponibles depuis le serveur MCP
    # Ces outils seront utilisables par l'agent
    tools = await mcp_client.get_tools()
    
    # Initialisation du modèle de langage OpenAI
    # J'utilise gpt-4o-mini pour un bon compromis qualité/coût
    # temperature=0 pour des réponses déterministes et reproductibles
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # Création de l'agent qui va combiner le modèle LLM avec les outils MCP
    # Le system_prompt guide le comportement de l'agent
    agent = create_agent(
        model=llm, 
        tools=tools,
        system_prompt="answer the user question using provided tools",
    )
    
    # Boucle interactive pour poser des questions à l'agent
    while True:
        # Demande une question à l'utilisateur
        user_query = input("Question:")
        
        # Condition de sortie de la boucle
        if user_query == "exit":
            break
        
        # Envoi de la question à l'agent et attente de la réponse
        # ainvoke est la version asynchrone pour ne pas bloquer l'exécution
        response = await agent.ainvoke({"messages": [HumanMessage(user_query)]})
        
        # Affichage du contenu du dernier message (la réponse de l'agent)
        print(response["messages"][-1].content)

# Point d'entrée du script
# Si ce fichier est exécuté directement (et pas importé comme module)
if __name__ == "__main__":
    # Lancement de la fonction asynchrone main()
    asyncio.run(main())