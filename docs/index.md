# Gruppo ELA

# Autori:

- Alessandro Cassani (n. matricola 920015)
- Emilio Daverio (n. matricola 918799)
- Luca Perfetti (n. matricola 919835)

# Repository:

[GitLab Repository Link](https://gitlab.com/academicunimib/DevOps)

# Obiettivo:

L'obiettivo del progetto consiste nel creare e configurare una pipeline CI/CD (Continuous Integration/Continuous Deployment) per automatizzare l'intero processo di sviluppo e distribuzione del software, garantendo che ogni modifica al codice sorgente venga sottoposta a un rigoroso processo di verifica automatica prima del rilascio dell'applicativo in produzione.

# Descrizione target App

Il progetto, sviluppato dal gruppo ELA, rappresenta un'implementazione di un'applicazione App-DB sviluppata per verificare le informazioni inserite dall'utente relative alla facoltà frequentata. L'utente inserisce da terminale il proprio username, la propria password e il dipartimento frequentato, l'applicativo si occupa di stabilire una connessione con il database offerto dal servizio cloud di mongoDb nel quale sono presenti le informazioni da verificare, se l'utente ha inserito le informazioni corrette il sw restituirà un messaggio di conferma, altrimenti un messaggio dove indica che le informazioni inserite non sono registrate.
Il sistema contiene due componenti principali; il modulo mongo_db_connection che fornisce i metodi per la creazione della connessione al database e dei relativi metodi di disconnessione e di ottenimento del riferimento della collezione nella quale sono contenute le informazioni utilizzate, ed il modulo main.py che si occupa dell'ottenimento delle informazioni ricevute dall'utente da terminale ed il relativo utilizzo di queste per interrogare il db grazie ai metodi forniti dal modulo precedente. Questi moduli sono contenuti nella directory 'application', mentre i test di unità e di integrazione sono contenuti nella directory test. Nella root directory del progetto è poi contenuto il file .gitlab-ci.yml contenente l'implementazione della pipeline CI/CD, oltre che il file 'requirements.txt' contenente le dipendenze necessarie per lo stage di build del progetto e il modulo 'setup.py' utile per lo stage 'package' della pipeline.
L'applicativo è stato sviluppato utilizzando Python come linguaggio principale e come ambiente di sviluppo Visual Studio Code (VSCode).

# Descrizione Pipeline

Quando la pipeline viene eseguita, la prima operazione che deve fare è verificare l'ordine di esecuzione dei vari stage definiti al suo interno. Nell'ordine specificato, gli stage sono i seguenti:

- [build](#stage-build)
- [verify](#stage-verify)
- [unit-test](#stage-unit-test)
- [integration-test](#stage-integration-test)
- [package](#stage-package)
- [release](#stage-release)
- [docs](#stage-docs)

Successivamente vengono definite due sezioni utili per gestire le dipendenze Python e l'ambiente virtuale in maniera efficiente. In fase di progettazione è stato definito di lasciare di default la clusola 'allow_failure = false' in modo da fermare l'esecuzione della pipeline quando questa fallisca in qualsiasi suo stage.

All'interno della sezione VARIABLES sono definite le variabili d'ambiente:

1. PIP_CACHE_DIR--> specifica la directory in cui vengono memorizzate le dipendenze Python. il path è il seguente: '$CI_PROJECT_DIR/.cache pip', dove $CI_PROJECT_DIR è la variabile d'ambiente predefinita di gitLab che punta alla root directory del progetto.
2. VENV_DIR--> specifica la directory in cui verrà creato e utilizzato l'ambiente virtuale Python. il path è il seguente: '$CI_PROJECT_DIR/venv'.

La sezione CACHE è utilizzata per ridurre il tempo necessario per compilare e rilasciare il software, in modo da evitare il re-download o la ricompilazione delle stesse risorse in ogni job di compilazione. e al suo interno sono definite le seguenti variabili:

1.  key--> La chiave di cache è impostata su $CI_COMMIT_REF_NAME, che è una variabile d'ambiente che contiene il nome del branch corrente. Questo significa che i risultati delle build verranno memorizzati in cache in modo distinto per ciascun branch.
2.  paths--> Specifica quali directory devono essere memorizzate in cache. In questo caso vengono memorizzate due directory:
    -PIP_CACHE_DIR --> la directory in cui sono memorizzate le dipendenze Python, per evitare di doverle scaricare nuovamente.
    -VENV_DIR --> la directory dell'ambiente virtuale Python.

Dopo aver completato con successo l'installazione delle variabili d'ambiente e la configurazione della cache, il processo procede all'esecuzione dello script definito nella sezione 'before_script'.
Il 'before_script' è una parte della pipeline che viene eseguita prima di un qualsiasi stage specifico al suo interno, all'interno del quale vengono svolte le operazioni necessarie per tutti gli stage della pipeline:

    - python -m venv $VENV_DIR: crea un ambiente virtuale Python nella directory specificata da $VENV_DIR.
    - source $VENV_DIR/bin/activate: attiva l'ambiente virtuale Python creato nella fase precedente.
    - pip install --upgrade pip: aggiorna il gestore di pacchetti Python pip all'interno dell'ambiente virtuale.
    - pip install --upgrade setuptools: aggiorna il modulo setuptools, che è un framework utilizzato per la distribuzione di pacchetti Python.

## stage: build

questo stage si occupa della build del progetto e al suo interno, tramite il job 'compile', viene eseguita l'installazione (con il comando pip install) delle dipendenze software specificate nel file 'requirements.txt', inoltre viene specificata, attraverso al comando --cache-dir $PIP_CACHE_DIR, la directory in cui "pip" deve memorizzare in cache le dipendenze installate.

## stage: verify

All'interno di questo stage vengono eseguiti i tool 'prospector' e 'bandit', strumenti utilizzati per l'analisi statica del codice sorgente per poter individuare potenziali problemi, vulnerabilità o miglioramenti nella qualità del codice. Questi due tool sono eseguiti in due job separati, chiamati rispettivamente 'prospector-analysis' e 'bandit- analysis', in modo da poterli eseguire in parallelo all'interno del medesimo stage, dato che i due tool non sono in dipendenza uno dall'altro.
Il comando 'prospector' nel job 'prospector-analysis' serve per l'esecuzione dell'analisi statica del codice sorgente del progetto.
Mentre nel job 'bandit-analysis' viene eseguito il comando 'bandit -r ./application --exclude tests' il quale serve per individuare potenziali vulnerabilità nel codice. Questa operazione viene eseguita nella directory specificata, ovvero application, perchè l'analisi di vulnerabilità vuole essere eseguita unicamente sui moduli componenti dell'applicativo, non considerando directory relative ai test e documentazione. La clausola 'dependencies [ ]' viene definita per configurare il job in questione a non scaricare precedenti artefatti.

## stage: unit-test

esegue in maniera automatica i vari test unitari i quali vengono eseguiti con il comando pytest. In questo stage ci si concentra sulla verifica delle singole unità di codice. In questo caso si va verificare singolarmente: la connessione a moongDB e le credenziali di accesso dell'utente. il comando pytest viene lanciato all'interno della directory 'tests/unit', dove sono contenuti i moduli relativi ai test di unità. La clausola 'dependencies [ ]' viene definita per configurare il job in questione a non scaricare precedenti artefatti.

## stage: integration-test

Come lo stage precedente, si esegue in modo automatico il test di integrazione con il comando pytest nel path 'tests/integration. Questo stage serve per verificare che l'interazione tra le diverse componenti del software sia eseguito in modo corretto. La clausola 'dependencies [ ]' viene definita per configurare il job in questione a non scaricare precedenti artefatti.

## stage: package

Nel corso della realizzazione di questa fase, è stato fondamentale creare un file noto come "setup.py". Questo file è stato creato manualmente e ha lo scopo di definire le informazioni relative al pacchetto Python in sviluppo, nonché di gestire le operazioni di installazione, distribuzione e gestione del pacchetto. Il "setup.py" include informazioni fondamentali come il nome del pacchetto, la versione, una descrizione dettagliata, l'autore e altre componenti rilevanti. Tali dettagli sono importanti, in quanto verranno utilizzati in fasi successive del progetto. Ad esempio, saranno necessari quando si procederà alla pubblicazione del pacchetto sul Python Package Index (PyPI) o quando si dovrà creare una distribuzione per gli utenti finali. Tale file è un elemento rilevante per garantire una corretta installazione e utilizzo del pacchetto Python, oltre a fornire informazioni essenziali sulla sua identità e scopo.

Andando a fare un'analisi più approfondita della struttura del codice scritto per la realizzazione di tale stage, è presente all'interno di "script" un solo comando che eseguirà due azioni principali:

1. "sdist": permette di creare un pacchetto sorgente (source distribution) del progetto Python. Tale pacchetto contiene il codice originale del progetto, insieme ai file di configurazione, documentazione e altri file necessari.
2. "bdist-wheel": questa operazione permette di creare un pacchetto binario (binary distribution) del progetto Python, solitamente in formato wheel. Questo pacchetto contiene il codice compilato e pronto per l'installazione su altri sistemi.

Nel punto "artifacts" vengono specificati quali risultati della pipeline verranno archiviati come "artefatti" per utilizzi futuri o per distribuire. In questo caso, gli artefatti sono i pacchetti creati nei passaggi precedenti e archiviati nella directory "dist/". Questo definisce che il contenuto della directory "dist/" verrà salvato come artefatto e potrà essere utilizzato successivamente in altre parti della pipeline o essere disponibile per il download se fosse necessario.

## stage: release

Arrivati a questo punto del progetto, è richiesta l'implementazione dello stage "release" in modo da eseguire un upload del pacchetto Python su un repository software che ospita pacchetti e librerie Python pronti per essere utilizzati, nel nostro caso è stato impiegato Python Package Index (PyPI). Da tale sistema verrà generato un token che permette di identificare l'utente che effettua operazioni e fornisce autorizzaioni per l'esecuzione di attività specifiche su PyPI, come per esempio, il caricamento di un pacchetto.
All'interno di "script" si esegue un solo comando "twine upload" che è uno strumento per caricare pacchetti Python su PyPI. A esso bisogna aggiungere due flag:

1. "-u \_ _ token _ \_": specifica che l'autenticazione averrà tramite un token. Il quale è stato creato a priori da PyPI e poi aggiunto alla variabile "$PYPI_TOKEN".
2. "-p $PYPI_TOKEN": specifica il token di autenticazione creato in precedenza. Per rendere più sicuro il token, la password è stata aggiunta nelle impostazioni di GitLab, sezione "CI/CD Variables"
   L'ultimo comando utilizzato è il "allow-failure : false" che stato presentato nella sezione "Descrizione della pipeline" di tale documento.

## stage: docs

Questo stage viene utilizzato per creare e gestire la documentazione di progetto con la conseguente pubblicazione in GitLab Pages. Viene utilizzato il comando "mkdocs build --clean" per poter costruire la documentazione del progetto rimuovendo i precedenti artefatti di build. Successivamente, tramite il comando 'mkdir .public/' viene creata la directory utilizzata per memorizzare i file risultati della build, i quali vengono poi successivamente spostati tramite il comando 'cp -r public/\* .public' nella directory '.public'.
La sezione 'artifacts' specifica quali risultati della build dovrebbero essere archiviati e conservati per l'uso successivo. In questo caso, vengono archiviati i seguenti file:

1. public: I file di build della documentazione.
2. mkdocs.yml: Il file di configurazione di MkDocs.

Infine, la clausola 'only: main' viene utilizzata in modo da eseguire lo stage corrente unicamente per modifiche nel main branch.

## Limiti della soluzione sviluppata

Limitazioni della soluzione sviluppata
Una delle limitazioni che emergono nella soluzione sviluppata riguarda lo stage "release" della pipeline. Questo stage richiede una nuova versione del progetto ogni volta che viene eseguito, e se la versione non viene incrementata, causa un errore. Per affrontare questa limitazione, è necessario apportare una modifica manuale alla versione del progetto seguendo questi passaggi:

1. Aprire il file setup.py.
2. Trova il parametro 'version=x.x.x' all'interno del file, dove 'x.x.x' rappresenta la versione attuale del progetto.
3. Incrementa il terzo valore della versione di uno. Ad esempio, se la versione attuale è 'version=1.0.1', modificala in 'version=1.0.2'.

Questo passaggio è essenziale per garantire che ogni nuova versione del progetto abbia un numero di versione unico e crescente.

## Note della soluzione sviluppata

Durante il processo di sviluppo del presente progetto, è stato adoperato il sistema di controllo delle versioni GitLab al fine di caricare il codice sorgente scritto nell'ambiente di sviluppo e condividerlo sulla piattaforma GitLab. Durante l'analisi dei commit effettuati dai vari contributori del progetto, è emersa la presenza di un quarto utente, identificato come "drago02". È importante notare che, in realtà, l'utente "drago02" corrisponde sempre all'autore Alessandro Cassani.
