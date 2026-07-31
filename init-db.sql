CREATE USER mlops_user WITH PASSWORD 'mlops_pass';
CREATE DATABASE mlflowdb;
GRANT ALL PRIVILEGES ON DATABASE mlflowdb TO mlops_user;