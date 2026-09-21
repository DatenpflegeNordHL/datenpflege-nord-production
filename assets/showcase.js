(() => {
  "use strict";

  const projectsUrl = "/website-showcase/showcase-projects.json?v=8f75a7813c638eccea8b759f0afae84355c9c0c7cb2f086ad28754e93564df5e";
  const INITIAL_COUNT = 12;
  const LOAD_STEPS = [12, 24, 48];
  const LATE_BATCH_COUNT = 48;
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
  const MOBILE_PREVIEW_RATIO = 0.55;
  let projects = [];
  let filtered = [];
  let visibleCount = INITIAL_COUNT;
  let loadStage = 0;
  let activeCardVideo = null;
  let mobileObserver = null;
  let mobilePreviewFrame = 0;
  let mobilePreviewEngaged = false;
  const mobileCandidates = new Map();
  let lastFocused = null;

  const normalize = (value) => String(value || "").normalize("NFKD").replace(/[\u0300-\u036f]/g, "").toLocaleLowerCase("de");
  const projectHaystack = (project) => normalize([project.name, project.category, project.publicLabel, project.source?.path, project.description, ...(project.style || []), ...(project.industries || [])].join(" "));

  const stopCardVideo = (onlyVideo = null) => {
    if (!activeCardVideo) return;
    if (onlyVideo && activeCardVideo.video !== onlyVideo) return;
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
    video.play().catch(() => stopCardVideo(video));
  };

  const mobilePreviewAllowed = () => !hoverCapable.matches && !reduceMotion.matches && !saveData && "IntersectionObserver" in window;

  const selectMobilePreview = () => {
    mobilePreviewFrame = 0;
    if (!mobilePreviewAllowed() || !mobilePreviewEngaged || dialog.open) {
      if (!hoverCapable.matches) stopCardVideo();
      return;
    }
    const viewportCenter = window.innerHeight / 2;
    let selected = null;
    for (const candidate of mobileCandidates.values()) {
      if (!candidate.visible) continue;
      const rect = candidate.article.getBoundingClientRect();
      const distance = Math.abs((rect.top + rect.bottom) / 2 - viewportCenter);
      if (!selected || distance < selected.distance) selected = { ...candidate, distance };
    }
    if (selected) startCardVideo(selected.project, selected.article, selected.video);
    else stopCardVideo();
  };

  const scheduleMobilePreview = () => {
    if (mobilePreviewFrame) return;
    mobilePreviewFrame = window.requestAnimationFrame(selectMobilePreview);
  };

  const engageMobilePreview = () => {
    if (mobilePreviewEngaged || !mobilePreviewAllowed()) return;
    mobilePreviewEngaged = true;
    scheduleMobilePreview();
  };

  const resetMobileObserver = () => {
    if (mobileObserver) mobileObserver.disconnect();
    mobileObserver = null;
    mobileCandidates.clear();
    if (mobilePreviewFrame) window.cancelAnimationFrame(mobilePreviewFrame);
    mobilePreviewFrame = 0;
    if (!mobilePreviewAllowed()) return;
    mobileObserver = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        const candidate = mobileCandidates.get(entry.target);
        if (!candidate) continue;
        candidate.visible = entry.isIntersecting && entry.intersectionRatio >= MOBILE_PREVIEW_RATIO;
        if (!candidate.visible) stopCardVideo(candidate.video);
      }
      scheduleMobilePreview();
    }, { threshold: [0, MOBILE_PREVIEW_RATIO, 0.7, 0.85, 1] });
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
    dialog.querySelector("[data-dialog-category]").textContent = `${project.publicLabel} · ${project.category}`;
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
    const contact = dialog.querySelector("[data-dialog-contact]");
    const contactUrl = new URL("/", window.location.origin);
    contactUrl.searchParams.set("topic", "website");
    contactUrl.searchParams.set("design", project.id);
    contactUrl.searchParams.set("designName", project.name);
    contactUrl.hash = "kontakt";
    contact.href = `${contactUrl.pathname}${contactUrl.search}${contactUrl.hash}`;
    if (project.video?.src && !reduceMotion.matches && !saveData) {
      dialogVideo.poster = project.poster.src;
      dialogVideo.src = project.video.src;
      dialogVideo.hidden = false;
      dialogImage.hidden = true;
      dialogVideo.load();
    } else {
      dialogVideo.removeAttribute("poster");
    }
    dialog.showModal();
    if (project.video?.src && !reduceMotion.matches && !saveData) dialogVideo.play().catch(() => {});
    if (updateAddress) updateUrl(project);
  };

  const closeDialog = ({ updateAddress = true } = {}) => {
    closeDialogMedia();
    if (dialog.open) dialog.close();
    if (updateAddress) updateUrl();
    if (lastFocused instanceof HTMLElement) lastFocused.focus();
    scheduleMobilePreview();
  };

  const cardFor = (project, index) => {
    const article = document.createElement("article");
    article.className = "showcase-card";
    article.dataset.projectId = project.id;
    const button = document.createElement("button");
    button.className = "showcase-card__button";
    button.type = "button";
    button.setAttribute("aria-haspopup", "dialog");
    const media = document.createElement("span");
    media.className = "showcase-card__media";
    const image = document.createElement("img");
    image.src = project.poster.src;
    image.alt = project.poster.alt || `Website-Vorschau: ${project.name}`;
    image.width = project.poster.width || 960;
    image.height = project.poster.height || 600;
    image.loading = index === 0 ? "eager" : "lazy";
    if (index === 0) image.fetchPriority = "high";
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
      if (!reduceMotion.matches && !saveData) {
        const play = document.createElement("span");
        play.className = "showcase-card__play";
        play.setAttribute("aria-hidden", "true");
        play.textContent = "▶";
        media.append(play);
      }
      article.addEventListener("pointerenter", () => { if (hoverCapable.matches) startCardVideo(project, article, video); });
      article.addEventListener("pointerleave", () => { if (hoverCapable.matches) stopCardVideo(video); });
      button.addEventListener("focus", () => {
        if (hoverCapable.matches || button.matches(":focus-visible")) startCardVideo(project, article, video);
      });
      button.addEventListener("blur", () => { if (hoverCapable.matches) stopCardVideo(video); });
      if (mobileObserver) {
        mobileCandidates.set(article, { project, article, video, visible: false });
        mobileObserver.observe(article);
      }
    }
    const body = document.createElement("span");
    body.className = "showcase-card__body";
    const category = document.createElement("span");
    category.className = "showcase-card__category";
    category.textContent = `${project.publicLabel} · ${project.category}`;
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
    resetMobileObserver();
    const shown = filtered.slice(0, visibleCount);
    grid.replaceChildren(...shown.map((project, index) => cardFor(project, index)));
    more.hidden = shown.length >= filtered.length;
    status.textContent = `${filtered.length} ${filtered.length === 1 ? "Website-Beispiel" : "Website-Beispiele"}`;
    progress.textContent = filtered.length ? `${shown.length} von ${filtered.length} angezeigt` : "Keine passende Vorschau gefunden.";
    scheduleMobilePreview();
  };

  const applyFilters = () => {
    visibleCount = INITIAL_COUNT;
    loadStage = 0;
    const query = normalize(search.value.trim());
    const selectedFilter = filter.value;
    filtered = projects.filter((project) => {
      const sourceMatch = selectedFilter === "all"
        || (selectedFilter === "source:legacy" && project.sourceType === "legacy")
        || (selectedFilter === "source:owned" && project.sourceType === "owned")
        || (selectedFilter.startsWith("category:") && project.category === selectedFilter.slice(9));
      return sourceMatch && (!query || query.split(/\s+/).every((term) => projectHaystack(project).includes(term)));
    });
    render();
  };

  const setup = (data) => {
    projects = (data.projects || [])
      .filter((project) => project.active === true && project.publicationStatus === "active" && project.poster?.type === "image" && project.poster?.src)
      .sort((a, b) => (a.displayOrder ?? Number.MAX_SAFE_INTEGER) - (b.displayOrder ?? Number.MAX_SAFE_INTEGER) || String(a.id).localeCompare(String(b.id), "de"));
    filtered = projects.slice();
    const categories = [...new Set(projects.map((project) => project.category))].sort((a, b) => a.localeCompare(b, "de"));
    const sourceOptions = [
      ["source:legacy", "Video-Previews"],
      ["source:owned", "DatenpflegeNord Demos"],
    ].map(([value, label]) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = label;
      return option;
    });
    filter.append(...sourceOptions, ...categories.map((value) => {
      const option = document.createElement("option");
      option.value = `category:${value}`;
      option.textContent = `Kategorie: ${value}`;
      return option;
    }));
    search.addEventListener("input", applyFilters);
    filter.addEventListener("change", applyFilters);
    more.addEventListener("click", () => {
      if (loadStage < LOAD_STEPS.length - 1) {
        loadStage += 1;
        visibleCount = LOAD_STEPS[loadStage];
      } else {
        visibleCount += LATE_BATCH_COUNT;
      }
      render();
    });
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
  dialog.addEventListener("close", () => { closeDialogMedia(); scheduleMobilePreview(); });
  window.addEventListener("pagehide", () => stopCardVideo());
  window.addEventListener("scroll", scheduleMobilePreview, { passive: true });
  window.addEventListener("touchstart", engageMobilePreview, { passive: true, once: true });
  window.addEventListener("pointerdown", engageMobilePreview, { passive: true, once: true });
  window.addEventListener("wheel", engageMobilePreview, { passive: true, once: true });
  window.addEventListener("resize", scheduleMobilePreview, { passive: true });
  reduceMotion.addEventListener("change", render);
  hoverCapable.addEventListener("change", render);

  fetch(projectsUrl, { credentials: "same-origin" })
    .then((response) => response.ok ? response.json() : Promise.reject(new Error("Katalog nicht verfügbar")))
    .then(setup)
    .catch(() => {
      status.textContent = "Die Website-Beispiele konnten gerade nicht geladen werden.";
      progress.textContent = "Bitte versuchen Sie es später erneut.";
    });
})();
