# 🧪 Teste Completo do Fluxo CI/CD

Este documento mostra como testar todo o fluxo de CI/CD do projeto.

## 🎯 Objetivo

Testar o fluxo completo:
```
Código → GitHub → CI/CD → Docker Hub → ArgoCD → Kubernetes
```

## ✅ Pré-requisitos

- [ ] Secrets configurados no GitHub (veja [SETUP-PIPELINE.md](SETUP-PIPELINE.md))
- [ ] Cluster Kubernetes rodando
- [ ] ArgoCD instalado e funcionando
- [ ] Repositório já clonado localmente

## 🚀 Passo a Passo do Teste

### 1. Preparar o Ambiente

```bash
# Clonar o repositório (se não tiver)
git clone https://github.com/robarros/argocd-lab.git
cd argocd-lab

# Verificar branch atual
git branch
```

### 2. Fazer uma Mudança Simples

```bash
# Editar a aplicação para incluir uma nova mensagem
sed -i "s/'Olá Mundo! 🌍'/'Olá Mundo! 🌍 - Versão CI\/CD!'/" app/app.py

# Verificar a mudança
grep "Olá Mundo" app/app.py
```

### 3. Commit e Push

```bash
# Adicionar mudanças
git add app/app.py

# Fazer commit
git commit -m "test: adicionar versão CI/CD na mensagem"

# Push para trigger da pipeline
git push origin main
```

### 4. Monitorar a Pipeline

1. **GitHub Actions:**
   - Acesse: https://github.com/robarros/argocd-lab/actions
   - Veja o workflow "CI/CD Pipeline" executando
   - Aguarde todos os steps completarem (✅)

2. **Docker Hub:**
   - Acesse: https://hub.docker.com/r/robarros/argocd-app
   - Verifique se novas tags foram criadas
   - Exemplo: `abc1234`, `20241023-143000`, `latest`, `stable`

### 5. Verificar ArgoCD

```bash
# Verificar aplicações ArgoCD
kubectl get applications -n argocd

# Ver status da aplicação
kubectl describe application hello-world-app -n argocd

# Forçar sync manual (se necessário)
kubectl patch application hello-world-app -n argocd -p '{"operation":{"initiatedBy":{"username":"admin"},"sync":{"syncStrategy":{"apply":{"force":true}}}}}' --type merge
```

### 6. Verificar Deploy no Kubernetes

```bash
# Ver pods da aplicação
kubectl get pods -n hello-world

# Ver deployment
kubectl get deployment -n hello-world

# Verificar imagem usada
kubectl describe deployment hello-world-app -n hello-world | grep Image

# Ver logs da aplicação
kubectl logs -l app=hello-world-app -n hello-world --tail=20
```

### 7. Testar a Aplicação

```bash
# Port-forward para testar localmente
kubectl port-forward -n hello-world service/hello-world-service 8080:80 &

# Testar endpoint principal
curl http://localhost:8080

# Testar health check
curl http://localhost:8080/health

# Parar port-forward
pkill -f "port-forward"
```

## 📊 Resultados Esperados

### ✅ GitHub Actions
- [ ] Build completed successfully
- [ ] Docker image pushed to registry
- [ ] Kubernetes manifests updated
- [ ] Security scan completed

### ✅ Docker Hub
- [ ] Nova imagem com tag do commit
- [ ] Tag `latest` atualizada
- [ ] Tag `stable` atualizada (se main branch)
- [ ] Multiple architectures (amd64, arm64)

### ✅ ArgoCD
- [ ] Application status: `Synced` e `Healthy`
- [ ] Deployment usando nova imagem
- [ ] Pods rodando com nova versão

### ✅ Aplicação
- [ ] Resposta contém "Versão CI/CD"
- [ ] Health checks funcionando
- [ ] Logs sem erros

## 🐛 Troubleshooting

### Pipeline falhou?

```bash
# Ver logs detalhados no GitHub Actions
# Verificar secrets configurados
# Testar login Docker Hub manualmente:
docker login -u robarros
```

### ArgoCD não sincronizou?

```bash
# Forçar refresh da aplicação
kubectl patch application hello-world-app -n argocd -p '{"spec":{"source":{"targetRevision":"HEAD"}}}' --type merge

# Ver eventos do ArgoCD
kubectl get events -n argocd --sort-by=.metadata.creationTimestamp
```

### Aplicação não atualizou?

```bash
# Verificar se deployment foi atualizado
git log --oneline -n 5

# Forçar restart do deployment
kubectl rollout restart deployment hello-world-app -n hello-world

# Verificar rollout status
kubectl rollout status deployment hello-world-app -n hello-world
```

## 🎉 Sucesso!

Se todos os passos funcionaram, você tem:

1. ✅ **Pipeline CI/CD completa** - Commits automaticamente viram deploys
2. ✅ **GitOps funcionando** - ArgoCD mantém estado desejado
3. ✅ **Registry privado** - Imagens no seu Docker Hub
4. ✅ **Monitoramento** - Logs e métricas disponíveis

## 🔄 Próximos Testes

Experimente:

1. **Rollback:** Fazer commit que reverte mudança
2. **Feature branch:** Criar branch, fazer PR, ver preview
3. **Breaking change:** Introduzir erro e ver como pipeline detecta
4. **Load test:** Escalar pods e testar sob carga

---

💡 **Dica:** Mantenha este fluxo de teste salvo para validar mudanças futuras na pipeline!