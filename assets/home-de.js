window.DPN = {
      user: "DatenpflegeNordHL",
      email: "kontakt@datenpflege-nord.de",
      feedLimit: innerWidth > 900 ? 7 : 5,
    };

(() => {
      const dictionaries = {
        de: {
          current:"aktuell", feedStatusStatic:"Öffentliche Aktivität · statischer Stand",
          feedStatusUpdated:"Öffentliche Aktivität · aktualisiert",
          scopeExternal:"Open Source", scopeOwn:"Eigenes Projekt",
          prMerged:"PR gemergt", prOpened:"PR geöffnet", prClosed:"PR geschlossen", pullRequest:"Pull Request",
          issueOpened:"Issue eröffnet", issue:"Issue", issueContribution:"Issue-Beitrag", codeUpdate:"Code-Update", release:"Release",
          fallbackPr:"Pull Request", fallbackIssue:"GitHub Issue", fallbackIssueContribution:"Beitrag zu einem Issue",
          fallbackCode:"Änderungen veröffentlicht", fallbackRelease:"Neue Version",
          today:"heute", hoursAgo:"vor {n} Std.", dayAgo:"vor {n} Tag", daysAgo:"vor {n} Tagen",
          mailSubject:"Anfrage DatenpflegeNord", mailName:"Name", mailEmail:"E-Mail", mailTopic:"Thema",
          topicSoftware:"Softwareentwicklung", topicWebsite:"Website", topicAutomation:"Automatisierung", topicOther:"Sonstiges"
        },
        en: {
          current:"recent", feedStatusStatic:"Public activity · static snapshot",
          feedStatusUpdated:"Public activity · updated",
          scopeExternal:"Open source", scopeOwn:"Own project",
          prMerged:"PR merged", prOpened:"PR opened", prClosed:"PR closed", pullRequest:"Pull request",
          issueOpened:"Issue opened", issue:"Issue", issueContribution:"Issue contribution", codeUpdate:"Code update", release:"Release",
          fallbackPr:"Pull request", fallbackIssue:"GitHub issue", fallbackIssueContribution:"Contribution to an issue",
          fallbackCode:"Changes published", fallbackRelease:"New release",
          today:"today", hoursAgo:"{n}h ago", dayAgo:"{n} day ago", daysAgo:"{n} days ago",
          mailSubject:"DatenpflegeNord enquiry", mailName:"Name", mailEmail:"Email", mailTopic:"Topic",
          topicSoftware:"Software development", topicWebsite:"Website", topicAutomation:"Automation", topicOther:"Other"
        }
      };
      const language = document.documentElement.lang.toLowerCase().startsWith("en") ? "en" : "de";
      const t = key => dictionaries[language][key] ?? dictionaries.de[key] ?? key;
      const format = (key, values = {}) => Object.entries(values).reduce(
        (text, [name, value]) => text.replace(`{${name}}`, value), t(key)
      );
      window.DPN_I18N = { language, t, format };
    })();

(() => {
      const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
      const typeText = document.getElementById("typeText");
      const typeCursor = document.getElementById("typeCursor");
      let typeTimer = null;

      const typewrite = (text, delay = 0) => {
        if (!typeText || !typeCursor) return;
        clearTimeout(typeTimer);
        typeCursor.hidden = reduceMotion;
        typeCursor.style.opacity = "1";
        if (reduceMotion) { typeText.textContent = text; return; }
        typeText.textContent = "";
        let index = 0;
        const step = () => {
          typeText.textContent = text.slice(0, index++);
          if (index <= text.length) typeTimer = setTimeout(step, 22);
          else typeTimer = setTimeout(() => { typeCursor.style.opacity = ".45"; }, 400);
        };
        typeTimer = setTimeout(step, delay);
      };
      typewrite(typeText?.textContent.trim() || "", 260);

      const elements = [...document.querySelectorAll(".reveal")];
      if (!reduceMotion && innerWidth > 620 && "IntersectionObserver" in window) {
        const observer = new IntersectionObserver(entries => {
          entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            entry.target.animate([
              { opacity:.82, transform:"translateY(8px)" },
              { opacity:1, transform:"translateY(0)" }
            ], { duration:380, easing:"cubic-bezier(.22,1,.36,1)", fill:"forwards" });
            observer.unobserve(entry.target);
          });
        }, { threshold:.08, rootMargin:"0px 0px -24px 0px" });
        elements.forEach(el => observer.observe(el));
      }
    })();

(() => {
      const cfg = window.DPN;
      const feed = document.getElementById("githubFeed");
      const status = document.getElementById("feedStatus");
      const owner = cfg.user.toLowerCase();
      const escapeHtml = (s = "") => String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"})[c]);
      const apiToWeb = (url = "") => url.replace("https://api.github.com/repos/", "https://github.com/").replace("/pulls/", "/pull/").replace("/commits/", "/commit/");
      const relDate = value => {
        const i18n = window.DPN_I18N;
        const d = new Date(value);
        if (Number.isNaN(d.getTime())) return i18n.t("current");
        const hours = Math.max(0, Math.floor((Date.now() - d.getTime()) / 36e5));
        if (hours < 24) return hours <= 1 ? i18n.t("today") : i18n.format("hoursAgo", { n: hours });
        const days = Math.floor(hours / 24);
        if (days < 8) return i18n.format(days === 1 ? "dayAgo" : "daysAgo", { n: days });
        return new Intl.DateTimeFormat(i18n.language === "de" ? "de-DE" : "en-GB", { day:"2-digit", month:"2-digit", year:"2-digit" }).format(d);
      };
      const normalize = e => {
        const p = e.payload || {};
        const repo = e.repo?.name || "GitHub";
        const external = !repo.toLowerCase().startsWith(`${owner}/`);
        let type, title, url;
        if (e.type === "PullRequestEvent") {
          const pr = p.pull_request || {};
          type = pr.merged ? "prMerged" : p.action === "opened" ? "prOpened" : "pullRequest";
          title = pr.title || `${window.DPN_I18N.t("fallbackPr")} #${p.number || pr.number || ""}`;
          url = pr.html_url || apiToWeb(pr.url) || `https://github.com/${repo}/pull/${p.number}`;
        } else if (e.type === "IssuesEvent") {
          type = p.action === "opened" ? "issueOpened" : "issue";
          title = p.issue?.title || window.DPN_I18N.t("fallbackIssue");
          url = p.issue?.html_url || apiToWeb(p.issue?.url) || `https://github.com/${repo}/issues`;
        } else if (e.type === "IssueCommentEvent") {
          type = "issueContribution";
          title = p.issue?.title || window.DPN_I18N.t("fallbackIssueContribution");
          url = p.comment?.html_url || p.issue?.html_url || `https://github.com/${repo}/issues`;
        } else if (e.type === "PushEvent") {
          const commit = p.commits?.[0];
          type = "codeUpdate";
          title = commit?.message?.split("\n")[0] || window.DPN_I18N.t("fallbackCode");
          url = commit?.url ? apiToWeb(commit.url) : `https://github.com/${repo}`;
        } else if (e.type === "ReleaseEvent") {
          type = "release";
          title = p.release?.name || p.release?.tag_name || window.DPN_I18N.t("fallbackRelease");
          url = p.release?.html_url || `https://github.com/${repo}/releases`;
        } else return null;
        return { id:e.id, type, title, repo, url, date:e.created_at, external };
      };
      const choose = events => {
        const seen = new Set();
        const items = [];
        events.map(normalize).filter(Boolean).forEach(item => {
          const key = item.url || `${item.repo}-${item.title}`;
          if (!seen.has(key)) { seen.add(key); items.push(item); }
        });
        return [...items.filter(i => i.external), ...items.filter(i => !i.external)].slice(0, cfg.feedLimit);
      };
      let currentItems = null;
      const render = items => {
        if (!items.length) return;
        currentItems = items;
        const i18n = window.DPN_I18N;
        feed.innerHTML = items.map((item, index) => `
          <a class="feed-item" href="${escapeHtml(item.url)}" target="_blank" rel="noopener noreferrer">
            <span class="feed-index mono">${String(index + 1).padStart(2,"0")}</span>
            <span class="feed-kind"><span class="feed-badge">${escapeHtml(i18n.t(item.type))}</span><span class="feed-scope">${item.external ? i18n.t("scopeExternal") : i18n.t("scopeOwn")}</span></span>
            <span class="feed-main"><span class="feed-repo">${escapeHtml(item.repo)}</span><h3>${escapeHtml(item.title)}</h3></span>
            <span class="feed-meta"><span>${relDate(item.date)}</span><span class="feed-arrow">↗</span></span>
          </a>`).join("");
      };
      const countUp = (el, target) => {
        if (!Number.isFinite(target)) { el.textContent = "—"; return; }
        const start = performance.now();
        const duration = 600;
        const frame = now => {
          const p = Math.min((now - start) / duration, 1);
          el.textContent = Math.round(target * (1 - Math.pow(1-p, 3)));
          if (p < 1) requestAnimationFrame(frame);
        };
        requestAnimationFrame(frame);
      };
      const setStats = stats => Object.entries(stats).forEach(([key, value]) => {
        const el = document.querySelector(`[data-stat="${key}"]`);
        if (el) countUp(el, value);
      });
      const fetchJson = async url => {
        const response = await fetch(url, { headers: { "Accept":"application/vnd.github+json", "X-GitHub-Api-Version":"2022-11-28" } });
        if (!response.ok) throw new Error(`${response.status} ${url}`);
        return response.json();
      };
      const load = async () => {
        try {
          const [profileResult, prResult, eventsResult] = await Promise.allSettled([
            fetchJson(`https://api.github.com/users/${cfg.user}`),
            fetchJson(`https://api.github.com/search/issues?q=${encodeURIComponent(`author:${cfg.user} type:pr`)}`),
            fetchJson(`https://api.github.com/users/${cfg.user}/events/public?per_page=100&page=1`)
          ]);

          const events = eventsResult.status === "fulfilled" ? eventsResult.value : [];
          const items = choose(events);
          if (items.length) render(items);

          const repos = new Set(events.map(e => e.repo?.name).filter(Boolean));
          const external = new Set([...repos].filter(name => !name.toLowerCase().startsWith(`${owner}/`)));
          const stats = {};
          if (profileResult.status === "fulfilled") stats.repos = profileResult.value.public_repos ?? 0;
          if (prResult.status === "fulfilled") stats.prs = prResult.value.total_count ?? 0;
          if (events.length) {
            stats.projects = repos.size;
            stats.external = external.size;
          }
          setStats(stats);

          const updated = profileResult.status === "fulfilled" || prResult.status === "fulfilled" || events.length;
          status.textContent = window.DPN_I18N.t(updated ? "feedStatusUpdated" : "feedStatusStatic");
        } catch (error) {
          console.warn("GitHub-Feed konnte nicht aktualisiert werden", error);
          status.textContent = window.DPN_I18N.t("feedStatusStatic");
        }
      };

      document.getElementById("contactForm").addEventListener("submit", async event => {
        event.preventDefault();

        const form = event.currentTarget;
        const data = new FormData(form);
        const i18n = window.DPN_I18N;
        const button = form.querySelector('button[type="submit"]');
        const status = document.getElementById("contactStatus");
        const en = i18n.language === "en";

        const idleText = en ? "Send message ↗" : "Nachricht senden ↗";
        const sendingText = en ? "Sending…" : "Wird gesendet…";
        const successText = en
          ? "Message sent. Thank you."
          : "Nachricht gesendet. Vielen Dank.";
        const errorText = en
          ? "Sending failed. Please try again or email kontakt@datenpflege-nord.de."
          : "Versand fehlgeschlagen. Bitte erneut versuchen oder an kontakt@datenpflege-nord.de schreiben.";
        const rateText = en
          ? "Too many requests. Please wait a few minutes."
          : "Zu viele Anfragen. Bitte einige Minuten warten.";

        const payload = {
          name: String(data.get("name") || "").trim(),
          email: String(data.get("email") || "").trim(),
          topic: String(data.get("topic") || "other"),
          message: String(data.get("message") || "").trim(),
          website: String(data.get("website") || "")
        };

        if (payload.message.length < 5) {
          status.textContent = "Bitte mindestens 5 Zeichen als Nachricht eingeben.";
          return;
        }

        button.disabled = true;
        button.textContent = sendingText;
        status.textContent = "";

        try {
          const response = await fetch("/api/contact", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Accept": "application/json"
            },
            body: JSON.stringify(payload)
          });

          const result = await response.json().catch(() => ({}));

          if (!response.ok || !result.ok) {
            status.textContent =
              response.status === 429 ? rateText : errorText;
            return;
          }

          form.reset();
          status.textContent = successText;

        } catch (error) {
          console.warn(
            "Kontaktformular konnte nicht gesendet werden",
            error
          );
          status.textContent = errorText;

        } finally {
          button.disabled = false;
          button.textContent = idleText;
        }
      });
      document.getElementById("year").textContent = new Date().getFullYear();
      load();
    })();
