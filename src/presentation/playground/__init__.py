import asyncio

from agno.playground import Playground
from core.usecases.agent.agent_usecases import (
    CreateAgentUseCase,
    DefineTeamToPlaygroundUseCase,
)
from presentation.playground.auth import agent_repository, auth_repository, login_user


# Criar agentes diretamente para o playground
async def create_playground_team():
    """Cria um team para o playground sem necessidade de autenticação"""
    create_agent_usecase = CreateAgentUseCase(
        auth_repository=auth_repository, 
        agent_repository=agent_repository,
    )

    define_team_usecase = DefineTeamToPlaygroundUseCase(
        agent_create_usecase=create_agent_usecase,
        auth_repository=auth_repository,
        agent_repository=agent_repository,
    )

    token = login_user["access_token"]

    return await define_team_usecase.execute(token)


# Executar de forma síncrona para criar o playground
def create_inner_team():
    """Wrapper síncrono para criar o team"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(create_playground_team())
    finally:
        loop.close()


# Criar o playground
inner_chat_team, inner_agents = create_inner_team()

playground = Playground(
    teams=[inner_chat_team],
    agents=inner_agents,
    name="Inner Chat Playground",
    description="Playground para interações com agentes de chat internos",
)
