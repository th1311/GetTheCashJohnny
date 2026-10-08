# Get the Cash — Phoenix and GitHub Pages edition

This is a ready-to-host static website. The game remains Python/Pygame and its browser build is already included. You do not need Python installed to play it.

## Open in Phoenix Code

1. Extract this ZIP.
2. Open the entire `GetTheCashWebsite` folder as your project in Phoenix Code.
3. Open the top-level `index.html`.
4. Start Live Preview with the lightning-bolt icon.
5. Use the Pop Out to New Window control to open the preview in your browser for gameplay. Some editor preview modes capture or disable clicks.
6. Wait for the Python runtime to finish downloading, then select Play game.

Use a served preview, not a file:// URL created by double-clicking index.html. Internet access is needed to load the Python runtime from pygame-web.github.io. The first load takes longer. The ready-to-host files have been checked, but Phoenix itself has not been tested here.

If the editor preview prevents the runtime from loading, serve this same folder with a local server: open a terminal in the folder, run `python -m http.server 8000`, and open http://localhost:8000 in your browser. This fallback needs Python installed.

## Publish on GitHub Pages

1. Create a GitHub repository, for example `get-the-cash` (a public repository is suitable for GitHub Free).
2. Upload the CONTENTS of GetTheCashWebsite, keeping every folder intact. `index.html` must be at the repository root, not inside another GetTheCashWebsite folder.
3. Commit the files to the `main` branch.
4. Open repository Settings > Pages.
5. Under Build and deployment, choose Deploy from a branch.
6. Choose main and /(root), then Save.
7. Wait for GitHub to publish the site and use the link shown in Pages settings.

The expected project URL is https://YOUR_USERNAME.github.io/get-the-cash/ (replace the username and repository name). Relative asset paths allow it to work inside a project repository. No Python server is needed on GitHub Pages.

## Files to edit

- index.html — page structure, text and buttons.
- style.css — colors, fonts, layout and responsive appearance.
- app.js — surrounding website controls and the communication with the Python game.
- python-game/main.py — editable Python game logic.
- python-game/figures/ — the images used by the game.
- audio/JohannTheme.mp3 — music used by the website.
- play/index.html and play/game.tar.gz — browser-ready game loader and bundled Python/assets. These are generated files; rebuilding is necessary after changing the Python game or its images.

## Rebuild after Python or game-image changes

Install Python 3.12 or newer, then in a terminal run:

    python -m pip install pygbag==0.9.3
    python rebuild.py

On Windows, use `py` instead of `python` if that is your Python command. The rebuild script updates play/ and copies python-game/audio/JohannTheme.mp3 to the website audio/ folder. Refresh Live Preview or commit the changed files to GitHub afterward. Ordinary HTML/CSS edits require no rebuild.

## Controls

Arrow keys or WASD set movement direction; movement continues until you turn. Each axis retains its direction as in the original game. Space pauses/resumes, R restarts, M toggles sound. Touch direction buttons appear on touch devices. Collect cash and avoid obstacles and the edges.

## Documentation

Phoenix Live Preview: https://docs.phcode.dev/docs/Features/Live%20Preview
GitHub Pages publishing: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

