# Example 01

This playbook is using only tasks (not roles) to make the example simpler.

There are six tasks:
- **Debug VARS**: show the vars used in the playbook (only to prove the concept).
- **Updates APT Cache**: updates the APT list of packages.
- **Install Python**: installs python3, python3-pip and python3-dev packages.
- **Install Python Libraries for Example 01**: installs libraries used by example 01.
- **Copy Python Files**: copies the code of the application to the server.
- **Execute Python Application**: executes the application in the background.

To execute the playbook use the command below. 

```bash
ansible-playbook playbooks/example01.yml
```

To test the execution use the following command:

```bash
curl http://172.18.1.1:5000/cipher?text=example+of+text+to+cipher
```

To validate the answer of the first test you can run:

```bash
curl http://172.18.1.1:5000/cipher?text=oximtno+ef+poxp+pe+cathos
```

To stop the application from in the destination server run the following command:

```bash
ansible-playbook playbooks/example01.yml
```

## The tenispolar Application

TenisPolar is a cipher from Pedro Bandeira's books.

In the books, a club of teenagers use a substitution cipher replacing letters of `tenis` by letters of `polar` word and vice-versa. This is not a serious cipher in computational terms, but a good way to practice.

This code uses Flask to offer to the clients an 
endpoint to access the service.
