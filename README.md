#  Monitoring Agent - Dashboard com Grafana, PostgreSQL e Docker

##  **Descrição do Projeto**
Este projeto tem como objetivo monitorar a latência de sites e coletar estatísticas da plataforma ViaIpe. Os dados são armazenados em um banco de dados PostgreSQL e visualizados através de dashboards no Grafana.

##  **Tecnologias Utilizadas**
- **Python** (Coleta e processamento de dados)
- **PostgreSQL** (Armazenamento de dados)
- **Grafana** (Visualização dos dados)
- **Docker & Docker Compose** (Gerenciamento dos containers)

##  **Como Executar o Projeto**

### **1 Clonar o repositório**
```sh
git clone <URL_DO_REPOSITORIO>
cd monitoring-agent
```

### **2 Subir os containers**
```sh
docker-compose up -d
```
Isso iniciará os seguintes containers:
- `monitoring_agent` - Coleta a latência dos sites e armazena no banco.
- `viaipe_collector` - Obtém estatísticas da API ViaIpe e armazena no banco.
- `monitoring_db` - Banco de dados PostgreSQL.
- `monitoring_grafana` - Interface para visualização dos dados.

### **3 Acessar os dashboards no Grafana**
Abra o navegador e acesse:
```
http://localhost:3000
```
- **Usuário:** `admin`
- **Senha:** `admin` (ou a senha configurada no `docker-compose.yml`)

##  **Banco de Dados**
O banco PostgreSQL possui duas tabelas principais:

### **1 network_monitor** (Monitoramento de sites)
| id  | timestamp  | host   | latency | load_time | status_code |
|-----|------------|--------|---------|------------|-------------|
| 1   | 2025-03-11 13:03:53 | rnp.br  | 13.7    | 234  | 200 |
| 2   | 2025-03-11 13:03:52 | youtube.com | 18.5    | 612  | 200 |
| 3   | 2025-03-11 13:03:52 | google.com  | 16.0    | 606  | 200 |

### **2 viaipe_monitor** (Disponibilidade e Banda - ViaIpe)
| id  | timestamp  | availability | bandwidth |
|-----|------------|--------------|------------|
| 1   | 2025-03-11 12:54:50 | 1.15  | 21694651 |
| 2   | 2025-03-11 12:55:02 | 1.15  | 21694651 |
| 3   | 2025-03-11 12:56:02 | 1.15  | 21690665 |

##  **Prints dos Dashboards**
### **1 Latência dos Sites Monitorados**
![Latência dos Sites Monitorados](./LatenciaGrafana.PNG)

### **2 Disponibilidade e Banda (ViaIpe)**
![Disponibilidade e Banda - ViaIpe](./ViaIpedisponibilidadeebanda.png)





## 📬 Contato
📧 Email: **moacirsistemax@gmail.com**

