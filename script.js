function convert() {
  const input = document.getElementById("url");
  const url = input.value.trim();

  if (!url) {
    alert("Paste a YouTube link first");
    return;
  }

  // simple validation
  if (!url.includes("youtube.com") && !url.includes("youtu.be")) {
    alert("Enter a valid YouTube link");
    return;
  }

  // redirect to your backend (downloads file)
  window.location.href =
    "http://127.0.0.1:3000/convert?url=" + encodeURIComponent(url);
}