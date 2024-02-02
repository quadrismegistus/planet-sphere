from .imports import *

geoloc_js = """
async function geoloc() {
    window.geoloc = {'lat':0.0, 'lon':0.0};
    await navigator.geolocation.getCurrentPosition(
        (pos) => { 
            window.geoloc = {
                'lat':pos.coords.latitude,
                'lon':pos.coords.longitude
            }
        }
    );
}

geoloc();
"""

hover_js = """

window.hover_json = "";
setInterval(
    function() {
        const els = window.document.getElementsByClassName('hoverlayer');
        if(els.length) {
            const el = els[0];
            const txt = el.textContent;
            if(txt!=window.hover_json) {
                window.hover_json = txt;
            }
        }
    },
    100
);

window.mouseX = 0;
window.mouseY = 0;

function updateMouseLoc(event) {
    window.mouseX = event.clientX;
    window.mouseY = event.clientY;
}

document.addEventListener('mousemove', updateMouseLoc);
document.body.style.overflow = 'hidden';

var style = document.createElement('style');
style.innerHTML = `
  a:hover { 
    text-decoration: none !important; 
  }
`;
document.head.appendChild(style);

"""
