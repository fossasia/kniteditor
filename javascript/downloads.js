
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
    var OSName=IdentifyOS();
    downloadById(OSName);
    }
  }
}
function IdentifyOS(){
    var OSName;
if (window.navigator.userAgent.indexOf("Windows NT 10.0 || Windows NT 6.2 || Windows NT 6.1 || Windows NT 6.0 || Windows NT 5.1 || Windows NT 5.0")                                         != -1) OSName="windows";
if (window.navigator.userAgent.indexOf("Mac")            != -1) OSName="mac";
if (window.navigator.userAgent.indexOf("X11 || Linux")   != -1) OSName="ubuntu";
    return OSName;
}