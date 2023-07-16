FROM    debian:11.7
ENV     container docker
STOPSIGNAL SIGRTMIN+3
VOLUME  [ "/tmp", "/run", "/run/lock" ]
WORKDIR /
RUN     rm -f /lib/systemd/system/multi-user.target.wants/* \
        /etc/systemd/system/*.wants/* \
        /lib/systemd/system/local-fs.target.wants/* \
        /lib/systemd/system/sockets.target.wants/*udev* \
        /lib/systemd/system/sockets.target.wants/*initctl* \
        /lib/systemd/system/sysinit.target.wants/systemd-tmpfiles-setup* \
        /lib/systemd/system/systemd-update-utmp*
ENV     DEBIAN_FRONTEND=noninteractive
RUN     apt-get update &&\
        apt-get install -y openssh-server sudo python3 python3-pip &&\
        apt-get clean
ARG     USER_NAME=cicerow
ARG     USER_PASS=SetStrongPass_123
ARG     ROOT_PASS=SetStrongPass_123
RUN     adduser --home /home/$USER_NAME --uid 1201 $USER_NAME &&\
        adduser $USER_NAME sudo &&\
        echo "$USER_NAME:$USER_PASS"|chpasswd &&\
        echo "root:$USER_PASS"|chpasswd
RUN     cp /etc/sudoers /etc/sudoers.orig &&\
        sed  "s/ALL=(ALL:ALL) ALL/ALL=(ALL:ALL) NOPASSWD:ALL/" /etc/sudoers.orig > /etc/sudoers
COPY    ansible_root_rsa_key.pub /root/.ssh/authorized_keys
COPY    ansible_user_rsa_key.pub /home/$USER_NAME/.ssh/authorized_keys
CMD     [ "/lib/systemd/systemd", "log-level=info", "unit=sysinit.target" ]
