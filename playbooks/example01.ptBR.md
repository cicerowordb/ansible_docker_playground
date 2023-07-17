# Exemplo 01

Este playbook está usando apenas tarefas (não funções) para tornar o exemplo mais simples.

São seis tarefas:
- **Debug VARS**: mostra as variáveis usadas no playbook (apenas para provar o conceito).
- **Atualiza Cache APT**: atualiza a lista de pacotes APT.
- **Instalar Python**: instala os pacotes python3, python3-pip e python3-dev.
- **Install Python Libraries for Example 01**: instala as bibliotecas usadas pelo exemplo 01.
- **Copy Python Files**: copia o código da aplicação para o servidor.
- **Execute Python Application**: executa o aplicativo em segundo plano.

Para executar o playbook use o comando abaixo.

```bash
ansible-playbook playbooks/example01.yml
```

Para testar a execução use o seguinte comando:

```bash
curl http://172.18.1.1:5000/cipher?text=example+of+text+to+cipher
```

Para validar a resposta do primeiro teste, você pode executar:

```bash
curl http://172.18.1.1:5000/cipher?text=oximtno+ef+poxp+pe+cathos
```

Para parar o aplicativo no servidor de destino, execute o seguinte comando:

```bash
ansible-playbook playbooks/example01.yml
```

## A aplicação tenispolar

TenisPolar é uma cifra dos livros de Pedro Bandeira.

Nos livros, um clube de adolescentes usa uma cifra de substituição trocando as letras de `tenis` por letras da palavra `polar` e vice-versa. Esta não é uma cifra séria em termos computacionais, mas uma boa maneira de praticar.

Este código utiliza Flask para oferecer aos clientes um
endipoint para acessar o serviço.
