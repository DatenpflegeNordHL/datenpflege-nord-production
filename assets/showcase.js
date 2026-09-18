(() => {
  "use strict";

  const projectsUrl = "/website-showcase/showcase-projects.json?v=aef78d1385c449ee9f12dac9ddddf1dd1d38665985301f57c0fcc4dde0a5c971";
  const INITIAL_COUNT = 12;
  const BATCH_COUNT = 12;
  const grid = document.querySelector("#showcase-grid");
  const filter = document.querySelector("#showcase-filter");
  const search = document.querySelector("#showcase-search");
  const status = document.querySelector("#showcase-status");
  const progress = document.querySelector("#showcase-progress");
  const more = document.querySelector("#showcase-more");
  const dialog = document.querySelector("#showcase-dialog");
  const dialogVideo = dialog.querySelector("[data-dialog-video]");
  const dialogImage = dialog.querySelector("[data-dialog-image]");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const hoverCapable = window.matchMedia("(hover: hover) and (pointer: fine)");
  const saveData = Boolean(navigator.connection && navigator.connection.saveData);
  let projects = [];
  let filtered = [];
  let visibleCount = INITIAL_COUNT;
  let activeCardVideo = null;
  let lastFocused = null;

  const normalize = (value) => String(value || "").normalize("NFKD").replace(/[\u0300-\u036f]/g, "").toLocaleLowerCase("de");
  const projectHaystack = (project) => normalize([project.name, project.category, project.description, ...(project.style || []), ...(project.industries || [])].join(" "));

  const stopCardVideo = () => {
    if (!activeCardVideo) return;
    const { video, article } = activeCardVideo;
    video.pause();
    video.removeAttribute("src");
    video.load();
    article.classList.remove("is-playing");
    activeCardVideo = null;
  };

  const startCardVideo = (project, article, video) => {
    if (!project.video?.src || reduceMotion.matches || saveData) return;
    if (activeCardVideo?.video === video) return;
    stopCardVideo();
    video.src = project.video.src;
    video.load();
    activeCardVideo = { video, article };
    article.classList.add("is-playing");
    video.play().catch(stopCardVideo);
  };

  const closeDialogMedia = () => {
    dialogVideo.pause();
    dialogVideo.removeAttribute("src");
    dialogVideo.load();
    dialogVideo.hidden = true;
    dialogImage.hidden = false;
  };

  const updateUrl = (project = null) => {
    const url = new URL(window.location.href);
    if (project) url.searchParams.set("design", project.id);
    else url.searchParams.delete("design");
    history.replaceState({}, "", `${url.pathname}${url.search}${url.hash}`);
  };

  const openDialog = (project, { updateAddress = true } = {}) => {
    stopCardVideo();
    lastFocused = document.activeElement;
    dialog.querySelector("[data-dialog-category]").textContent = project.category;
    dialog.querySelector("[data-dialog-title]").textContent = project.name;
    dialog.querySelector("[data-dialog-description]").textContent = project.description;
    const tags = [...(project.style || []), ...(project.industries || [])].slice(0, 6);
    dialog.querySelector("[data-dialog-tags]").replaceChildren(...tags.map((value) => {
      const span = document.createElement("span");
      span.textContent = value;
      return span;
    }));
    dialogImage.src = project.poster.src;
    dialogImage.alt = project.poster.alt || `Website-Vorschau: ${project.name}`;
    dialogImage.hidden = false;
    const demo = dialog.querySelector("[data-dialog-demo]");
    demo.hidden = !project.demo;
    if (project.demo) demo.href = project.demo;
    else demo.removeAttribute("href");
    const contact = dialog.querySelector("[data-dialog-contact]");
    contact.href = "/#kontakt";
    if (project.video?.src) {
      dialogVideo.poster = project.poster.src;
      dialogVideo.src = project.video.src;
      dialogVideo.hidden = false;
      dialogImage.hidden = true;
      dialogVideo.load();
    } else {
      dialogVideo.removeAttribute("poster");
    }
    dialog.showModal();
    if (project.video?.src && !reduceMotion.matches) dialogVideo.play().catch(() => {});
    if (updateAddress) updateUrl(project);
  };

  const closeDialog = ({ updateAddress = true } = {}) => {
    closeDialogMedia();
    if (dialog.open) dialog.close();
    if (updateAddress) updateUrl();
    if (lastFocused instanceof HTMLElement) lastFocused.focus();
  };

  const cardFor = (project) => {
    const article = document.createElement("article");
    article.className = "showcase-card";
    article.dataset.projectId = project.id;
    const button = document.createElement("button");
    button.className = "showcase-card__button";
    button.type = "button";
    button.setAttribute("aria-haspopup", "dialog");
    button.setAttribute("aria-label", `${project.name}: Vorschau und Details öffnen`);
    const media = document.createElement("span");
    media.className = "showcase-card__media";
    const image = document.createElement("img");
    image.src = project.poster.src;
    image.alt = project.poster.alt || `Website-Vorschau: ${project.name}`;
    image.width = project.poster.width || 960;
    image.height = project.poster.height || 600;
    image.loading = "lazy";
    image.decoding = "async";
    media.append(image);
    let video = null;
    if (project.video?.src) {
      video = document.createElement("video");
      video.preload = "none";
      video.muted = true;
      video.loop = true;
      video.playsInline = true;
      video.setAttribute("aria-hidden", "true");
      media.append(video);
      const play = document.createElement("span");
      play.className = "showcase-card__play";
      play.setAttribute("aria-hidden", "true");
      play.textContent = "▶";
      media.append(play);
      article.addEventListener("pointerenter", () => { if (hoverCapable.matches) startCardVideo(project, article, video); });
      article.addEventListener("pointerleave", stopCardVideo);
      button.addEventListener("focus", () => startCardVideo(project, article, video));
      button.addEventListener("blur", stopCardVideo);
    }
    const body = document.createElement("span");
    body.className = "showcase-card__body";
    const category = document.createElement("span");
    category.className = "showcase-card__category";
    category.textContent = project.category;
    const title = document.createElement("span");
    title.className = "showcase-card__title";
    title.textContent = project.name;
    body.append(category, title);
    button.append(media, body);
    button.addEventListener("click", () => openDialog(project));
    article.append(button);
    return article;
  };

  const render = () => {
    stopCardVideo();
    const shown = filtered.slice(0, visibleCount);
    grid.replaceChildren(...shown.map(cardFor));
    more.hidden = shown.length >= filtered.length;
    status.textContent = `${filtered.length} ${filtered.length === 1 ? "Website-Beispiel" : "Website-Beispiele"}`;
    progress.textContent = filtered.length ? `${shown.length} von ${filtered.length} angezeigt` : "Keine passende Vorschau gefunden.";
  };

  const applyFilters = () => {
    visibleCount = INITIAL_COUNT;
    const query = normalize(search.value.trim());
    const category = filter.value;
    filtered = projects.filter((project) => (category === "all" || project.category === category) && (!query || query.split(/\s+/).every((term) => projectHaystack(project).includes(term))));
    render();
  };

  const setup = (data) => {
    projects = (data.projects || []).filter((project) => project.approved === true && project.status === "approved" && project.poster?.type === "image" && project.poster?.src);
    filtered = projects.slice();
    const categories = [...new Set(projects.map((project) => project.category))].sort((a, b) => a.localeCompare(b, "de"));
    filter.append(...categories.map((value) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = value;
      return option;
    }));
    search.addEventListener("input", applyFilters);
    filter.addEventListener("change", applyFilters);
    more.addEventListener("click", () => { visibleCount += BATCH_COUNT; render(); });
    render();
    const requested = new URLSearchParams(window.location.search).get("design");
    if (requested) {
      const project = projects.find((item) => item.id === requested);
      if (project) openDialog(project, { updateAddress: false });
    }
  };

  dialog.querySelector(".showcase-dialog__close").addEventListener("click", () => closeDialog());
  dialog.addEventListener("click", (event) => { if (event.target === dialog) closeDialog(); });
  dialog.addEventListener("cancel", (event) => { event.preventDefault(); closeDialog(); });
  dialog.addEventListener("close", () => { closeDialogMedia(); });
  window.addEventListener("pagehide", stopCardVideo);

  fetch(projectsUrl, { credentials: "same-origin" })
    .then((response) => response.ok ? response.json() : Promise.reject(new Error("Katalog nicht verfügbar")))
    .then(setup)
    .catch(() => {
      status.textContent = "Die Website-Beispiele konnten gerade nicht geladen werden.";
      progress.textContent = "Bitte versuchen Sie es später erneut.";
    });
})();
