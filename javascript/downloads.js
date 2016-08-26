
// var binaries is declared in javascript.html.

function getBinaryById(osId) {
  for (var i = 0; i < binaries.length ; i++) {
    var binary = binaries[i];
    if (binary.id == osId) {
      return binary;
    }
  }
  return null;
}

window.onload = function () {
  prepareLinks();
  downloadAutomatically();
}

function prepareLinks() {
  var osLinks = document.getElementsByClassName("os");
  for (var i = 0; i < osLinks.length ; i++ ) {
    var osLink = osLinks[i];
    var id = osLink.id;
    var binary = getBinaryById(id);
    osLink.href = "javascript:downloadById(" + JSON.stringify(id) + ")";
    binary.osLink = osLink;
  }
}
  
function downloadById(binaryId) {
  var binary = getBinaryById(binaryId);
  download(binary);
}

function download(binary) {
  document.getElementById("frame").src = binary.download;
  binary.osLink.classList.add("marked");
}

function downloadAutomatically() {
  for (var i = 0; i < binaries.length ; i++) {
    var binary = binaries[i];
    for (var j = 0; j < binary.browser.length; j++) {
      var osIdentifier = binary.browser[j];
      // TODO: identify os and start download automatically
    }
  }
}