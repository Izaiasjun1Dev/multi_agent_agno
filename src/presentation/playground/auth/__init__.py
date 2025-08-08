from infraestructure.repositoryes.agent.agent_repository import AgentRepository
from infraestructure.repositoryes.auth.repository import AuthRepository
from infraestructure.repositoryes.user.repository import UserRepository
from core.usecases.user.usecases import LoginUserUseCase
from configs.load_env import settings

user_repository = UserRepository()
auth_repository = AuthRepository()
agent_repository = AgentRepository()

usecase = LoginUserUseCase(
    auth_interface=auth_repository,
)
if settings.user_password is None:
    raise ValueError("User password is not set in the environment variables.")

login_user = usecase.execute(
    email="solucaoprogramer@gmail.com",
    password=settings.user_password,
)