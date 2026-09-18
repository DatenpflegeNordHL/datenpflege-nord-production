(() => {
  "use strict";

  const projectsUrl = "/website-showcase/showcase-projects.json?v=1c1da573e7077dd575ac11e426cda2ddbc798f449f2d641b17a50939b3234d9e";
  const grid = document.querySelector("#showcase-grid");
  const filter = document.querySelector("#showcase-filter");
  const status = document.querySelector("#showcase-status");
  const dialog = document.querySelector("#showcase-dialog");
  let projects = [];

  const text = (selector, value) => {
    dialog.querySelector(selector).textContent = value;
  };

  const list = (selector, values) => {
    dialog.querySelector(selector).replaceChildren(...values.map((value) => {
      const item = document.createElement("li");
      item.textContent = value;
      return item;
    }));
  };

  const renderPoster = (project, target) => {
    target.classList.toggle("showcase-poster--image", project.poster.type === "image");
    target.dataset.variant = project.poster.variant || "";
    target.replaceChildren();

    if (project.poster.type === "image" && project.poster.src) {
      const image = document.createElement("img");
      image.src = project.poster.src;
      image.alt = project.poster.alt || "";
      image.width = project.poster.width || 720;
      image.height = project.poster.height || 420;
      image.loading = "lazy";
      image.decoding = "async";
      target.append(image);
      return;
    }

    target.append(document.createElement("span"), document.createElement("span"), document.createElement("span"));
  };

  const openDialog = (project) => {
    renderPoster(project, dialog.querySelector("[data-dialog-poster]"));
    text("[data-dialog-category]", project.category);
    text("[data-dialog-title]", project.name);
    text("[data-dialog-description]", project.description);
    list("[data-dialog-industries]", project.industries);
    list("[data-dialog-features]", project.features);
    dialog.querySelector("[data-dialog-editorial-note]").hidden = project.approvalScope !== "editorial-inspiration-only";

    const demo = dialog.querySelector("[data-dialog-demo]");
    demo.hidden = !project.demo;
    if (project.demo) demo.href = project.demo;
    else demo.removeAttribute("href");

    dialog.showModal();
  };

  const cardFor = (project) => {
    const article = document.createElement("article");
    article.className = "showcase-card";

    const button = document.createElement("button");
    button.type = "button";
    button.className = "showcase-card__button";
    button.setAttribute("aria-haspopup", "dialog");
    button.setAttribute("aria-label", project.name + ": Details öffnen");
    button.addEventListener("click", () => openDialog(project));

    const poster = document.createElement("div");
    poster.className = "showcase-poster";
    poster.setAttribute("aria-hidden", "true");
    renderPoster(project, poster);

    const body = document.createElement("div");
    body.className = "showcase-card__body";
    const category = document.createElement("p");
    category.className = "showcase-card__category";
    category.textContent = project.category;
    const title = document.createElement("h3");
    title.textContent = project.name;
    const description = document.createElement("p");
    description.textContent = project.description;
    const action = document.createElement("span");
    action.className = "showcase-card__action";
    action.textContent = "Richtung ansehen →";
    body.append(category, title, description, action);
    button.append(poster, body);
    article.append(button);

    if (project.demo) {
      const demo = document.createElement("a");
      demo.className = "showcase-card__demo";
      demo.href = project.demo;
      demo.innerHTML = "<span>Live-Demo öffnen</span><span aria-hidden=\"true\">↗</span>";
      article.append(demo);
    }
    return article;
  };

  const render = () => {
    const visible = projects.filter((project) => filter.value === "all" || project.category === filter.value);
    grid.replaceChildren(...visible.map(cardFor));
    status.textContent = visible.length + " von " + projects.length + " Designrichtungen sichtbar";
  };

  const setup = (data) => {
    projects = [...data.projects, ...(data.curatedLegacyDirections || [])]
      .filter((project) => project.approved && project.status === "approved");
    const categories = [...new Set(projects.map((project) => project.category))]
      .sort((a, b) => a.localeCompare(b, "de"));
    filter.append(...categories.map((category) => {
      const option = document.createElement("option");
      option.value = category;
      option.textContent = category;
      return option;
    }));
    filter.addEventListener("change", render);
    render();
  };

  dialog.querySelector(".showcase-dialog__close").addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) dialog.close();
  });

  fetch(projectsUrl, { credentials: "same-origin" })
    .then((response) => response.ok ? response.json() : Promise.reject(new Error("Katalog nicht verfügbar")))
    .then(setup)
    .catch(() => {
      status.textContent = "Die Designrichtungen konnten gerade nicht geladen werden. Bitte versuchen Sie es später erneut.";
    });
})();
