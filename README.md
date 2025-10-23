# Hello World App - ArgoCD Lab

Este projeto demonstra uma aplicação Python simples ("Olá Mundo") com deploy automatizado usando ArgoCD no Kubernetes, seguindo o padrão Apps of Apps.

## 📁 Estrutura do Projeto

```
argocd-lab/
├── app/                           # Código da aplicação
│   ├── app.py                     # Aplicação Flask
│   └── requirements.txt           # Dependências Python
├── Dockerfile                     # Imagem Docker
├── k8s/                          # Manifests Kubernetes
│   └── hello-world-app/
│       ├── namespace.yaml
│       ├── deployment.yaml
│       ├── service.yaml
│       └── ingress.yaml
└── argocd/                       # Configurações ArgoCD
    ├── app-of-apps.yaml          # App principal (Apps of Apps)
    └── apps/
        └── hello-world-app.yaml  # Definição da aplicação
```

## 🚀 Como Usar

### 1. Setup da Pipeline CI/CD

⚠️ **Primeiro configure a pipeline!** Veja [SETUP-PIPELINE.md](SETUP-PIPELINE.md) para configurar os secrets do GitHub Actions.

### 2. Executar Localmente (Desenvolvimento)

```bash
# Instalar dependências e executar
cd app
pip install -r requirements.txt
python app.py

# Ou com Docker
docker build -t hello-world-app:latest .
docker run -p 5000:5000 --name hello-world-app hello-world-app:latest
```

### 3. Testar Endpoints

```bash
# Testar manualmente:
curl http://localhost:5000
curl http://localhost:5000/health
curl http://localhost:5000/ready
```

### 4. Deploy Automático com CI/CD

Com a pipeline configurada, o deploy é **100% automático**:

1. **Faça um commit e push:**
```bash
git add .
git commit -m "feat: nova feature"
git push origin main
```

2. **A pipeline automaticamente:**
   - 🔨 Faz build da aplicação
   - 🐳 Cria imagem Docker com tag baseada no commit
   - 📤 Faz push para `robarros/argocd-app`
   - 📝 Atualiza o deployment.yaml
   - 🔄 ArgoCD detecta e faz deploy automático

3. **Monitore o progresso:**
   - GitHub Actions: Aba `Actions` do repositório
   - ArgoCD UI: Dashboard das aplicações
   - Kubernetes: `kubectl get pods -n hello-world`

### 5. Deploy Manual no Kubernetes com ArgoCD

#### Pré-requisitos
- Cluster Kubernetes
- ArgoCD instalado
- Repositório Git com este código

#### Passos:

1. **Faça build e push da imagem Docker:**

```bash
# Build local
docker build -t hello-world-app:latest .

# Tag para seu registry
docker tag hello-world-app:latest your-registry/hello-world-app:latest

# Push para registry
docker push your-registry/hello-world-app:latest
```

2. **Atualize a imagem no deployment:**

   Edite `k8s/hello-world-app/deployment.yaml` e substitua `hello-world-app:latest` pela imagem do seu registry.

3. **Deploy no ArgoCD:**

```bash
# Aplicar o App of Apps
kubectl apply -f argocd/app-of-apps.yaml

# Verificar aplicações no ArgoCD
kubectl get applications -n argocd
```

### 6. Acessar a Aplicação

```bash
# Via port-forward (desenvolvimento)
kubectl port-forward -n hello-world service/hello-world-service 8080:80

# Acessar: http://localhost:8080
```

```bash
# Via Ingress (produção)
# Adicionar ao /etc/hosts:
# <INGRESS_IP> hello-world.local

# Acessar: http://hello-world.local
```

## 🔧 Configurações

### Variáveis de Ambiente

- `APP_VERSION`: Versão da aplicação (default: "1.0.0")
- `PORT`: Porta da aplicação (default: 5000)
- `DEBUG`: Modo debug (default: "false")

### CI/CD Pipeline

Pipeline completa com **GitHub Actions**:

**🔄 Fluxo Automático:**
```
Commit → Build → Docker Push → K8s Update → ArgoCD Sync → Deploy
```

**🏷️ Tags Criadas:**
- `latest` - Última versão
- `stable` - Branch main apenas  
- `<commit-sha>` - Identificador único
- `<timestamp>` - Momento do build

**🛡️ Segurança:**
- Scan de vulnerabilidades com Trivy
- Multi-architecture builds (amd64/arm64)
- Secrets management com GitHub

### ArgoCD - Apps of Apps Pattern

Este projeto usa o padrão **Apps of Apps** do ArgoCD:

- **App Principal** (`app-of-apps.yaml`): Gerencia todas as aplicações
- **Apps Filhas** (`apps/`): Cada aplicação individual

**Vantagens:**
- Gerenciamento centralizado
- Facilita adição de novas aplicações
- Melhor organização e governança
- Sync automático de todas as apps

## 📊 Endpoints da API

| Endpoint | Descrição |
|----------|-----------|
| `GET /` | Retorna mensagem "Olá Mundo" com metadados |
| `GET /health` | Health check para liveness probe |
| `GET /ready` | Readiness check para readiness probe |

## 🛡️ Segurança

- Container executa como usuário não-root
- Security contexts configurados
- Resource limits definidos
- Read-only root filesystem
- Capabilities dropped

## 🔍 Monitoramento

- Health checks configurados
- Probes de liveness e readiness
- Logs estruturados
- Métricas básicas via endpoints

## 📝 Notas

- Configure seu registry de imagens Docker
- Adapte os recursos (CPU/memória) conforme necessário
- Configure ingress controller se necessário
# Pipeline corrigida
