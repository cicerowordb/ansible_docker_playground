# Ansible + Docker Playground

This repository demonstrates how to create an environment based on Docker for practicing Ansible. [Ansible](https://www.ansible.com/) is an open-source automation tool that simplifies configuration management and application deployment.

We can avoid the need for virtual machines and save system resources by using Docker containers as servers. Docker containers consume fewer resources, including CPU, memory, and disk space, compared to virtual machines.

The Dockerfile in this repository creates an image with SSH and SystemD support, allowing us to simulate servers and install services using Ansible. This image also supports passwordless sudo to ease the manipulation of privileged commands.

Even addressing an environment for practicing, this repository shows a secure way to deploy containers with SSH access. This is one of the best ways to secure access to servers exposed on the Internet. 

## Requirements

- Docker default installation.
- Docker build kit (export DOCKER_BUILDKIT=1) (optional).
- SSH client installation.

## Create SSH Keys

To ensure the most secure way to access your environment, it is recommended creating SSH keys and save them in your images. Keep the private keys in a secure storage location while distributing the corresponding public keys in the Docker image.

```bash
ssh-keygen -P "" -t rsa  -b 4096 -C "root@server.local" -f ansible_root_rsa_key
ssh-keygen -P "" -t rsa  -b 4096 -C "user@server.local" -f ansible_user_rsa_key
```

## Create Docker Network

To have better control over the IP addresses assigned to each container/server, it is necessary to create a network using a different IP range. Docker already uses the 172.17.0.0/16 range by default, so we recommend using the next available block.

```bash
docker network create \
    --subnet 172.18.0.0/16 \
    --gateway 172.18.0.1 \
    --driver bridge \
    ansible-net
```

## Build Image

You can simply create an image with default options. If you Dockerfile is protected you can set the arguments (USER_NAME, USER_PASS, ROOT_PASS) with the appropriated values. It takes some minutes (almost 10 in my tests) depending of your computer resources.

```bash
docker build -t ansible-srv .
```

But the most secure way is set the arguments in build command without save in commands history:

```bash
  docker build -t ansible-srv \
  --build-arg USER_NAME=cicerow \
  --build-arg USER_PASS=YourStrongPass_123 \
  --build-arg ROOT_PASS=YourStrongPass_123 .
```

## Run Containers

To run the servers, use the following for loop. In this example, the command will create two servers. You can change the number in the first line to set the required number of servers you need. Each server will take one IP following the sequence: 172.18.1.1, 172.18.1.2, and so on. All these servers publish the TCP/22 port using a mapping like: 0.0.0.0:32769->22/tcp. 

```bash
for x in {1..2}
do
  docker run --name ansible-srv$x \
    --detach \
    --privileged \
    --cap-add SYS_ADMIN \
    --security-opt seccomp=unconfined \
    --cgroup-parent docker.slice \
    --cgroupns private \
    --net ansible-net \
    --ip 172.18.1.$x \
    --dns 1.1.1.1 \
    --hostname ansible-srv$x \
    --publish 22 \
    ansible-srv
done
```

List all containers and check the IP to make sure is everything all right.

```bash
for x in {1..2}
do
  echo -n "ansible-srv$x = "
  docker inspect -f \
    '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' \
    ansible-srv$x
done
```

## Test Access

To test if SSH access is working use these commands. The first line tests access using root account and second tests access using a common account.

```bash
ssh -o "StrictHostKeyChecking no" -i ansible_root_rsa_key root@172.18.1.1
ssh -o "StrictHostKeyChecking no" -i ansible_user_rsa_key cicerow@172.18.1.1
```

## Test SystemD

To test if SystemD is working use the following command. The command lists all services and other resources controlled by SystemD.

```bash
docker container exec -it ansible-srv1 systemctl
```

## Remove All

To remove all components used in this installation run the commands below. They will remove the containers, the image and the network.

```bash
for x in ansible-srv{1..2}
do
  docker rm --force $x
done
docker image rm ansible-srv
docker network rm ansible-net
```


# Ansible configuration

To install Ansible use the command recommended to your operating system or distribution. For Ubuntu and other Debian derivatives, you can use the following command. You can use Python to install Ansible too. Check the [documentation](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) if needed.


```bash
sudo apt install ansible
```

To create a new hosts file use the following commands. We are creating a group with all servers and include name and IP. In the **group_vars/ansible_servers.yml** file there are other variables. 

```bash
echo '# Hosts configuration
[ansible_servers]' > hosts
for x in {1..2}
do 
  echo "ansible-srv$x ansible_host=172.18.1.$x" >> hosts
done
echo "" >> hosts
```

The configuration  in **group_vars/ansible_servers.yaml** is applied to all servers in the group with the same name in **hosts** file and shows four configurations:

- **ansible_ssh_private_key_file**: indicates the authentication file.
- **ansible_ssh_common_args**: indicates arguments used in the SSH client access.
- **ansible_port**: indicates the SSH TCP port.
- **ansible_shell_executable**: indicates the default shell command to execute in the servers.


To test communication with all servers use a command to check uptime and to check location of Python interpreter (it must be the same path used in ansible.cfg):

```bash
ansible -m shell -a "uptime" ansible_servers
ansible -m shell -a "which python3" ansible_servers
```

## Examples

Check some examples in **playbooks** folder:
- **example01.yaml**: uses one server to run a simple Python/Flask application that executes the tenispolar cipher. Check more information in the **[example01.md](playbooks/example01.md)** file.
- **example02.yaml**: uses two servers to run a simple Python/Flask application inside ansible-srv1 and a Redis server inside ansible-srv2. Check more information in the **[example02.md](playbooks/example02.md)** file.

## Run inside Kubernetes

This code was tested in a GKE cluster with a successful installation of PostgreSQL. To run this code inside a Kubernetes cluster build the image and create a Pod like the following example:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: ansible-srv
  labels:
    app: ansible-srv
spec:
  containers:
  - name: ansible-srv
    image: systemd-container:latest
    securityContext:
      privileged: true
      capabilities:
        add:
        - SYS_ADMIN
  dnsPolicy: ClusterFirst
```

If you need to create a NetworkPolicy check this example:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-systemd-container-egress
spec:
  egress: 
  - {}
  podSelector:
    matchLabels:
      app.kubernetes.io/name: systemd-container
  policyTypes:
  - Egress
---
apiVersion: v1
kind: Pod
metadata:
  labels:
    app.kubernetes.io/name: systemd-container
  name: systemd-container
spec:
  containers:
  - name: systemd-container
    image: systemdcontainer:latest
    securityContext:
      privileged: true
      capabilities:
        add:
        - SYS_ADMIN
  dnsPolicy: ClusterFirst
```

##  Known issues:
- This environment runs containers in privileged mode as root, which is acceptable only for testing and learning purposes. Include USER instruction in your Dockerfile to avoid this.
- Please note that it does not work in WSL (Windows Subsystem for Linux) due to the requirement of cgroupv2. If you wish to use it in WSL, you should first install [WSL SystemD support](https://devblogs.microsoft.com/commandline/systemd-support-is-now-available-in-wsl/).
- The SSH test command uses the option **StrictHostKeyChecking no** to avoid a prompt for initial access. Feel free to change this behavior if desired or if more secure environment is demanded.
- If you remove a container and create it again, the SSH client will display a warning indicating a change in the remote host identification. This is normal as a new key (and fingerprint) is created for the hosts.
- If you receive a warning like presented in image1, you have to downgrade your Jinja2 library ```python3 -m pip install Jinja2==3.0``` to version 3.0.

![Image1 - Warning about Jinja version](images/image1.png)

*Image1 - Warning about Jinja version*


## References

- [https://serverfault.com/questions/1053187/systemd-fails-to-run-in-a-docker-container-when-using-cgroupv2-cgroupns-priva](https://serverfault.com/questions/1053187/systemd-fails-to-run-in-a-docker-container-when-using-cgroupv2-cgroupns-priva)
- [https://medium.com/swlh/docker-and-systemd-381dfd7e4628](https://medium.com/swlh/docker-and-systemd-381dfd7e4628)
- [https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

