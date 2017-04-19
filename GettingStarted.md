### On Mac, locally install postgres & mongodb
```shell
brew install postgres
brew install mongodb
```
### Install pip and python deps
```shell
sudo easy_install pip
sudo pip install -r requirements.txt
sudo python setup.py install
```
### start postgres now and on startup
```shell
pg_ctl -D /usr/local/var/postgres start && brew services start postgresql
```
### start mongodb, using brew services on mac
```shell
mkdir -p /data/db
sudo chown -R `id -un` /data/db
brew tap homebrew/services
brew services start mongodb
```
### manually run customer server as same user did installs
```shell
python -m customer.server
```
### run tests
```shell
pytest customer/test/test_customer.py
```
