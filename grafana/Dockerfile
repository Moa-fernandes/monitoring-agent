FROM grafana/grafana:latest

# Copia as configurações para dentro do container
COPY provisioning /etc/grafana/provisioning
COPY dashboards /var/lib/grafana/dashboards

# Expondo a porta do Grafana
EXPOSE 3000
