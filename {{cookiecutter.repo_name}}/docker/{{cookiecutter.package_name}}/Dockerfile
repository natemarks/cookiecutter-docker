
FROM {{ cookiecutter.base_docker_image }}

# add credentials on build
ENV GPG_DECRYPTION_KEY 'OVERRIDE_DECRYPTION_KEY'
ENV PROJECT_DIRECTORY 'OVERRIDE_PROJECT_DIRECTORY'
ENV AWS_ACCESS_KEY_ID 'OVERRIDE_AWS_ACCESS_KEY_ID'
ENV AWS_SECRET_ACCESS_KEY 'OVERRIDE_AWS_SECRET_ACCESS_KEY'

RUN mkdir /root/.ssh/

# RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa
COPY docker /root/.ssh/docker
RUN chmod 600 /root/.ssh/docker

COPY .ssh/config /root/.ssh/config
COPY .ssh/known_hosts /root/.ssh/known_hosts

COPY decrypt_gpg_creds-0.0.1-py2.py3-none-any.whl decrypt_gpg_creds-0.0.1-py2.py3-none-any.whl


# make sure your domain is accepted
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan stash.imprivata.com >> /root/.ssh/known_hosts

RUN git clone ssh://git@stash.imprivata.com:7999/cldops/dna.git

RUN apt update -y
RUN apt upgrade -y


RUN pip install --upgrade pip
RUN pip install decrypt_gpg_creds-0.0.1-py2.py3-none-any.whl

RUN pip install -r dna/provisioning/requirements.txt
RUN pip install -r dna/misc/requirements.txt

ENTRYPOINT ["/bin/bash"]
