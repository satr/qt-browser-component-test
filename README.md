# qt-browser-component-test

This repo contains two small test apps:

- `main.py` — a PySide6 `QWebView` desktop shell for testing Qt WebView.
- `webapp/` — a React + Vite app configured with the legacy plugin so builds emit `polyfills-legacy-*.js`.

## Qt WebView shell

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
python main.py
```

Pass a URL to open a specific page:

```bash
python main.py https://example.com
```

## React + Vite legacy test app

1. Install Node.js dependencies:

```bash
cd webapp
npm install
```

2. Build the app:

```bash
npm run build
```

3. Serve the dev app:

```bash
npm run dev
```

The production build is written to `webapp/dist/` and includes the legacy bundle files such as `assets/polyfills-legacy-*.js`.
