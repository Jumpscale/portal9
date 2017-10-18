# install portal
branch=${1:-master}
js9 "j.tools.prefab.local.web.portal.install(branch='${branch}')"

pip3 install -e .
