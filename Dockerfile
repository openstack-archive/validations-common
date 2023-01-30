FROM redhat/ubi9:latest

LABEL name="Validations common development container file"
LABEL version="1.1"
LABEL description="Provides environment for development of new validations."

RUN dnf install -y git python3-pip gcc python3-devel jq

# Copy contents of the local validations-common repo with all of our changes
COPY . /root/validations-common
# validations-libs repo is cloned
RUN git clone https://opendev.org/openstack/validations-libs /root/validations-libs

# Install wheel, validations-libs, validations-common, pytest and all dependencies
RUN python3 -m pip install wheel &&\
    python3 -m pip install /root/validations-common &&\
    python3 -m pip install -r /root/validations-common/test-requirements.txt &&\
    python3 -m pip install pytest &&\
    python3 -m pip install /root/validations-libs

# Setting up the default directory structure for both ansible,
# and the VF
RUN ln -s /usr/local/share/ansible  /usr/share/ansible &&\
    mkdir -p /var/log/validations
# Simplified ansible inventory is created, containing only localhost,
# and defining the connection as local.
RUN mkdir -p /etc/ansible && \
    echo "localhost ansible_connection=local" > /etc/ansible/hosts
