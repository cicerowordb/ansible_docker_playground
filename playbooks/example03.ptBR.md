# Exemplo 03

Este exemplo usa Docker-in-Docker e funciona bem no WSL. Também usa roles e `set_fact` no lugar de `vars`

"Ansible facts são informações (dados do sistema e propriedades) coletadas dos nós alvo e enviadas para o nó de controle." [referência](https://www.redhat.com/sysadmin/playing-ansible-facts) Usando set_fact o administrador pode adicionar outras informações ao conjunto do Ansible facts de cada host. Com `cacheable: no` os facts adicionados aos hosts ficam disponíveis para todos os plays dentro do mesmo playbook. Se for modificado para `yes` os valores são salvos entre as execuções utilizando um cache de facts.

Roles são sequências de tasks adicionadas aos playbooks para promover o reúso. Neste exemplo, temos as roles `install_docker_single_mode` para instalar o serviço do Docker nos hosts do Ansible e `create_container_redis` para criar um container rodando a stack do Redis. Todos os outros passos usam tasks. Todas as roles precisam ser armazenadas na pasta `roles` usando essa estrutura:

```
playbooks/roles/
├── create_container_redis
│   └── tasks
│       └── main.yml
└── install_docker_single_mode
    └── tasks
        └── main.yml
```

O diretório `roles` tem de estar no mesmo nível dos arquivos de playbook. O nome do diretório dentro de roles dá nome à role. Um arquivo com o nome `main.yml` dentro da pasta tasks contém todas as tasks.

## Install Docker Single Mode

Esta role instala o Docker e tem oito tasks:

- **Install Aptitude**: Garante que a última versão do Aptitude esteja instalada.
- **Install Required System Packages**: Instala os pacotes usados durante a instalação do Docker.
- **Add Docker GPG APT Key**: Adiciona a chave GPG do repositório do Docker à configuração do APT.
- **Check Debian/Ubuntu Codename**: Pega o correto codename de distribuições Debian e Ubuntu.
- **Add Docker Repository**: Adiciona o repositório do Docker à configuração do ATP.
- **Update APT and Install docker-ce**: Atualiza o APT e instala o Docker Community Edition.
- **Start Docker Service**: Inicia o serviço do Docker e garante que esteja rodando.
- **Install PIP Library to Ansible Docker Modules**: Instala a biblioteca PIP usada pelos módulos Ansible do Docker e outras configurações.

Nenhum fact ou variável foi usada nessa role.

## Create Container Redis

Esta role cria um container rodando o Redis. Ela usa quatro facts como variáveis:

- **redis_service_port**: Porta TCP usada pelo serviço.
- **redis_insight_port**: Porta TCP usada pelo painel web.
- **redis_default_password**: A senha usada por padrão.
- **redis_server_volume_path**: O volume usado para preservar os dados do Redis.

A role tem três tasks:

- **Create Redis Data Directory**: Cria o diretório para armazenar os dados do Redis.
- **Pull Redis Image From Docker Hub**: Carrega a image do Docker Hub (isso pode tomar muito tempo de acordo com a velocidade da sua conexão de Internet).
- **Start/Restart a Redis Container**: Inicia um container Redis rodando a Redis Stack com a configuração indicada.

## Outros Passos

Todos os outros passos usam tasks no lugar de roles. Isso pode ser justificado já que todos esses passos são específicos para o código usado no terceiro exemplo. Então, eles possuem baixo potencial de reúso.

Os próximos passos são:

- **Create Application Code Zip File**: Cria o arquivo zip com o conteúdo do código na máquina do administrador.
- **Create Application Directory**: Cria um diretório para receber o código da aplicação e para ser utilizado como um volume.
- **Send the Application Code Zip file**: Extrai o arquivo zio para dentro do diretório da aplicação.
- **Download Application Base Container**: Baixa a imagem usada pela aplicação (pode tomar muito tempo).
- **Create Application Container**: Inicia o container com a nova applicação e todos os comandos necessários.

Esses passos poderiam ser facilmente adaptados para usar um commando `git clone` no lugar de um arquivo zip. Mas aqui desejo manter todos os arquivos necessários em um único repositório.
