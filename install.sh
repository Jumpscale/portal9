#for development mode
apt-get install -y  libsnappy-dev
pip3 install -e .

js9 'j.tools.prefab.get().apps.portal.install()'
