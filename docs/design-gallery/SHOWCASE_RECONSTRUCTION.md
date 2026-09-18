# Website-Showcase Rekonstruktion

Stand: 2026-09-18 · Draft PR #19 · kein Production-Merge.

## Quelle und Archiv

Legacy-Quelle: `pulkitxm/claude-directory`, gepinnt auf `9b5ad43b1450fe6b28a42a9cb8115498d5c56e2a` (MIT). Privater Git-Mirror: `/srv/nordwerk-gallery/archive/claude-directory.git`. Vollständiges Bundle nach Archivabschluss: `/srv/nordwerk-gallery/archive/claude-directory.bundle`.

Die 546 Poster-/Video-Paare liegen privat unter `/srv/nordwerk-gallery/media/`. Das aktuelle Release-Gate ist `showcase-source-manifest.json`; nur `rightsStatus=approved` darf in `website-showcase/showcase-projects.json` erscheinen.

## Freigabe

Die Draft-Galerie enthält 30 Projekte. 24 Legacy-Projekte stammen aus der bereits dokumentierten Curation mit MIT-Quelle, vorhandenem Projekt-Prompt, ohne Premium-Flag und ohne die dort dokumentierten URL-/Tracker-Risikoflags. Sechs weitere Projekte sind eigene DatenpflegeNord-Demos.

Nicht freigegeben: 199 Legacy-Einträge mit Review-/Risikoflags und 323 weitere `unknown`-Einträge. Sie bleiben außerhalb des öffentlichen Katalogs.

## Medien und Interaktion

Die 24 freigegebenen Legacy-Projekte verwenden echte `poster.jpg` und `demo.mp4`. Videos erhalten ihre `src` erst bei Desktop-Hover, Tastaturfokus oder geöffneter Detailansicht; `preload=none` bleibt Standard und es kann nur eine Videoquelle gleichzeitig aktiv sein. Auf Mobile öffnet Tap die Detailansicht.

`showcase-public-media.sha256` enthält SHA-256-Prüfsummen für alle 48 freigegebenen Legacy-Medien und die 12 Dateien der sechs eigenen Demo-Routen/Poster.

## SEO und Preview

`/website-showcase/` ist als spätere Production-Seite indexierbar und enthält Canonical, OpenGraph, Breadcrumbs sowie Anbieter-/Regionalbezug zu DatenpflegeNord, Lübeck und Schleswig-Holstein. Template-Demos unter `/website-showcase/demo/<slug>/` sind `noindex,follow` und nicht in der Sitemap.

Das Draft-Artefakt überschreibt HTML auf `noindex, nofollow, noarchive` und erzeugt `robots.txt` mit `Disallow: /`.
