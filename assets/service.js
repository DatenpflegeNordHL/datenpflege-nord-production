const updateYear = () => {
  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();
};
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", updateYear, { once: true });
} else {
  updateYear();
}
