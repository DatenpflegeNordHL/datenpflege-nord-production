/* GA4 is loaded only after an explicit analytics decision. */
(() => {
  'use strict';
  if (window.DPNAnalyticsConsent) return;
  window.DPNAnalyticsConsent = true;
  const measurementId = 'G-NHB0PGPYTW';
  const storageKey = 'dpn-analytics-consent';
  const disableKey = 'ga-disable-' + measurementId;
  let started = false;
  let decision = null;
  let returnFocus = null;
  window[disableKey] = true;
  const readDecision = () => {
    try {
      const value = localStorage.getItem(storageKey);
      return value === 'accepted' || value === 'denied' ? value : null;
    } catch { return null; }
  };
  const startAnalytics = () => {
    if (started || decision !== 'accepted') return;
    started = true;
    window[disableKey] = false;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'default', {
      analytics_storage: 'granted', ad_storage: 'denied',
      ad_user_data: 'denied', ad_personalization: 'denied'
    });
    window.gtag('js', new Date());
    window.gtag('config', measurementId, {
      allow_google_signals: false, allow_ad_personalization_signals: false,
      cookie_path: '/'
    });
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=G-NHB0PGPYTW';
    document.head.append(script);
  };
  const clearAnalyticsCookies = () => {
    const domains = location.hostname.split('.');
    const candidates = [''];
    while (domains.length > 1) {
      candidates.push('; domain=' + domains.join('.'));
      domains.shift();
    }
    for (const cookie of document.cookie.split(/;/)) {
      const name = cookie.split('=')[0].trim();
      if (name !== '_ga' && !name.startsWith('_ga_')) continue;
      for (const domain of candidates) {
        document.cookie = name + '=; Max-Age=0; path=/' + domain;
      }
    }
  };
  const applyDecision = value => {
    decision = value;
    if (value === 'accepted') startAnalytics();
    else {
      window[disableKey] = true;
      clearAnalyticsCookies();
      // A new document also stops already loaded GA code and in-flight loading.
      if (started) location.reload();
    }
  };
  const setup = () => {
    const en = document.documentElement.lang.startsWith('en');
    const text = en ? {
      title: 'Website analytics',
      description: 'May we use Google Analytics 4 to understand how this website is used? Google is contacted and analytics cookies are set only after you accept. The website also works if you decline. You can change your decision in the privacy settings.',
      accept: 'Accept analytics', reject: 'Decline analytics',
      settings: 'Privacy settings', privacy: 'Privacy policy (German)',
      storage: 'Your browser cannot save this decision. It applies to this page only.'
    } : {
      title: 'Website-Analyse',
      description: 'Dürfen wir Google Analytics 4 verwenden, um die Nutzung dieser Website zu verstehen? Erst nach Ihrer Zustimmung wird Google kontaktiert und werden Analyse-Cookies gesetzt. Die Website funktioniert auch bei Ablehnung. Sie können Ihre Entscheidung in den Datenschutzeinstellungen ändern.',
      accept: 'Analyse akzeptieren', reject: 'Analyse ablehnen',
      settings: 'Datenschutzeinstellungen', privacy: 'Datenschutzerklärung',
      storage: 'Ihr Browser kann diese Entscheidung nicht speichern. Sie gilt nur für diese Seite.'
    };
    const dialog = document.createElement('dialog');
    dialog.id = 'analytics-consent';
    dialog.className = 'analytics-consent';
    dialog.setAttribute('aria-labelledby', 'analytics-consent-title');
    dialog.setAttribute('aria-describedby', 'analytics-consent-description');
    const title = document.createElement('h2');
    title.id = 'analytics-consent-title'; title.textContent = text.title;
    const description = document.createElement('p');
    description.id = 'analytics-consent-description'; description.textContent = text.description;
    const privacy = document.createElement('a');
    privacy.href = '/datenschutz/#cookies'; privacy.textContent = text.privacy;
    if (en) privacy.lang = 'de';
    const actions = document.createElement('div');
    actions.className = 'analytics-consent-actions';
    const settings = document.createElement('button');
    settings.type = 'button'; settings.className = 'analytics-consent-settings';
    settings.textContent = text.settings;
    settings.setAttribute('aria-controls', dialog.id);
    const notice = document.createElement('p');
    notice.className = 'analytics-consent-notice'; notice.setAttribute('role', 'status');
    for (const [value, label] of [['denied', text.reject], ['accepted', text.accept]]) {
      const button = document.createElement('button');
      button.type = 'button'; button.textContent = label;
      button.dataset.analyticsDecision = value;
      button.addEventListener('click', () => {
        try { localStorage.setItem(storageKey, value); }
        catch { notice.textContent = text.storage; }
        dialog.close();
        applyDecision(value);
        if (returnFocus?.isConnected) returnFocus.focus();
        else settings.focus({ preventScroll: true });
      });
      actions.append(button);
    }
    dialog.append(title, description, privacy, actions);
    const footer = document.querySelector('footer .footer-links') || document.querySelector('footer') || document.body;
    footer.classList.add('analytics-consent-links');
    footer.append(settings, notice);
    document.body.append(dialog);
    const open = () => {
      if (dialog.open) return;
      returnFocus = document.activeElement;
      dialog.show(); // Non-modal: navigation and content remain accessible.
    };
    settings.addEventListener('click', open);
    dialog.addEventListener('cancel', event => {
      if (!decision) event.preventDefault();
    });
    window.addEventListener('storage', event => {
      if (event.key !== storageKey && event.key !== null) return;
      const value = readDecision();
      applyDecision(value);
      if (value) dialog.close(); else open();
    });
    applyDecision(readDecision());
    if (!decision) open();
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setup, { once: true });
  else setup();
})();
