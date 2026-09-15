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

const automationMatrix = document.querySelector("[data-automation-decision-matrix]");
if (automationMatrix) {
  const storageKey = "dpn-automation-decision-matrix-v1";
  const fields = [...automationMatrix.querySelectorAll("select[data-auto-field]")];
  const result = automationMatrix.querySelector("[data-auto-result]");
  const explanation = automationMatrix.querySelector("[data-auto-explanation]");
  const questions = automationMatrix.querySelector("[data-auto-questions]");
  const evaluate = automationMatrix.querySelector("[data-auto-evaluate]");
  const saved = safeRead(storageKey);

  if (saved && typeof saved === "object") {
    fields.forEach((field) => {
      if (Object.hasOwn(saved, field.id)) field.value = saved[field.id];
    });
  }

  const value = (id) => automationMatrix.querySelector(`#${id}`)?.value || "";
  const updateAutomationMatrix = () => {
    const state = Object.fromEntries(fields.map((field) => [field.id, field.value]));
    safeWrite(storageKey, state);

    const repeatability = value("auto-repeatability");
    const rules = value("auto-rules");
    const data = value("auto-data");
    const exceptions = value("auto-exceptions");
    const approval = value("auto-approval");
    const consequence = value("auto-consequence");
    const api = value("auto-api");
    const reversibility = value("auto-reversibility");

    let heading = "Deterministische Automatisierung prüfen";
    let detail = "Bei klaren Regeln und strukturierten Daten sollte zuerst ein fester Workflow geprüft werden. KI erhöht hier nicht automatisch die Qualität.";
    let prompts = [
      "Welche Bedingungen können als feste Regeln getestet werden?",
      "Welche API-Aktion muss idempotent oder gegen Duplikate geschützt sein?",
      "Welche Fehler sollen stoppen, wiederholen oder an einen Menschen übergeben werden?",
    ];

    const notReady = repeatability === "low" || (api === "none" && reversibility === "hard");
    const highRisk = consequence === "high" || approval === "required" || reversibility === "hard";
    const aiUseful = data === "unstructured" || (data === "mixed" && rules !== "clear") || rules === "partial";
    const deterministicFit = rules === "clear" && data === "structured" && exceptions === "low";

    if (notReady) {
      heading = "Prozess noch nicht automatisierungsreif";
      detail = "Zuerst sollten Prozessgrenzen, Verantwortlichkeiten oder ein sicherer Systemzugang geklärt werden. Ein Modell löst diese Grundlage nicht.";
      prompts = [
        "Welcher wiederkehrende Kern lässt sich überhaupt stabil beschreiben?",
        "Wer entscheidet fachlich, ob ein Ergebnis korrekt ist?",
        "Wie kann eine Systemaktion sicher getestet oder rückgängig gemacht werden?",
      ];
    } else if (highRisk) {
      heading = "Human-in-the-Loop als Ausgangspunkt";
      detail = "Die Folgen eines Fehlers oder der Freigabebedarf sprechen dafür, automatische Verarbeitung und produktive Aktion klar zu trennen. Kritische Schritte bleiben prüfbar und freigabepflichtig.";
      prompts = [
        "Welche konkrete Aktion braucht vor Ausführung eine Freigabe?",
        "Welche Informationen muss der prüfende Mensch für die Entscheidung sehen?",
        "Was passiert bei Ablehnung, Timeout oder widersprüchlichem Ergebnis?",
      ];
    } else if (deterministicFit && !aiUseful) {
      heading = "Deterministische Automatisierung bevorzugen";
      detail = "Die Eingaben und Regeln wirken ausreichend strukturiert für einen festen Workflow. Das vereinfacht Tests, Fehlersuche und Betrieb.";
    } else if (aiUseful) {
      heading = "KI-gestützte Automatisierung prüfen";
      detail = "Variable oder unstrukturierte Informationen können einen begrenzten KI-Schritt rechtfertigen. Das Modell sollte eine eng definierte Aufgabe übernehmen und seine Ausgabe vor jeder Folgeaktion validiert werden.";
      prompts = [
        "Welche variable Information kann nicht zuverlässig mit festen Regeln verarbeitet werden?",
        "Welches Ausgabeformat lässt sich deterministisch validieren?",
        "Ab wann wird ein unsicherer Fall an einen Menschen übergeben?",
      ];
    }

    result.textContent = heading;
    explanation.textContent = detail;
    questions.replaceChildren();
    prompts.forEach((prompt) => {
      const item = document.createElement("li");
      item.textContent = prompt;
      questions.append(item);
    });
  };

  fields.forEach((field) => field.addEventListener("change", updateAutomationMatrix));
  evaluate.addEventListener("click", updateAutomationMatrix);
  automationMatrix.addEventListener("reset", () => {
    try {
      localStorage.removeItem(storageKey);
    } catch {
      // The visible reset remains effective.
    }
    requestAnimationFrame(() => {
      updateAutomationMatrix();
      fields[0]?.focus();
    });
  });
  updateAutomationMatrix();
}
