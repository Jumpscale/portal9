#for development mode
apt-get install -y  libsnappy-dev
pip3 install -e .


GIGBRANCH=${GIGBRANCH:-master}
# install portal:
js9 'j.tools.prefab.get().apps.portal.install(branch=${GIGBRANCH})'
