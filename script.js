function convert() {
  const url = document.getElementById("url").value.trim();

  if (!url) {
    alert("Paste a YouTube link");
    return;
  }

  window.location.href =
    "https://lediomp3-czt7.onrender.com/convert?url=" +
    encodeURIComponent(url);
}
