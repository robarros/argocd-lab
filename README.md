# Hello World App - ArgoCD Lab

Este projeto demonstra uma aplicação Python simples ("Olá Mundo") com deploy automatizado usando ArgoCD no Kubernetes, seguindo o padrão Apps of Apps.

## 📁 Estrutura do Projeto

```
# Laboratório de GitOps com Argo CD

Este repositório contém um projeto de exemplo para demonstrar o uso do Argo CD com o padrão "App of Apps" para gerenciar múltiplas aplicações em um cluster Kubernetes.

## Arquitetura

A abordagem utilizada é o **GitOps**, onde o repositório Git é a única fonte da verdade para o estado desejado do nosso cluster. O Argo CD é a ferramenta que sincroniza esse estado.

O projeto utiliza o padrão **App of Apps**:
1.  Uma aplicação "raiz" (`app-of-apps`) é criada no Argo CD.
2.  Esta aplicação raiz tem a responsabilidade de monitorar o diretório `argocd/` deste repositório.
3.  Qualquer manifesto de `Application` do Argo CD adicionado ao diretório `argocd/` será automaticamente detectado e implantado pelo Argo CD, criando assim "aplicações filhas".

## Estrutura de Diretórios

```
.
├── Dockerfile              # Dockerfile para a aplicação Python de exemplo
├── app/                    # Código-fonte da aplicação "hello-world"
│   ├── app.py
│   └── requirements.txt
├── argocd/                 # Manifestos de Application do Argo CD (aplicações filhas)
│   ├── hello-world-app.yaml
│   └── nginx-app.yaml
├── bootstrap/              # Aplicação raiz (App of Apps)
│   └── app-of-apps.yaml
├── k8s/                    # Manifestos Kubernetes para cada aplicação
│   ├── hello-world-app/
│   └── nginx/
└── README.md
```

## Pré-requisitos

-   Um cluster Kubernetes (ex: Minikube, Kind, Docker Desktop).
-   `kubectl` instalado e configurado para acessar seu cluster.
-   Argo CD instalado no cluster.

## Como Iniciar

### 1. Instalação do Argo CD

Se você ainda não tem o Argo CD instalado, siga os passos abaixo.

```bash
# Cria o namespace para o Argo CD
kubectl create namespace argocd

# Aplica os manifestos de instalação do Argo CD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 2. Deploy do App of Apps

Para iniciar o processo de GitOps, aplique a aplicação raiz no seu cluster. Ela irá instruir o Argo CD a gerenciar as demais aplicações.

```bash
kubectl apply -f bootstrap/app-of-apps.yaml
```

Após aplicar este comando, o Argo CD irá:
1.  Criar a aplicação `apps-of-apps`.
2.  Sincronizar essa aplicação, que por sua vez lerá o diretório `argocd/`.
3.  Criar as aplicações `hello-world-app` e `nginx`.
4.  Sincronizar estas duas aplicações, fazendo o deploy dos seus respectivos recursos (Deployments, Services, etc.) no cluster.

Você pode acompanhar o status pela UI do Argo CD ou via linha de comando.

## Como Adicionar uma Nova Aplicação

Para adicionar uma nova aplicação gerenciada por este fluxo de GitOps, siga os passos:

1.  **Crie os manifestos Kubernetes:** Adicione os manifestos da sua nova aplicação em um novo subdiretório dentro de `k8s/`.
    ```
    k8s/
    ├── ...
    └── nova-app/
        ├── deployment.yaml
        └── service.yaml
    ```

2.  **Crie a Application do Argo CD:** Crie um novo arquivo YAML no diretório `argocd/` que defina a `Application` para o Argo CD. Use os arquivos existentes como modelo, ajustando o `metadata.name` e o `spec.source.path`.
    ```yaml
    # argocd/nova-app.yaml
    apiVersion: argoproj.io/v1alpha1
    kind: Application
    metadata:
      name: nova-app
      namespace: argocd
    spec:
      project: default
      source:
        repoURL: https://github.com/robarros/argocd-lab.git # URL do seu repositório
        targetRevision: HEAD
        path: k8s/nova-app # Caminho para os manifestos da nova app
      destination:
        server: https://kubernetes.default.svc
        namespace: nova-app # Namespace onde a app será criada
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
    ```

3.  **Commit e Push:** Adicione os novos arquivos ao Git e envie para o repositório.
    ```bash
    git add .
    git commit -m "feat: Adiciona a nova-app"
    git push
    ```

O Argo CD detectará automaticamente a nova `Application` no diretório `argocd/` e iniciará o deploy da sua nova aplicação.
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

**🏷️ Tag Criada:**
- `<commit-sha>` - Identificador único do commit (ex: `abc1234`)

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
