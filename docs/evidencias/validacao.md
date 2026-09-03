# Evidências de validação

Saídas reais capturadas em 03/09/2026, em ambiente limpo — o volume do banco foi
removido com `docker compose down -v` antes de iniciar.

## 1. `docker compose up --build` a partir do zero

```console
$ docker compose down -v
$ docker compose up --build
Container nexa-db Creating 
Container nexa-db Created 
Container nexa-api Creating 
Container nexa-api Created 
Container nexa-db Starting 
Container nexa-db Started 
Container nexa-db Waiting 
Container nexa-db Healthy 
Container nexa-api Starting 
Container nexa-api Started 
nexa-api  |   Applying chamados.0001_initial... OK
nexa-api  |   Applying chamados.0002_alter_chamado_titulo... OK
nexa-api  | Watching for file changes with StatReloader
nexa-api  | System check identified no issues (0 silenced).
nexa-api  | Django version 5.2.17, using settings 'config.settings'
nexa-api  | Starting development server at http://0.0.0.0:8000/
```

O banco sobe primeiro; o serviço `api` aguarda o healthcheck (`nexa-db Healthy`)
e só então inicia, aplicando as migrações automaticamente. **INC-04.**

## 2. Serviços em execução

```console
$ docker compose ps
NAME       IMAGE                STATUS                    PORTS
nexa-api   nexa-solutions-api   Up 38 seconds             0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp
nexa-db    postgres:16-alpine   Up 43 seconds (healthy)   5432/tcp
```

## 3. INC-01 — título obrigatório (manutenção corretiva)

```console
$ curl -X POST http://localhost:8000/api/chamados/ \
       -H 'Content-Type: application/json' -d '{"descricao":"sem titulo"}'
{"titulo":["O título é obrigatório."]}
HTTP 400

$ curl -X POST ... -d '{"titulo":"   ","descricao":"titulo so com espacos"}'
{"titulo":["O título é obrigatório."]}
HTTP 400

$ curl -X POST ... -d '{"titulo":"Impressora sem tinta no 3o andar","descricao":"Setor financeiro"}'
{"id":4,"titulo":"Impressora sem tinta no 3o andar","descricao":"Setor financeiro sem impressao desde as 9h","status":"ABERTO","criado_em":"2026-09-03T17:01:12.336035-03:00","atualizado_em":"2026-09-03T17:01:12.336047-03:00"}
HTTP 201
```

A regra vale também para atualização, porque foi aplicada na camada compartilhada
(modelo + serializer) e não apenas na rota citada no relato:

```console
$ curl -X PATCH http://localhost:8000/api/chamados/1/ -d '{"titulo":""}'
{"titulo":["O título é obrigatório."]}
HTTP 400
```

## 4. INC-02 — filtro por status (manutenção evolutiva)

```console
$ curl http://localhost:8000/api/chamados/
  #4 Impressora sem tinta no 3o andar [ABERTO]
  #3 Reset de senha do sistema de RH [CONCLUIDO]
  #2 Troca de HD do servidor de arquivos [EM_ANDAMENTO]
  #1 VPN cai a cada 10 minutos [ABERTO]
  -> 4 chamado(s), HTTP 200

$ curl "http://localhost:8000/api/chamados/?status=ABERTO"
  #4 Impressora sem tinta no 3o andar [ABERTO]
  #1 VPN cai a cada 10 minutos [ABERTO]
  -> 2 chamado(s), HTTP 200

$ curl "http://localhost:8000/api/chamados/?status=EM_ANDAMENTO"
  #2 Troca de HD do servidor de arquivos [EM_ANDAMENTO]
  -> 1 chamado(s), HTTP 200

$ curl "http://localhost:8000/api/chamados/?status=concluido"   # normaliza a caixa
  #3 Reset de senha do sistema de RH [CONCLUIDO]
  -> 1 chamado(s), HTTP 200

$ curl "http://localhost:8000/api/chamados/?status=INVALIDO"
{"status":["Status inválido. Valores aceitos: ABERTO, EM_ANDAMENTO, CONCLUIDO."]}
HTTP 400
```

## 5. INC-06 — indicadores (manutenção evolutiva)

```console
$ curl http://localhost:8000/api/indicadores/
{"total":4,"abertos":2,"em_andamento":1,"concluidos":1}
HTTP 200
```

## 6. INC-07 — testes automatizados

```console
$ docker compose run --rm api python manage.py test
Found 11 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...........
----------------------------------------------------------------------
Ran 11 tests in 0.062s

OK
Destroying test database for alias 'default'...
```

## 7. INC-05 — nenhum segredo versionado

```console
$ git check-ignore -v .env
.gitignore:9:.env	.env

$ git ls-files .env | wc -l          # o .env está versionado?
0

$ grep -rn "django-insecure" --include="*.py" backend/ | wc -l   # chave antiga no código?
0
```

## 8. Persistência do volume

```console
$ docker compose down          # sem -v: o volume postgres_data é preservado
$ docker compose up -d
$ curl http://localhost:8000/api/indicadores/
{"total":4,"abertos":2,"em_andamento":1,"concluidos":1}   # dados mantidos
```

## 9. Interface web

Servida pelo próprio Django em `http://localhost:8000/`, com o painel de
indicadores e o filtro por status:

![Painel de indicadores e listagem de chamados](tela-chamados.png)
