# Guida al Testing del Sistema Microservizi

## ✅ Setup Completato

Il sistema di gestione microservizi è stato implementato e configurato:
- ✅ Database migrato con 3 nuove tabelle
- ✅ Backend API funzionante (12 endpoints)
- ✅ Frontend con UI completa
- ✅ Link nel menu principale della navbar

## 🌐 Accesso al Sistema

### 1. Verifica che i servizi siano in esecuzione

```bash
docker compose ps
```

Dovresti vedere:
- `intellyhub-db-1` (PostgreSQL)
- `intellyhub-api-1` (Backend Flask)
- `intellyhub-frontend-1` (Frontend Vue.js)

### 2. Accedi al frontend

Apri il browser e vai a: **http://localhost:5173**

## 🔐 Login

1. Se non hai un account, registrati cliccando su "Register"
2. Oppure fai login con un account esistente
3. Dopo il login, dovresti vedere la dashboard

## 🎯 Test della Pagina Microservizi

### Accesso alla pagina

**Metodo 1**: Usa il menu principale
- Nella navbar in alto, clicca sul pulsante **"Microservizi"** (icona cubo)
- Dovrebbe portarti a `/microservices`

**Metodo 2**: Accesso diretto
- Naviga a: http://localhost:5173/microservices

### Cosa dovresti vedere

Una pagina con:
- **Header** con titolo "Gestione Microservizi"
- **Bottoni azione**: Statistiche, Importa YAML, Esporta YAML, Nuovo Microservizio
- **Filtri**: Search, Location, Tipo, Status
- **Tabella vuota** (prima volta) con messaggio "Nessun microservizio trovato"
- **Bottone primario**: "Nuovo Microservizio"

## 🧪 Test Case 1: Creare un Microservizio Redis (Locale)

### Passo 1: Apri il dialog di creazione
1. Clicca su **"Nuovo Microservizio"**
2. Si apre un dialog con un form

### Passo 2: Compila il form

**Campi base**:
- **Nome**: `Redis Cache`
- **Tipo Servizio**: `redis`
- **Descrizione**: `Redis in-memory cache for flows`
- **Location**: `local` (Kubernetes)
- **Costo Stimato**: `$10/month`
- **Tags**: `cache, redis, local`

**Connection Info (JSON)**:
Espandi il pannello "Informazioni Connessione" e inserisci:
```json
{
  "url": "redis://redis-cache.intellyhub.svc.cluster.local:6379",
  "password": "{REDIS_PASSWORD}"
}
```

**Configurazione Kubernetes (JSON)**:
Espandi il pannello "Configurazione Kubernetes" e inserisci:
```json
{
  "image": "redis:7-alpine",
  "replicas": 1,
  "ports": [
    {
      "name": "redis",
      "containerPort": 6379,
      "servicePort": 6379
    }
  ],
  "volumes": [
    {
      "name": "redis-data",
      "mountPath": "/data",
      "size": "5Gi"
    }
  ],
  "env": [
    {
      "name": "REDIS_PASSWORD",
      "value": "test123"
    }
  ],
  "resources": {
    "requests": {
      "memory": "512Mi",
      "cpu": "250m"
    },
    "limits": {
      "memory": "1Gi",
      "cpu": "500m"
    }
  },
  "healthCheck": {
    "type": "tcp",
    "port": 6379,
    "initialDelay": 10,
    "period": 5
  }
}
```

### Passo 3: Salva
1. Clicca su **"Crea"**
2. Il sistema dovrebbe:
   - Creare il record nel database
   - Avviare il deployment in Kubernetes (questo può richiedere 30-60 secondi)
   - Mostrare un messaggio di successo
   - Aggiornare la lista

### Passo 4: Verifica il deployment

**Nel frontend**:
1. Nella tabella, clicca sull'icona **occhio** (View Details)
2. Si apre un dialog con 5 tabs:
   - **Info**: Vedi tutti i dettagli del microservizio
   - **Status**: Mostra repliche, pods, status del deployment
   - **Health**: Timeline dei health checks
   - **Logs**: Logs del container
   - **Dependencies**: Flow che usano questo microservizio

**Nel terminale** (verifica Kubernetes):
```bash
# Vedi il deployment
kubectl get deployments -n intellyhub | grep redis

# Vedi i pods
kubectl get pods -n intellyhub | grep redis

# Vedi i services
kubectl get services -n intellyhub | grep redis

# Vedi i PVC
kubectl get pvc -n intellyhub | grep redis
```

Dovresti vedere:
- 1 Deployment: `microservice-<user_id>-<microservice_id>`
- 1 Pod in stato `Running`
- 1 Service: `microservice-<user_id>-<microservice_id>`
- 1 PVC: `microservice-<user_id>-<microservice_id>-redis-data`

## 🧪 Test Case 2: Creare un Microservizio Neo4j (Remoto)

### Passo 1: Nuovo microservizio
Clicca su **"Nuovo Microservizio"**

### Passo 2: Compila il form

**Campi base**:
- **Nome**: `Neo4j AuraDB`
- **Tipo Servizio**: `neo4j`
- **Descrizione**: `Managed Neo4j on AuraDB`
- **Location**: `remote` (Cloud)
- **Costo Stimato**: `$65/month`
- **Tags**: `database, graph, cloud`

**Connection Info (JSON)**:
```json
{
  "bolt_url": "neo4j+s://xxxxx.databases.neo4j.io",
  "http_url": "https://xxxxx.databases.neo4j.io/browser/",
  "username": "neo4j",
  "password": "{NEO4J_CLOUD_PASSWORD}"
}
```

**NOTA**: Per i microservizi **remoti**, NON serve la configurazione Kubernetes.

### Passo 3: Salva
Clicca su **"Crea"**

Il microservizio remoto viene salvato immediatamente (nessun deployment K8s necessario).

## 🧪 Test Case 3: Operazioni sui Microservizi

### Test 3.1: Restart (solo local)
1. Nella tabella, trova il microservizio Redis
2. Clicca sull'icona **restart** (frecce circolari)
3. Conferma l'operazione
4. Il sistema esegue un `kubectl rollout restart`

### Test 3.2: Scale (solo local)
1. Clicca sull'icona **scale** (bilancia)
2. Usa lo slider per scegliere il numero di repliche (es: 2)
3. Clicca su **"Scala"**
4. Verifica:
   ```bash
   kubectl get pods -n intellyhub | grep redis
   ```
   Dovresti vedere 2 pods in esecuzione

### Test 3.3: Logs (solo local)
1. Clicca su **View Details** (occhio)
2. Vai al tab **"Logs"**
3. Seleziona il numero di righe (es: 100)
4. Clicca su **"Ricarica"**
5. Vedi i logs del container in tempo reale

### Test 3.4: Edit
1. Clicca sull'icona **edit** (matita)
2. Modifica la descrizione o i tags
3. Clicca su **"Salva"**
4. Le modifiche vengono applicate

### Test 3.5: Delete
1. Clicca sull'icona **delete** (cestino)
2. Leggi il warning sulle dipendenze
3. Conferma l'eliminazione
4. Il microservizio viene rimosso dal database
5. Per i microservizi locali, viene anche fatto cleanup in Kubernetes

## 🧪 Test Case 4: Import/Export YAML

### Test 4.1: Export
1. Clicca su **"Esporta YAML"**
2. Il sistema genera un file YAML con tutti i tuoi microservizi
3. Il file viene scaricato automaticamente: `microservices.yaml`
4. Apri il file per verificare il contenuto

### Test 4.2: Import
1. Clicca su **"Importa YAML"**
2. Incolla il contenuto del file di esempio:
   ```
   /home/kuduk/IntellyHub/examples/microservices.yaml
   ```
3. Clicca su **"Importa"**
4. Il sistema:
   - Valida il YAML
   - Crea i microservizi in batch
   - Mostra un report con successi/errori
5. La tabella si aggiorna con i nuovi microservizi

## 🧪 Test Case 5: Statistics
1. Clicca su **"Statistiche"**
2. Si apre un dialog con:
   - Totale microservizi
   - Distribuzione per location (local vs remote)
   - Distribuzione per status (running, stopped, error, ecc.)
   - Distribuzione per tipo (neo4j, redis, postgresql, ecc.)

## 🧪 Test Case 6: Filtri
1. Usa il campo **Search** per cercare per nome o tipo
2. Usa i dropdown per filtrare per:
   - **Location**: local / remote
   - **Tipo**: neo4j, redis, ecc.
   - **Status**: running, stopped, error
3. I filtri si combinano (AND logic)

## 🧪 Test Case 7: Dependency Resolution (Avanzato)

Questo è il test più importante per verificare l'integrazione end-to-end.

### Prerequisiti
1. Crea un microservizio Neo4j locale (vedi Test Case 1, ma con Neo4j)
2. Attendi che sia in stato `running`

### Passo 1: Crea un plugin manifest con dipendenze

**File**: `ai-automation-fsm-py/intellyhub-plugins/plugins/test-neo4j/manifest.json`
```json
{
  "name": "test-neo4j",
  "version": "1.0.0",
  "description": "Test plugin with Neo4j dependency",
  "entry_file": "test_neo4j_state.py",
  "state_type": "test_neo4j",
  "dependencies": {
    "services": [
      {
        "type": "neo4j",
        "required": true,
        "prefer": "local",
        "fallback": ["remote"],
        "connection_vars": {
          "bolt_url": "NEO4J_BOLT_URL",
          "username": "NEO4J_USERNAME",
          "password": "NEO4J_PASSWORD"
        },
        "health_check": {
          "type": "tcp",
          "port": 7687,
          "timeout": 5
        }
      }
    ]
  }
}
```

### Passo 2: Crea un flow che usa il plugin

**Flow YAML**:
```yaml
start_state: test_connection

variables:
  test_query: "RETURN 1 as result"

states:
  test_connection:
    state_type: test_neo4j
    # NO neo4j_url, username, password needed!
    # Will be auto-injected by DependencyResolver
    query: "{test_query}"
    output: result
    transition: end

  end:
    state_type: end
```

### Passo 3: Esegui il flow
1. Nel frontend, vai alla pagina del flow
2. Clicca su **"Execute"**
3. Il sistema dovrebbe:
   - Rilevare che il flow usa `test_neo4j`
   - Leggere il manifest e identificare la dipendenza da Neo4j
   - Trovare il microservizio Neo4j locale
   - Verificare che sia deployato e healthy
   - **Iniettare** le variabili: `NEO4J_BOLT_URL`, `NEO4J_USERNAME`, `NEO4J_PASSWORD`
   - Creare il Kubernetes Job con queste env vars
   - Eseguire il flow

### Passo 4: Verifica l'iniezione
Controlla i logs del job:
```bash
kubectl logs -n intellyhub job/flow-job-<user_id>-<flow_id>
```

Dovresti vedere che le variabili d'ambiente sono state iniettate:
```
NEO4J_BOLT_URL=bolt://neo4j-local.intellyhub.svc.cluster.local:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=test123
```

### Passo 5: Verifica Dependencies Tab
1. Vai su `/microservices`
2. Clicca su **View Details** del microservizio Neo4j
3. Vai al tab **"Dependencies"**
4. Dovresti vedere il flow elencato tra le dipendenze

## 🐛 Troubleshooting

### Errore: "Missing Authorization Header"
- Assicurati di essere loggato
- Il token JWT deve essere valido
- Ricarica la pagina e riprova

**Soluzione: Login manuale**
```bash
# 1. Login tramite API
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"paggio@gmail.com","password":"GattoBlu25!"}'

# 2. Copia l'access_token dalla risposta

# 3. Nel browser console (F12), esegui:
localStorage.setItem('token', 'IL_TUO_TOKEN_QUI')

# 4. Ricarica la pagina (F5)
```

### Errore: "404 Not Found"
- Verifica che l'API sia in esecuzione: `docker compose ps`
- Controlla i logs: `docker compose logs api --tail 50`
- Verifica l'URL: `/api/microservices/` (con trailing slash)

### Microservizio bloccato in "deploying"
- Controlla i pods: `kubectl get pods -n intellyhub`
- Vedi i logs del pod: `kubectl logs -n intellyhub <pod-name>`
- Possibili cause:
  - Immagine Docker non trovata
  - Risorse insufficienti nel cluster
  - PVC non può essere montato

### Health checks falliscono
- Verifica che il servizio sia effettivamente in ascolto sulla porta
- Controlla il tipo di health check (TCP vs HTTP)
- Aumenta `initialDelay` nel config se il container ci mette tempo ad avviarsi

### Frontend non mostra il link "Microservizi"
- Verifica di essere loggato
- Ricarica la pagina (Ctrl+F5)
- Controlla la console del browser per errori JavaScript
- Verifica che Navbar.vue sia stato aggiornato:
  ```bash
  docker compose exec frontend cat /app/src/components/Navbar.vue | grep -i microservi
  ```

## 📊 Metriche di Successo

Un test completo è considerato riuscito se:
- ✅ Puoi accedere alla pagina `/microservices`
- ✅ Puoi creare almeno 2 microservizi (1 locale + 1 remoto)
- ✅ Il deployment locale appare in Kubernetes
- ✅ I filtri e la ricerca funzionano
- ✅ Le operazioni (restart, scale, logs) funzionano
- ✅ Import/Export YAML funzionano
- ✅ Statistics mostra dati corretti
- ✅ (Avanzato) Un flow riceve le variabili iniettate correttamente

## 📝 Logs Utili

```bash
# Backend logs
docker compose logs api -f

# Frontend logs
docker compose logs frontend -f

# Database
docker compose logs db -f

# Kubernetes pods
kubectl logs -n intellyhub -l app=intellyhub -f

# Deployment status
kubectl get deployments -n intellyhub -w

# Eventi Kubernetes
kubectl get events -n intellyhub --sort-by='.lastTimestamp'
```

## 🎓 Next Steps

Dopo aver testato con successo:
1. Crea microservizi per i servizi che usi realmente (Redis, PostgreSQL, Neo4j, ecc.)
2. Configura plugin esistenti per dichiarare le loro dipendenze nei manifest
3. Testa la dependency resolution con flow reali
4. Monitora le performance e i costi
5. Usa le statistiche per ottimizzare l'infrastruttura

## 📚 Documentazione Completa

Per maggiori dettagli, consulta:
- `MICROSERVICES_FEATURE_COMPLETE.md` - Architettura completa
- `CLAUDE.md` - Sezione "Microservices Management"
- `examples/microservices.yaml` - Configurazioni di esempio
- `examples/plugin-manifest-with-dependencies.json` - Esempio manifest
- `examples/flow-with-microservice-dependencies.yaml` - Esempio flow
