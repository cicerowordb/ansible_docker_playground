## Exemplo 02

Este playbook usa apenas tasks (nenhuma role) para mostrar um exemplo de uma aplicação usando 2 servidores: a aplicação baseada em Python/Flask no ansible-srv1 e um Redis server em ansible-srv2.

```
     ┌─────────┐
     │ USUÁRIO │
     └───┬─────┘
         │
 ┌───────▼───────────────┐     ┌──────────────────┐
 │ Servidor de Aplicação │     │ REDIS Server     │
 │ Porta TCP: 5001       ├────►│ Porta TCP:  6379 │
 │ IP: 172.18.1.1        │     │ IP: 172.18.1.2   │
 │ ansible-srv1          │     │ ansible-srv2     │
 │ Rotas para acessar:   │     └──────────────────┘ 
 │    /add               │
 │    /list              │
 │    /del               │
 └───────────────────────┘
```

Esta simples aplicação apenas recebe os parâmetros via rota /add para inserir dentro de um servidor Redis, lista todas as informações inseridas usando a rota /list e apaga itens usando a rota /del. A rota /add precisa de três parâmetros: (1) **name** para indicar o nome do livro, (2) **author** para indicar o nome do autor, e (3) **borrowed_to** para indicar quem pegou o livro emprestado. Outros dois parâmetros são calculados: (4) **borrowed_on** para indicar quando o livro foi emprestado e (5) code usado como nome da entrada no servidor Redis (usado como uma chave primária se pudermos comparar). A rota /del usa um parâmetro: o código da entrada no Redis.

Existem 13 tasks:
- **ansible-srv2**: Play para instalar o Redis no servidor2.
  - **Updates APT Cache**: Atualiza a lista de pacotes do APT.
  - **Install Redis Requirements**: Instala o curl e o gpg necessários durante a instalação.
  - **Configure REDIS Repository**: Configura o repositório APT do Redis via comandos bash.
  - **Updates APT Cache**: Atualiza a lista do APT novamente para incluir os pacotes do Redis.
  - **Install REDIS**: Instala o serviço do Redis.
  - **Configure REDIS IP**: Configura o Redis para ouvir no PI de ansible-srv2.
  - **Configure REDIS Password**: Configura o Redis para usar senha.
  - **Restart REDIS**: Reinicia o serviço do Redis após a mudança na configuração.
- **ansible-srv1**: Play para copiar o código fonte, preparar o servidor 1 e executar a aplicação.
  - **Copy Python Files**: Copia os arquivos para o servidor ansible-srv1.
  - **Updates APT Cache**: Atualiza a lista de pacotes do APT.
  - **Install Python**: Instala os binários do Python.
  - **Install Python Libraries for Example 02**: Instala as bibliotecas do Python.
  - **Execute Python Application**: Executa a plicação Python no servidor de destino.

Para executar esse playbook use o comando a seguir:

```bash
ansible-playbook playbooks/example02.yml
```

Para testar a aplicação use os comandos a seguir:

```bash
curl http://172.18.1.1:5001/add?name=Book+Name&author=Author+Name&borrowed_to=Friend+Name
curl http://172.18.1.1:5001/add?name=Book+Two&author=Author+Two&borrowed_to=Friend+Two
curl http://172.18.1.1:5001/list
curl http://172.18.1.1:5001/del?code=BOOK1
curl http://172.18.1.1:5001/list
```

Para parar a applicação no servidor de destino rode o comando a seguir:

```bash
ansible-playbook playbooks/example02_erase.yml
```
