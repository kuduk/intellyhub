# Guida alle Icone SVG per Plugin IntellyHub

## Come Funziona il Sistema di Icone

Il sistema di icone personalizzate per i plugin IntellyHub funziona tramite una semplice convenzione di naming:

1. **Convenzione di Naming**: Ogni plugin può avere un file chiamato `icon.svg` nella sua cartella
2. **Fallback Automatico**: Se l'icona non esiste, il sistema usa automaticamente le icone Material Design esistenti
3. **Formato**: Solo file SVG sono supportati
4. **Dimensioni**: L'icona viene ridimensionata automaticamente a 24x24 pixel

## Struttura Directory Plugin

```
intellyhub-plugins/
└── plugins/
    ├── telegram-bot/
    │   ├── manifest.json
    │   ├── telegram-bot_state.py
    │   ├── README.md
    │   └── icon.svg          # ← Icona personalizzata
    ├── rss-reader/
    │   ├── manifest.json
    │   ├── rss_reader_state.py
    │   ├── README.md
    │   └── icon.svg          # ← Icona personalizzata
    └── altro-plugin/
        ├── manifest.json
        ├── altro_plugin_state.py
        └── README.md         # ← Nessuna icona = usa fallback
```

## Come Aggiungere un'Icona al Tuo Plugin

1. **Crea il file SVG**: Crea un file chiamato `icon.svg` nella cartella del tuo plugin
2. **Formato SVG**: Assicurati che sia un file SVG valido con tag `<svg>` di apertura
3. **Dimensioni**: L'icona sarà ridimensionata a 24x24px, progetta di conseguenza
4. **Colori**: Puoi usare colori nel tuo SVG, il sistema gestisce automaticamente i temi scuri/chiari

## Esempio di Icona SVG

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0088cc">
  <path d="m20.665 3.717-17.73 6.837c-1.21.486-1.203 1.161-.222 1.462l4.552 1.42 10.532-6.645c.498-.303.953-.14.579.192l-8.533 7.701h-.002l.002.001-.314 4.692c.46 0 .663-.211.921-.46l2.211-2.15 4.599 3.397c.848.467 1.457.227 1.668-.789l3.019-14.228c.309-1.239-.473-1.8-1.282-1.43z"/>
</svg>
```

## API Endpoint

L'icona sarà servita automaticamente dall'endpoint:
```
GET /api/plugins/{plugin_name}/icon
```

## Caratteristiche Tecniche

- **Caching**: Le icone sono cachate per 1 ora per migliorare le performance
- **Validazione**: Il sistema verifica che il file sia un SVG valido
- **Filtri CSS**: Per i plugin installati, l'icona viene automaticamente resa bianca sui tema scuri
- **Gestione Errori**: Se l'icona non può essere caricata, si usa automaticamente il fallback

## Esempi di Icone Disponibili

Ho creato icone di esempio per i seguenti plugin:
- `telegram-bot`: Icona Telegram ufficiale
- `rss-reader`: Icona RSS feed
- `llm-agent`: Icona AI/stella
- `text-to-speech`: Icona speaker/audio
- `wechat`: Icona WeChat

Queste icone sono nella cartella `example-plugin-icons/` per riferimento.

## Note per gli Sviluppatori

- **Nessuna Modifica al Manifest**: Non è necessario modificare il `manifest.json`
- **Compatibilità**: Plugin esistenti continueranno a funzionare senza modifiche
- **Performance**: Le icone SVG sono leggere e scalabili
- **Accessibilità**: Include automaticamente attributi alt per l'accessibilità