# GitHub Actions Setup

Este documento explica como configurar os secrets necessários para a pipeline CI/CD funcionar corretamente.

## 🔐 Configurações Necessárias

### 1. Permissões do GitHub Actions

⚠️ **IMPORTANTE**: Primeiro habilite as permissões do GitHub Actions:

1. Acesse: `Settings` → `Actions` → `General`
2. Em **Workflow permissions**, selecione: `Read and write permissions`
3. Marque: `Allow GitHub Actions to create and approve pull requests`
4. Clique em **Save**

### 2. Secrets Necessários

Acesse: `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

**DOCKER_USERNAME**
```
robarros
```

**DOCKER_PASSWORD**
```
<seu-docker-hub-token-ou-senha>
```

### 2. Como criar Docker Hub Token (Recomendado)

1. Acesse [Docker Hub](https://hub.docker.com/)
2. Vá em `Account Settings` → `Security` → `Access Tokens`
3. Clique em `New Access Token`
4. Nome: `GitHub Actions argocd-lab`
5. Permissions: `Read, Write, Delete`
6. Copie o token gerado e use como `DOCKER_PASSWORD`

## 🚀 Como a Pipeline Funciona

### Triggers
- **Push** para branches `main` ou `develop`
- **Pull Requests** para `main`

### Processo Automático

1. **Build & Test**
   - Checkout do código
   - Setup Python 3.11
   - Instalação das dependências
   - Teste básico da aplicação

2. **Docker Build & Push**
   - Geração de tags baseadas no commit SHA
   - Build multi-arquitetura (amd64/arm64)
   - Push para `robarros/argocd-app` com múltiplas tags:
     - `latest` (sempre)
     - `stable` (apenas branch main)
     - `<commit-sha>` (identificador único)
     - `<timestamp>` (momento do build)

3. **Kubernetes Update**
   - Atualização automática do `deployment.yaml`
   - Commit das mudanças (apenas branch main)
   - ArgoCD detecta automaticamente as mudanças

4. **Security Scan**
   - Scanner Trivy para vulnerabilidades
   - Upload dos resultados para GitHub Security

## 📊 Tag Criada

Exemplo para commit `abc1234`:
```
robarros/argocd-app:abc1234
```

Apenas uma tag é criada por commit, baseada no SHA do commit para identificação única.

## 🔄 Fluxo ArgoCD

1. Pipeline atualiza o `deployment.yaml` com nova imagem
2. Commit é feito automaticamente
3. ArgoCD detecta mudança no repositório (sync a cada 30s)
4. ArgoCD aplica o novo deployment no cluster
5. Rollout automático da aplicação

## 🛠️ Configurações Adicionais

### Aplicar configuração do ArgoCD (opcional)
```bash
kubectl apply -f argocd/argocd-config.yaml
# Restart ArgoCD para aplicar configurações
kubectl rollout restart deployment argocd-server -n argocd
kubectl rollout restart deployment argocd-application-controller -n argocd
```

## 🐛 Troubleshooting

### Pipeline falhando?
1. Verifique se os secrets estão configurados corretamente
2. Verifique se o Docker Hub aceita o login
3. Veja os logs detalhados na aba Actions

### ArgoCD não sincronizando?
1. Verifique se o repositório está acessível
2. Force um refresh manual no ArgoCD UI
3. Verifique os logs do ArgoCD application controller

### Aplicação não atualizando?
1. Verifique se a nova imagem foi criada no Docker Hub
2. Verifique se o `deployment.yaml` foi atualizado
3. Force um rollout manual: `kubectl rollout restart deployment hello-world-app -n hello-world`

## 🎯 Próximos Passos

1. Configure os secrets no GitHub
2. Faça um push para testar a pipeline
3. Monitore o processo no GitHub Actions
4. Verifique o deploy no ArgoCD UI
5. Teste a aplicação funcionando