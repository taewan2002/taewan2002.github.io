const destination = new URL(document.getElementById('destination').href);
destination.search = window.location.search;
destination.hash = window.location.hash;
window.location.replace(destination.href);
