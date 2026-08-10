# API System Helpdesk

API RESTful para gerenciamento de chamados e usuários, construída utilizando Python, Flask e SQLAlchemy.

## Estrutura do Projeto

O projeto adota uma Arquitetura em Camadas (Layered Architecture):
- **Controllers**: Manipulação de requisições HTTP e validação de entrada/saída.
- **Services**: Lógica e regras de negócio.
- **Repositories**: Consultas diretas ao banco via ORM SQLAlchemy.
- **Models**: Mapeamento das tabelas SQLite.

## Requisitos
- Python 3.8+
- Pip

## Como Executar

1. **Instalar Dependências**:
   ```bash
   pip install flask flask-sqlalchemy