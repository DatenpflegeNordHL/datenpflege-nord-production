(() => {
      const dictionaries = {
        de: {
          mailSubject:"Anfrage DatenpflegeNord", mailName:"Name", mailEmail:"E-Mail", mailTopic:"Thema",
          topicSoftware:"Softwareentwicklung", topicWebsite:"Website", topicAutomation:"Automatisierung", topicOther:"Sonstiges"
        },
        en: {
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
      const video = document.getElementById("heroVideo");
      const source = video?.querySelector("source[data-src]");
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

      const allowVideo = Boolean(video && source && !reduceMotion && matchMedia("(pointer:fine)").matches);
      if (allowVideo) {
        source.src = source.dataset.src;
        video.load();

        let prevX = null;
        let targetTime = 0;
        let seeking = false;
        const seek = () => {
          if (!video.duration || seeking) return;
          seeking = true;
          video.currentTime = Math.max(0, Math.min(video.duration, targetTime));
        };
        video.addEventListener("loadedmetadata", () => {
          targetTime = Math.min(video.duration * .35, video.duration);
          video.currentTime = targetTime;
        }, { once:true });
        video.addEventListener("seeked", () => {
          seeking = false;
          if (Math.abs(video.currentTime - targetTime) > .025) seek();
        });
        addEventListener("mousemove", event => {
          if (!video.duration) return;
          if (prevX === null) { prevX = event.clientX; return; }
          const delta = event.clientX - prevX;
          prevX = event.clientX;
          targetTime = Math.max(0, Math.min(video.duration, targetTime + (delta / innerWidth) * .68 * video.duration));
          seek();
        }, { passive:true });
      }

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
      const applyShowcaseContactContext = () => {
        const url = new URL(window.location.href);
        const topic = url.searchParams.get("topic");
        const design = url.searchParams.get("design")?.trim();
        const designName = url.searchParams.get("designName")?.trim();
        if (topic !== "website" || !design || design.length > 256) return;

        const topicField = document.getElementById("topic");
        const messageField = document.getElementById("message");
        if (!(topicField instanceof HTMLSelectElement) || !(messageField instanceof HTMLTextAreaElement)) return;

        topicField.value = "website";
        if (designName && designName.length <= 200) {
          messageField.value = window.DPN_I18N.language === "en"
            ? `I'm interested in the “${designName}” design direction as inspiration for a custom website.`
            : `Ich interessiere mich für die Designrichtung „${designName}“ als Orientierung für eine eigene Website.`;
        }

        url.searchParams.delete("topic");
        url.searchParams.delete("design");
        url.searchParams.delete("designName");
        history.replaceState({}, "", `${url.pathname}${url.search}${url.hash}`);
      };

      applyShowcaseContactContext();

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
          status.textContent = "Please enter at least 5 characters.";
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
    })();
