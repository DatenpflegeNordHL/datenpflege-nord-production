const year = document.getElementById("year");
if (year) year.textContent = new Date().getFullYear();

const safeRead = (key) => {
  try {
    return JSON.parse(localStorage.getItem(key) || "null");
  } catch {
    return null;
  }
};

const safeWrite = (key, value) => {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch {
    // The tools remain usable when browser storage is unavailable.
  }
};

const scopeForm = document.querySelector("[data-scope-check]");
if (scopeForm) {
  const storageKey = "dpn-individualsoftware-scope-v1";
  const fields = [...scopeForm.querySelectorAll("select[data-scope-field]")];
  const level = scopeForm.querySelector("[data-scope-level]");
  const explanation = scopeForm.querySelector("[data-scope-explanation]");
  const questions = scopeForm.querySelector("[data-scope-questions]");
  const saved = safeRead(storageKey);

  if (saved && typeof saved === "object") {
    fields.forEach((field) => {
      if (Object.hasOwn(saved, field.id)) field.value = saved[field.id];
    });
  }

  const updateScope = () => {
    const score = fields.reduce((sum, field) => sum + Number(field.value), 0);
    const selected = fields.filter((field) => Number(field.value) > 0);
    const state = Object.fromEntries(fields.map((field) => [field.id, field.value]));
    safeWrite(storageKey, state);

    let result = "Niedrige Komplexität";
    let detail = "Der beschriebene Umfang wirkt begrenzbar. Abhängigkeiten und Ausnahmen müssen trotzdem vor einer Aufwandsschätzung geprüft werden.";
    if (score >= 15) {
      result = "Hohe Komplexität";
      detail = "Mehrere Rollen, Systeme oder Betriebsanforderungen greifen ineinander. Eine Discovery mit klarer erster Version ist vor einer Schätzung sinnvoll.";
    } else if (score >= 7) {
      result = "Mittlere Komplexität";
      detail = "Der Umfang enthält mehrere Abhängigkeiten. Schnittstellen, Berechtigungen und Abnahmefälle sollten vor einem Angebot konkretisiert werden.";
    }

    level.textContent = result;
    explanation.textContent = detail;
    questions.replaceChildren();
    const priorities = selected.length ? selected.slice(0, 5) : fields.slice(0, 3);
    priorities.forEach((field) => {
      const item = document.createElement("li");
      item.textContent = field.dataset.question;
      questions.append(item);
    });
  };

  scopeForm.addEventListener("change", updateScope);
  scopeForm.addEventListener("reset", () => {
    try {
      localStorage.removeItem(storageKey);
    } catch {
      // Reset still updates the visible form.
    }
    requestAnimationFrame(updateScope);
  });
  updateScope();
}

const checklist = document.querySelector("[data-relaunch-checklist]");
if (checklist) {
  const storageKey = "dpn-website-relaunch-checklist-v1";
  const boxes = [...checklist.querySelectorAll('input[type="checkbox"]')];
  const progress = checklist.querySelector("progress");
  const status = checklist.querySelector("[data-progress-status]");
  const reset = checklist.querySelector("[data-checklist-reset]");
  const saved = safeRead(storageKey);

  if (Array.isArray(saved)) {
    boxes.forEach((box) => {
      box.checked = saved.includes(box.id);
    });
  }

  const updateChecklist = () => {
    const complete = boxes.filter((box) => box.checked);
    progress.max = boxes.length;
    progress.value = complete.length;
    status.textContent = `${complete.length} von ${boxes.length} Aufgaben erledigt`;
    safeWrite(storageKey, complete.map((box) => box.id));
  };

  checklist.addEventListener("change", updateChecklist);
  reset.addEventListener("click", () => {
    boxes.forEach((box) => {
      box.checked = false;
    });
    try {
      localStorage.removeItem(storageKey);
    } catch {
      // The visible reset remains effective.
    }
    updateChecklist();
    boxes[0]?.focus();
  });
  updateChecklist();
}
