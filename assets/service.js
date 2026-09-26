(() => {
  const GA_ID = "G-NHB0PGPYTW";
  const CONSENT_KEY = "dpn_consent_v1";
  const CONSENT_MAX_AGE_MS = 180 * 24 * 60 * 60 * 1000;

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function gtag(){window.dataLayer.push(arguments);};

  const denied = {
    ad_storage: "denied",
    analytics_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied"
  };

  const grantedAnalytics = {
    ad_storage: "denied",
    analytics_storage: "granted",
    ad_user_data: "denied",
    ad_personalization: "denied"
  };

  window.gtag("consent", "default", denied);

  let analyticsLoaded = false;

  const loadAnalytics = () => {
    if (analyticsLoaded) return;
    analyticsLoaded = true;

    window.gtag("consent", "update", grantedAnalytics);

    const script = document.createElement("script");
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(GA_ID)}`;
    script.addEventListener("load", () => {
      window.gtag("js", new Date());
      window.gtag("config", GA_ID);
    }, { once: true });
    script.addEventListener("error", () => {
      analyticsLoaded = false;
    }, { once: true });
    document.head.appendChild(script);
  };

  const readConsent = () => {
    try {
      const raw = window.localStorage.getItem(CONSENT_KEY);
      if (!raw) return null;
      const saved = JSON.parse(raw);
      if (
        saved?.version !== 1 ||
        typeof saved.analytics !== "boolean" ||
        typeof saved.savedAt !== "number" ||
        Date.now() - saved.savedAt > CONSENT_MAX_AGE_MS
      ) {
        window.localStorage.removeItem(CONSENT_KEY);
        return null;
      }
      return saved;
    } catch {
      return null;
    }
  };

  const saveConsent = (analytics) => {
    try {
      window.localStorage.setItem(CONSENT_KEY, JSON.stringify({
        version: 1,
        analytics,
        savedAt: Date.now()
      }));
    } catch {
      // If storage is unavailable, the choice applies to the current page only.
    }
  };

  const deleteAnalyticsCookies = () => {
    const names = document.cookie
      .split(/;/)
      .map((part) => part.trim().split("=")[0])
      .filter((name) => name === "_ga" || name.startsWith("_ga_"));

    for (const name of names) {
      document.cookie = `${name}=; Max-Age=0; Path=/; SameSite=Lax`;
      document.cookie = `${name}=; Max-Age=0; Path=/; Domain=.datenpflege-nord.de; SameSite=Lax`;
    }
  };

  const language = document.documentElement.lang.toLowerCase().startsWith("en") ? "en" : "de";
  const copy = language === "en" ? {
    title: "Privacy settings",
    text: "We use Google Analytics only with your consent to understand visits statistically. Without consent, Google Analytics is not loaded and no analytics data is sent to Google.",
    privacy: "Privacy policy",
    necessary: "Necessary only",
    accept: "Allow analytics",
    settings: "Privacy settings"
  } : {
    title: "Datenschutz-Einstellungen",
    text: "Wir verwenden Google Analytics nur mit Ihrer Einwilligung, um Besuche statistisch auszuwerten. Ohne Zustimmung wird Google Analytics nicht geladen und es werden keine Analytics-Daten an Google gesendet.",
    privacy: "Datenschutzerklärung",
    necessary: "Nur notwendige",
    accept: "Analytics erlauben",
    settings: "Datenschutz-Einstellungen"
  };

  let dialog = null;

  const createDialog = () => {
    if (dialog) return dialog;

    dialog = document.createElement("dialog");
    dialog.id = "dpn-consent-dialog";
    dialog.setAttribute("aria-labelledby", "dpn-consent-title");
    dialog.setAttribute("aria-describedby", "dpn-consent-text");

    const title = document.createElement("h2");
    title.id = "dpn-consent-title";
    title.textContent = copy.title;

    const text = document.createElement("p");
    text.id = "dpn-consent-text";
    text.textContent = copy.text;

    const privacy = document.createElement("p");
    const privacyLink = document.createElement("a");
    privacyLink.href = "/datenschutz/#cookies";
    privacyLink.textContent = copy.privacy;
    privacy.appendChild(privacyLink);

    const form = document.createElement("form");
    form.method = "dialog";

    const necessary = document.createElement("button");
    necessary.type = "button";
    necessary.textContent = copy.necessary;
    necessary.addEventListener("click", () => {
      const hadAnalytics = Boolean(readConsent()?.analytics) || analyticsLoaded;
      saveConsent(false);
      window.gtag("consent", "update", denied);
      deleteAnalyticsCookies();
      dialog.close();
      if (hadAnalytics) window.location.reload();
    });

    const accept = document.createElement("button");
    accept.type = "button";
    accept.textContent = copy.accept;
    accept.addEventListener("click", () => {
      saveConsent(true);
      loadAnalytics();
      dialog.close();
    });

    form.append(necessary, accept);
    dialog.append(title, text, privacy, form);

    dialog.addEventListener("cancel", (event) => {
      event.preventDefault();
    });

    document.body.appendChild(dialog);
    return dialog;
  };

  const openSettings = () => {
    const currentDialog = createDialog();
    if (!currentDialog.open) currentDialog.showModal();
  };

  const addSettingsLink = () => {
    if (document.querySelector("[data-dpn-consent-settings]")) return;

    const link = document.createElement("a");
    link.href = "#datenschutz-einstellungen";
    link.dataset.dpnConsentSettings = "true";
    link.textContent = copy.settings;
    link.addEventListener("click", (event) => {
      event.preventDefault();
      openSettings();
    });

    const target = document.querySelector(".footer-links") || document.querySelector("footer");
    if (target) target.appendChild(link);
  };

  const updateYear = () => {
    const year = document.getElementById("year");
    if (year) year.textContent = new Date().getFullYear();
  };

  const init = () => {
    updateYear();
    addSettingsLink();

    const consent = readConsent();
    if (consent?.analytics) {
      loadAnalytics();
      return;
    }
    if (consent?.analytics === false) {
      deleteAnalyticsCookies();
      return;
    }

    // Clean up cookies left by the previous always-on GA deployment before asking again.
    deleteAnalyticsCookies();
    openSettings();
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
