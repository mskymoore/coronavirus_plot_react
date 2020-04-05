# To generate certs:
## on docker host:
```
sudo apt install letsencrypt
chown -R admin:admin /etc/letsencrypt

# need port 80 available
certbot certonly --standalone -d ncov.1337.rip

# see docker-compose for how nginx accesses these certs

# for auto renewal
crontab -e

# put this:
docker_compose_file='/home/admin/corona_plot_web/docker-compose.yml'
certbot renew --pre-hook "docker-compose -f $docker_compose_file down" --post-hook "docker-compose -f $docker_compose_file up -d"
```