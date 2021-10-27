docker-compose down

docker volume rm ac-search-dev_static-data

docker-compose up -d --build --force-recreate