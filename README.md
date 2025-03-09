# Monitoring Agent - DevOps RNP 

Este projeto é um **agente de monitoramento** que coleta métricas de rede, incluindo latência, tempo de carregamento de páginas web e códigos de status HTTP. Além disso, consome dados da API ViaIpe para análise de disponibilidade e uso de banda. Todos os dados são armazenados em um banco de dados PostgreSQL e visualizados através de dashboards no Grafana.

##  Objetivo
- Monitorar latência e disponibilidade de sites estratégicos (Google, YouTube, RNP)
- Coletar métricas da API ViaIpe
- Armazenar os resultados em um banco de dados PostgreSQL
- Criar dashboards no Grafana para análise e visualização dos dados

---

##  Arquitetura do Projeto
O projeto segue uma abordagem baseada em **containers Docker**, garantindo escalabilidade e fácil replicação. Os principais componentes são:

###  **1. Agente de Monitoramento (monitoring_agent)**
- Coleta latência, tempo de carregamento e código de status HTTP das seguintes páginas:
  - `google.com`
  - `youtube.com`
  - `rnp.br`
- Insere os dados no PostgreSQL.

###  **2. Coletor ViaIpe (viaipe_collector)**
- Consome dados da API **[https://viaipe.rnp.br/api/norte](https://viaipe.rnp.br/api/norte)**
- Realiza cálculos de **disponibilidade média**, **uso de banda** e **qualidade do serviço**
- Armazena os resultados no banco PostgreSQL.

###  **3. Banco de Dados (PostgreSQL - monitoring_db)**
- Contém as tabelas `network_monitor` e `viaipe_monitor` para armazenar os dados coletados.

###  **4. Grafana (monitoring_grafana)**
- Visualização dos dados em **dashboards interativos**
- Permite análise de padrões de disponibilidade e latência

---

##  Estrutura do Banco de Dados

### **Tabela: `network_monitor`** (Monitoramento Web)
| Campo         | Tipo          | Descrição                                    |
|--------------|--------------|---------------------------------------------|
| `id`        | SERIAL       | Chave primária                              |
| `host`      | TEXT         | Nome do site monitorado                     |
| `latency`   | FLOAT        | Tempo de resposta em ms                     |
| `load_time` | FLOAT        | Tempo de carregamento da página (ms)        |
| `status_code` | INTEGER    | Código de resposta HTTP (ex: 200, 404)      |
| `timestamp` | TIMESTAMP    | Data e hora da coleta                       |

### **Tabela: `viaipe_monitor`** (Coleta ViaIpe)
| Campo         | Tipo          | Descrição                                    |
|--------------|--------------|---------------------------------------------|
| `id`        | SERIAL       | Chave primária                              |
| `availability` | FLOAT     | Disponibilidade média (%)                   |
| `bandwidth` | FLOAT        | Consumo médio de banda (Mbps)               |
| `timestamp` | TIMESTAMP    | Data e hora da coleta                       |

---

##  Como Executar o Projeto

### **1️ Clonar o repositório**
```sh
git clone https://github.com/seu-usuario/monitoring-agent.git
cd monitoring-agent
```

### **2️ Subir os containers**
```sh
docker-compose up -d --build
```
Isso iniciará os serviços **PostgreSQL, Grafana, Agente de Monitoramento e Coletor ViaIpe**.

### **3️ Acessar o Grafana**
 Abra no navegador: **[http://localhost:3000](http://localhost:3000)**
- Usuário: `admin`
- Senha: `admin`

### **4️ Verificar se os dados estão sendo coletados**
```sh
docker exec -it monitoring_db psql -U user -d monitoring -c "SELECT * FROM network_monitor LIMIT 5;"
```
```sh
docker exec -it monitoring_db psql -U user -d monitoring -c "SELECT * FROM viaipe_monitor LIMIT 5;"
```
Se os dados aparecerem, significa que a coleta está funcionando corretamente. ✅

### **5️ Acessar os dashboards no Grafana**
- No menu lateral, vá para **"Dashboards"** e selecione o dashboard desejado.

---

## 🔍 Troubleshooting (Solução de Problemas)

### **Erro: Grafana não conecta ao PostgreSQL**
Verifique se o banco está acessível a partir do container do Grafana:
```sh
docker exec -it monitoring_grafana psql -h monitoring_db -U user -d monitoring -c "\dt"
```
Se houver erro de conexão, pode ser necessário editar a configuração do PostgreSQL e reiniciar os containers.

### **Erro: Nenhum dado aparece no Grafana**
1. Verifique se os scripts de coleta estão rodando:
```sh
docker logs monitoring_agent --tail 50
docker logs viaipe_collector --tail 50
```
2. Verifique se os dados estão sendo inseridos corretamente no PostgreSQL.
3. Atualize as queries no Grafana para o intervalo correto de tempo.

### **Erro: Banco de dados não responde**
Reinicie o banco:
```sh
docker restart monitoring_db
```

---

##  Estrutura do Projeto

📂 monitoring-agent
├── 📁 agent   # Coletor de latência e status HTTP
├── 📁 viaipe_collector   # Coletor de dados ViaIpe
├── 📁 grafana           # Dashboards e configuração do Grafana
├── 📁 postgres          # Banco de dados PostgreSQL
├── 📄 docker-compose.yml  # Orquestração dos serviços
├── 📄 README.md          # Documentação do projeto
```

---

## 📬 Contato
📧 Email: **moacirsistemax@gmail.com**

