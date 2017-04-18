
## Installs
### On Mac, locally install postgres & mongodb

brew install postgres
brew install mongodb

### Install pip and python deps
sudo easy_install pip
pip install -r requirements.txt
python setup.py install

### start postgres now and on startup
pg_ctl -D /usr/local/var/postgres start && brew services start postgresql

### manually run customer server
python -m customer.server

### run tests
pytest




postgres=# CREATE TABLE customers(uid INTEGER, f_name VARCHAR(100), an_income INTEGER, addr VARCHAR(100), dt_created DATE);
