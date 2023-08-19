# Example 02

This playbook is using only tasks (not role) to show an example of an application using 2 servers: the application based in Python/Flask in ansible-srv1 and a Redis server in ansible-srv2.

```
     ┌──────┐
     │ USER │
     └───┬──┘
         │
 ┌───────▼───────────┐     ┌────────────────┐
 │ APP Server        │     │REDIS Server    │
 │ TCP Port: 5001    ├────►│TCP Port:  6379 │
 │ IP: 172.18.1.1    │     │IP: 172.18.1.2  │
 │ ansible-srv1      │     │ansible-srv2    │
 │ Routes to access: │     └────────────────┘ 
 │    /add           │
 │    /list          │
 │    /del           │
 └───────────────────┘
```

This simple application only receives parameters via /add route to insert inside Redis server, list all inserted information using /list route and deletes items using /del route. The /add route needs three parameters: (1) **name** to indicate the book name, (2) **author** to indicate the author's name, (3) **borrowed_to** to indicate who borrowed the book. Other two parameters are calculated: (4) **borrowed_on** to indicate when the book was borrowed and (5) **code** used as name of the entry in Redis server (used as a primary key if we could compare). The /del route uses one parameter: the code of the Redis entry.

There are 13 tasks:
- **ansible-srv2**: Play to install Redis on server2.
  - **Updates APT Cache**: Update APT list of packages.
  - **Install Redis Requirements**: Install curl and gpg required during installing.
  - **Configure REDIS Repository**: Configure Redis APT repository via bash commands.
  - **Updates APT Cache**: Updates APT list again to include packages from new repository.
  - **Install REDIS**: Install Redis service.
  - **Configure REDIS IP**: Configure Redis to listen in ansible-srv2 IP.
  - **Configure REDIS Password**: Configure Redis to use password.
  - **Restart REDIS**: Restart Redis service after change configuration.
- **ansible-srv1**: Play to copy the source code, prepare server1 and execute application.
  - **Copy Python Files**: Copy files to ansible-srv1 server.
  - **Updates APT Cache**: Updates APT list of packages.
  - **Install Python**: Install Python binaries.
  - **Install Python Libraries for Example 02**: Install Python libraries.
  - **Execute Python Application**: Execute Python application in destination service.

To execute the playbook use the command below. 

```bash
ansible-playbook playbooks/example02.yml
```

To test the execution use the following commands:

```bash
curl http://172.18.1.1:5001/add?name=Book+Name&author=Author+Name&borrowed_to=Friend+Name
curl http://172.18.1.1:5001/add?name=Book+Two&author=Author+Two&borrowed_to=Friend+Two
curl http://172.18.1.1:5001/list
curl http://172.18.1.1:5001/del?code=BOOK1
curl http://172.18.1.1:5001/list
```

To stop the application in the destination server run the following command:

```bash
ansible-playbook playbooks/example02_erase.yml
```
