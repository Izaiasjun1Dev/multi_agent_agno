"""
Configuração de banco de dados PostgreSQL
Database configuration for PostgreSQL
"""

import os
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Importa as configurações do projeto
from configs.load_env import settings

# Base para os modelos SQLAlchemy
Base = declarative_base()


class DatabaseConfig:
    """
    Configuração do banco de dados PostgreSQL
    PostgreSQL database configuration
    """

    def __init__(self):
        self.database_url = self._get_database_url()

    def _get_database_url(self) -> str:
        """
        Constrói a URL de conexão com o PostgreSQL usando variáveis de ambiente
        Builds PostgreSQL connection URL using environment variables
        """
        return f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

    def _get_async_database_url(self) -> str:
        """
        Constrói a URL de conexão assíncrona com o PostgreSQL usando variáveis de ambiente
        Builds async PostgreSQL connection URL using environment variables
        """
        return f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

    def get_engine(self, echo: bool = False):
        """
        Cria e retorna o engine do SQLAlchemy
        Creates and returns SQLAlchemy engine
        """
        return create_engine(
            self.database_url,
            echo=echo,
            pool_pre_ping=True,  # Verifica conexões antes de usar
            pool_recycle=3600,  # Recicla conexões a cada hora
        )

    def get_async_engine(self, echo: bool = False):
        """
        Cria e retorna o engine assíncrono do SQLAlchemy
        Creates and returns SQLAlchemy async engine
        """
        async_url = self._get_async_database_url()
        return create_async_engine(
            async_url,
            echo=echo,
            poolclass=StaticPool,  # Usa um pool estático para conexões assíncronas
            future=True,  # Habilita o uso de novas APIs do SQLAlchemy
        )

    def get_session_factory(self, echo: bool = False):
        """
        Cria e retorna uma factory de sessões
        Creates and returns a session factory
        """
        engine = self.get_engine(echo=echo)
        return sessionmaker(bind=engine, autocommit=False, autoflush=False)

    def get_async_session_factory(self, echo: bool = False):
        """
        Cria e retorna uma factory de sessões assíncronas
        Creates and returns an async session factory
        """
        async_engine = self.get_async_engine(echo=echo)
        return async_sessionmaker(
            bind=async_engine,
            autoflush=False,
            expire_on_commit=False,
            future=True,
        )


# Instância global da configuração
db_config = DatabaseConfig()

# Engine e SessionLocal para uso em outros módulos
engine = db_config.get_engine()
SessionLocal = db_config.get_session_factory()
AsyncSessionLocal = db_config.get_async_session_factory()


def get_database_url() -> str:
    """
    Retorna a URL de conexão com o banco de dados
    Returns the database connection URL
    """
    return db_config.database_url


def get_db_session():
    """
    Dependency para obter uma sessão de banco de dados
    Dependency to get a database session
    """
    session = SessionLocal()
    try:
        return session
    finally:
        session.close()
