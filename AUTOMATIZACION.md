# Oncolopedia: código fuente y publicación

- Fuente de la web: esta rama (`claude/project-thread-juulw1` de sosarme-hue/oncolopedia).
- Web publicada: rama `main` del mismo repo = contenido de `dist/` (lo que genera `python3 build.py`).
- Dependencias: `pip install markdown pillow`.
- Blog: `src/es/blog/AAAA-MM-DD-slug.md` y `src/en/blog/AAAA-MM-DD-slug.md`. Front-matter: title, desc y, en la versión ES, `en: <slug-en sin fecha>`.
- Comprobar enlaces: `python3 tools/links.py dist` (debe dar «0 rotos»).
- Publicar: copiar `dist/` a un clon de `main` (manteniendo `.git`), commit, push y desplegar con Hostinger
  `hosting_git_deploy-website-repository` (username u235595016, dominio oncolopedia.com, repo https://github.com/sosarme-hue/oncolopedia.git, rama main, directory vacío).
  Comprobar con `hosting_files_list-website-and-directories`.
