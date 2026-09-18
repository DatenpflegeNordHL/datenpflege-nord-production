(() => {
  "use strict";
  const projectsUrl = "/website-showcase/showcase-projects.json?v=56fb2e39f74bff3446a60cdc85656b962ada02a8a199c815afdf22d297bd96bd";
  const grid = document.querySelector("#showcase-grid");
  const filter = document.querySelector("#showcase-filter");
  const status = document.querySelector("#showcase-status");
  const dialog = document.querySelector("#showcase-dialog");
  let projects = [];
  const text = (selector, value) => { dialog.querySelector(selector).textContent = value; };
  const list = (selector, values) => dialog.querySelector(selector).replaceChildren(...values.map((value) => { const item = document.createElement("li"); item.textContent = value; return item; }));
  const openDialog = (project) => { dialog.querySelector("[data-dialog-poster]").dataset.variant = project.poster.variant; text("[data-dialog-category]", project.category); text("[data-dialog-title]", project.name); text("[data-dialog-description]", project.description); list("[data-dialog-industries]", project.industries); list("[data-dialog-features]", project.features); const note = dialog.querySelector("[data-dialog-editorial-note]"); note.hidden = project.approvalScope !== "editorial-inspiration-only"; dialog.showModal(); };
  const render = () => {
    const visible = projects.filter((project) => filter.value === "all" || project.category === filter.value);
    grid.replaceChildren(...visible.map((project) => { const article = document.createElement("article"); article.className = "showcase-card"; const button = document.createElement("button"); button.type = "button"; button.className = "showcase-card__button"; button.setAttribute("aria-haspopup", "dialog"); button.setAttribute("aria-label", `${project.name}: Details öffnen`); button.addEventListener("click", () => openDialog(project)); const poster = document.createElement("div"); poster.className = "showcase-poster"; poster.dataset.variant = project.poster.variant; poster.setAttribute("aria-hidden", "true"); poster.append(document.createElement("span"), document.createElement("span"), document.createElement("span")); const body = document.createElement("div"); body.className = "showcase-card__body"; const category = document.createElement("p"); category.className = "showcase-card__category"; category.textContent = project.category; const title = document.createElement("h3"); title.textContent = project.name; const description = document.createElement("p"); description.textContent = project.description; const action = document.createElement("span"); action.className = "showcase-card__action"; action.textContent = "Richtung ansehen →"; body.append(category, title, description, action); button.append(poster, body); article.append(button); return article; }));
    status.textContent = `${visible.length} von ${projects.length} Designrichtungen sichtbar`;
  };
  const setup = (data) => { projects = [...data.projects, ...(data.curatedLegacyDirections || [])].filter((project) => project.approved && project.status === "approved"); const categories = [...new Set(projects.map((project) => project.category))].sort((a, b) => a.localeCompare(b, "de")); filter.append(...categories.map((category) => { const option = document.createElement("option"); option.value = category; option.textContent = category; return option; })); filter.addEventListener("change", render); render(); };
  dialog.querySelector(".showcase-dialog__close").addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", (event) => { if (event.target === dialog) dialog.close(); });
  fetch(projectsUrl, { credentials: "same-origin" }).then((response) => response.ok ? response.json() : Promise.reject(new Error("Katalog nicht verfügbar"))).then(setup).catch(() => { status.textContent = "Die Designrichtungen konnten gerade nicht geladen werden. Bitte versuchen Sie es später erneut."; });
})();
