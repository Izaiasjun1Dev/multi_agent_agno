#!/usr/bin/env python3
"""
Script para deletar todos os usuários do AWS Cognito User Pool de forma recursiva.
Script to recursively delete all users from AWS Cognito User Pool.

Uso/Usage:
    python delete_all_users.py --user-pool-id <USER_POOL_ID> [--region <REGION>] [--dry-run]

Exemplo/Example:
    python delete_all_users.py --user-pool-id us-east-1_XXXXXXXXX --region us-east-1
    python delete_all_users.py --user-pool-id us-east-1_XXXXXXXXX --dry-run
"""

import argparse
import sys
import time
from typing import Any, Dict, List

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class CognitoUserManager:
    """Gerenciador para operações de usuários do Cognito"""

    def __init__(self, user_pool_id: str, region: str = "us-east-1"):
        """
        Inicializa o gerenciador do Cognito

        Args:
            user_pool_id: ID do User Pool do Cognito
            region: Região AWS (padrão: us-east-1)
        """
        self.user_pool_id = user_pool_id
        self.region = region

        try:
            self.cognito_client = boto3.client("cognito-idp", region_name=region)
            print(f"✅ Conectado ao Cognito na região {region}")
        except Exception as e:
            print(f"❌ Erro ao conectar com o Cognito: {e}")
            sys.exit(1)

    def list_all_users(self) -> List[Dict[str, Any]]:
        """
        Lista todos os usuários do User Pool

        Returns:
            Lista de usuários
        """
        all_users = []
        pagination_token = None

        try:
            print("📋 Listando usuários do User Pool...")

            while True:
                params = {
                    "UserPoolId": self.user_pool_id,
                    "Limit": 60,  # Máximo permitido pelo Cognito
                }

                if pagination_token:
                    params["PaginationToken"] = pagination_token

                response = self.cognito_client.list_users(**params)
                users = response.get("Users", [])
                all_users.extend(users)

                print(f"📄 Encontrados {len(users)} usuários nesta página...")

                pagination_token = response.get("PaginationToken")
                if not pagination_token:
                    break

                # Pequena pausa para evitar rate limiting
                time.sleep(0.1)

            print(f"📊 Total de usuários encontrados: {len(all_users)}")
            return all_users

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            error_message = e.response.get("Error", {}).get("Message", "Unknown error")
            print(f"❌ Erro do Cognito ({error_code}): {error_message}")
            return []
        except Exception as e:
            print(f"❌ Erro inesperado ao listar usuários: {e}")
            return []

    def delete_user(self, username: str) -> bool:
        """
        Deleta um usuário específico

        Args:
            username: Nome do usuário para deletar

        Returns:
            True se deletado com sucesso, False caso contrário
        """
        try:
            self.cognito_client.admin_delete_user(
                UserPoolId=self.user_pool_id, Username=username
            )
            return True

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            error_message = e.response.get("Error", {}).get("Message", "Unknown error")
            print(
                f"❌ Erro ao deletar usuário '{username}' ({error_code}): {error_message}"
            )
            return False
        except Exception as e:
            print(f"❌ Erro inesperado ao deletar usuário '{username}': {e}")
            return False

    def delete_all_users(self, dry_run: bool = False) -> Dict[str, int]:
        """
        Deleta todos os usuários do User Pool

        Args:
            dry_run: Se True, apenas simula a deleção sem executar

        Returns:
            Dicionário com estatísticas da operação
        """
        users = self.list_all_users()

        if not users:
            print("ℹ️  Nenhum usuário encontrado para deletar.")
            return {"total": 0, "deleted": 0, "failed": 0}

        total_users = len(users)
        deleted_count = 0
        failed_count = 0

        print(
            f"\n{'🔍 SIMULAÇÃO' if dry_run else '🗑️  DELEÇÃO'} - Processando {total_users} usuários..."
        )
        print("=" * 60)

        for i, user in enumerate(users, 1):
            username = user.get("Username", "N/A")
            email = next(
                (
                    attr["Value"]
                    for attr in user.get("Attributes", [])
                    if attr["Name"] == "email"
                ),
                "N/A",
            )
            status = user.get("UserStatus", "N/A")

            print(f"[{i:3d}/{total_users}] {username} ({email}) - Status: {status}")

            if dry_run:
                print(f"         🔍 SIMULAÇÃO: Usuário seria deletado")
                deleted_count += 1
            else:
                if self.delete_user(username):
                    print(f"         ✅ Usuário deletado com sucesso")
                    deleted_count += 1
                else:
                    print(f"         ❌ Falha ao deletar usuário")
                    failed_count += 1

                # Pausa para evitar rate limiting
                time.sleep(0.2)

        print("\n" + "=" * 60)

        if dry_run:
            print(f"🔍 SIMULAÇÃO CONCLUÍDA:")
            print(f"   📊 Total de usuários: {total_users}")
            print(f"   🗑️  Seriam deletados: {deleted_count}")
        else:
            print(f"🗑️  DELEÇÃO CONCLUÍDA:")
            print(f"   📊 Total de usuários: {total_users}")
            print(f"   ✅ Deletados com sucesso: {deleted_count}")
            print(f"   ❌ Falhas: {failed_count}")

        return {"total": total_users, "deleted": deleted_count, "failed": failed_count}


def validate_user_pool_id(user_pool_id: str) -> bool:
    """
    Valida o formato do User Pool ID

    Args:
        user_pool_id: ID do User Pool para validar

    Returns:
        True se válido, False caso contrário
    """
    # Formato esperado: region_xxxxxxxxx (ex: us-east-1_XXXXXXXXX)
    import re

    pattern = r"^[a-z0-9-]+_[A-Za-z0-9]+$"
    return bool(re.match(pattern, user_pool_id))


def confirm_deletion(user_pool_id: str, dry_run: bool) -> bool:
    """
    Confirma a operação de deleção com o usuário

    Args:
        user_pool_id: ID do User Pool
        dry_run: Se é uma simulação

    Returns:
        True se confirmado, False caso contrário
    """
    if dry_run:
        print(f"🔍 MODO SIMULAÇÃO: Executando dry-run para User Pool: {user_pool_id}")
        return True

    print(
        f"⚠️  ATENÇÃO: Esta operação irá DELETAR TODOS os usuários do User Pool: {user_pool_id}"
    )
    print("⚠️  Esta ação é IRREVERSÍVEL!")
    print("\nTem certeza que deseja continuar? (Digite 'DELETAR' para confirmar)")

    confirmation = input("Confirmação: ").strip()

    if confirmation == "DELETAR":
        print("✅ Confirmação recebida. Iniciando deleção...")
        return True
    else:
        print("❌ Operação cancelada pelo usuário.")
        return False


def main():
    """Função principal do script"""
    parser = argparse.ArgumentParser(
        description="Deleta todos os usuários de um User Pool do AWS Cognito",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  %(prog)s --user-pool-id us-east-1_XXXXXXXXX --region us-east-1
  %(prog)s --user-pool-id us-east-1_XXXXXXXXX --dry-run
  %(prog)s --user-pool-id us-east-1_XXXXXXXXX --region us-west-2

Nota: É altamente recomendado executar com --dry-run primeiro para verificar
quais usuários serão deletados antes de executar a operação real.
        """,
    )

    parser.add_argument(
        "--user-pool-id",
        required=True,
        help="ID do User Pool do Cognito (ex: us-east-1_XXXXXXXXX)",
    )

    parser.add_argument(
        "--region", default="us-east-1", help="Região AWS (padrão: us-east-1)"
    )

    parser.add_argument(
        "--dry-run", action="store_true", help="Executa simulação sem deletar usuários"
    )

    parser.add_argument(
        "--force", action="store_true", help="Pula confirmação (use com cuidado!)"
    )

    args = parser.parse_args()

    # Validar User Pool ID
    if not validate_user_pool_id(args.user_pool_id):
        print("❌ Formato inválido do User Pool ID.")
        print("   Formato esperado: region_xxxxxxxxx (ex: us-east-1_XXXXXXXXX)")
        sys.exit(1)

    # Verificar credenciais AWS
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        if not credentials:
            print("❌ Credenciais AWS não encontradas.")
            print("   Configure com: aws configure")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Erro ao verificar credenciais AWS: {e}")
        sys.exit(1)

    print("🚀 AWS Cognito User Pool - Deleção de Usuários")
    print("=" * 50)
    print(f"📍 User Pool ID: {args.user_pool_id}")
    print(f"🌍 Região: {args.region}")
    print(f"🔍 Modo: {'Simulação (Dry-run)' if args.dry_run else 'Deleção Real'}")
    print("=" * 50)

    # Confirmar operação
    if not args.force:
        if not confirm_deletion(args.user_pool_id, args.dry_run):
            sys.exit(0)

    # Executar operação
    try:
        manager = CognitoUserManager(args.user_pool_id, args.region)
        result = manager.delete_all_users(dry_run=args.dry_run)

        # Status de saída baseado no resultado
        if result["failed"] > 0 and not args.dry_run:
            print(f"\n⚠️  Processo concluído com {result['failed']} falhas.")
            sys.exit(1)
        else:
            print(f"\n✅ Processo concluído com sucesso!")
            sys.exit(0)

    except KeyboardInterrupt:
        print("\n\n❌ Operação interrompida pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
