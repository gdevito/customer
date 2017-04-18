### On Mac, locally install postgres & mongodb
```shell
brew install postgres
brew install mongodb
```
### Install pip and python deps
```shell
sudo easy_install pip
pip install -r requirements.txt
python setup.py install
```
### start postgres now and on startup
```shell
pg_ctl -D /usr/local/var/postgres start && brew services start postgresql
```
### manually run customer server
```shell
python -m customer.server
```
### run tests
```shell
pytest
```
