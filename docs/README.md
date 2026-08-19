# Repositório-base — Nexa Solutions

> Projeto didático para a disciplina de Manutenção e Evolução de Software.
>
> **Atenção aos estudantes:** este repositório é entregue propositalmente incompleto. Ele possui falhas funcionais, lacunas de infraestrutura, documentação insuficiente e decisões técnicas que precisam ser revisadas. Não trate o estado atual como solução de referência.

## Contexto

A Nexa Solutions mantém uma API de chamados internos. A empresa precisa corrigir problemas relatados por usuários, melhorar a execução em ambientes diferentes e implementar funcionalidades solicitadas pela coordenação de suporte.

A aplicação registra chamados com título, descrição e status. O backend foi iniciado com Django e Django REST Framework, com uma página HTML simples para consumo da API.

## O que já existe

- API REST inicial para listar e cadastrar chamados.
- Modelo inicial `Chamado`.
- Interface HTML simples para listar e criar registros.
- Arquivos de Docker entregues **incompletos**.
- README propositalmente insuficiente.
- Lista de demandas da empresa em [`docs/issues.md`](docs/issues.md).

## Estrutura do projeto

```text
nexa-chamados/
├── backend/
│   ├── config/
│   ├── chamados/
│   ├── requirements.txt
│   └── manage.py
├── frontend/
│   └── index.html
├── docs/
│   └── issues.md
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Problemas intencionais conhecidos

A empresa informou que o projeto possui os seguintes indícios de problema, mas cabe à dupla analisar e confirmar o impacto de cada um:

- O cadastro sem título pode retornar erro interno em vez de uma resposta de validação.
- A API lista todos os chamados, mas ainda não permite filtro por status.
- Não há endpoint de indicadores.
- O Dockerfile não instala as dependências necessárias.
- O `docker-compose.yml` não inicia um banco de dados e não utiliza variáveis de ambiente.
- A configuração do Django utiliza SQLite e a chave secreta está escrita diretamente no código.
- Não há testes automatizados.
- Este README não explica como executar o sistema de maneira reproduzível.

## Entrega esperada da dupla

A dupla deverá transformar este projeto em uma entrega reproduzível e profissional. A versão final deve permitir que um avaliador execute o ambiente com:

```bash
docker compose up --build
```

Também deve conter documentação, variáveis de ambiente, banco de dados containerizado, testes automatizados, issues, branches, commits claros e Pull Requests revisadas.

Consulte o arquivo [`docs/issues.md`](docs/issues.md) para as solicitações formais da empresa.

## Estado atual — execução local temporária

Enquanto a infraestrutura Docker não é corrigida, o backend pode ser executado localmente, apenas para fins de diagnóstico:

```bash
cd backend
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

A API inicial estará disponível em `http://localhost:8000/api/chamados/`.

> Esta forma de execução **não** atende à demanda da empresa. A dupla deve corrigir a infraestrutura com Docker e Docker Compose.
