window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-NHB0PGPYTW');

const updateYear = () => {
  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();
};
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", updateYear, { once: true });
} else {
  updateYear();
}
