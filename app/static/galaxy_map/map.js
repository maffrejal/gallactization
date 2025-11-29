/********************************************************************
 * GALACTIZATION – INTERACTIVE GALAXY MAP
 * (Zoom + Pan + Hover + Twinkle + Click Navigation)
 ********************************************************************/

const canvas = document.getElementById("unimap");
const ctx = canvas.getContext("2d");

// Scale to device resolution
function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight * 0.9;
}
resize();
window.onresize = resize;

// Camera
let camX = 0;
let camY = 0;
let zoom = 1;
let targetZoom = 1;

// Hover detection
let mouseX = 0;
let mouseY = 0;

// Galaxy data (to be loaded from backend)
let galaxies = [];

/********************************************************************
 * 1. FETCH REAL GALAXY DATA
 ********************************************************************/
fetch("/api/galaxies")
    .then(r => r.json())
    .then(data => {
        galaxies = data.map(g => ({
            id: g.id,
            name: g.name,
            x: g.x,
            y: g.y,
            size: Math.random() * 2 + 1,
            brightness: Math.random(),
            cluster: g.cluster
        }));
    });

/********************************************************************
 * 2. INPUT HANDLING (PAN + ZOOM)
 ********************************************************************/
canvas.addEventListener("wheel", e => {
    e.preventDefault();
    targetZoom *= e.deltaY < 0 ? 1.1 : 0.9;
    targetZoom = Math.max(0.1, Math.min(5, targetZoom));
});

let dragging = false;
let lastX = 0;
let lastY = 0;

canvas.addEventListener("mousedown", e => {
    dragging = true;
    lastX = e.clientX;
    lastY = e.clientY;
});

canvas.addEventListener("mouseup", () => dragging = false);

canvas.addEventListener("mousemove", e => {
    mouseX = e.clientX;
    mouseY = e.clientY;

    if (dragging) {
        camX -= (e.clientX - lastX) / zoom;
        camY -= (e.clientY - lastY) / zoom;
        lastX = e.clientX;
        lastY = e.clientY;
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("galaxy-canvas");
    const ctx = canvas.getContext("2d");

    window.canvas = canvas;  // expose for debugging
    window.ctx = ctx;

    initMap(canvas, ctx);     // your map init function
});

canvas.addEventListener("click", (e) => {

    if (!galaxies || galaxies.length === 0) return;

    const rect = canvas.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;

    for (let g of galaxies) {
        // compute actual screen position (same as render())
        const sx = (g.x - camX) * zoom + canvas.width / 2;
        const sy = (g.y - camY) * zoom + canvas.height / 2;

        const dx = clickX - sx;
        const dy = clickY - sy;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 12) {   // good selection radius
            console.log("Galaxy clicked:", g.id);
            window.location.href = `/viewer/galaxy/${g.id}`;
            return;
        }
    }
});

/********************************************************************
 * 3. RENDER LOOP
 ********************************************************************/
function render() {
    requestAnimationFrame(render);

    // Smooth zoom
    zoom += (targetZoom - zoom) * 0.1;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    galaxies.forEach(g => {
        const sx = (g.x - camX) * zoom + canvas.width / 2;
        const sy = (g.y - camY) * zoom + canvas.height / 2;

        // Twinkle animation
        const twinkle = 0.5 + Math.sin(Date.now() * 0.002 + g.brightness * 20) * 0.3;

        ctx.beginPath();
        ctx.fillStyle = `rgba(180,220,255, ${twinkle})`;
        ctx.arc(sx, sy, g.size * zoom, 0, Math.PI * 2);
        ctx.fill();
    });

    drawHoverTooltip();
}
render();

/********************************************************************
 * 4. HOVER TOOLTIP
 ********************************************************************/
 function onClickGalaxy(event) {
    const rect = canvas.getBoundingClientRect();
    const mouseX = event.clientX - rect.left;
    const mouseY = event.clientY - rect.top;

    for (let g of galaxies) {
        const dx = mouseX - g.screenX;
        const dy = mouseY - g.screenY;
        const dist = Math.sqrt(dx*dx + dy*dy);

        if (dist < 6) {    // click radius threshold
            window.location.href = `/viewer/galaxy/${g.id}`;
            return;
        }
    }
}
function drawHoverTooltip() {
    let nearest = null;
    let nearestDist = 20;

    galaxies.forEach(g => {
        const sx = (g.x - camX) * zoom + canvas.width / 2;
        const sy = (g.y - camY) * zoom + canvas.height / 2;

        const dx = mouseX - sx;
        const dy = mouseY - sy;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < nearestDist) {
            nearest = g;
            nearestDist = dist;
        }
    });

    if (!nearest) return;

    // Tooltip UI
    ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
    ctx.fillRect(mouseX + 10, mouseY + 10, 160, 60);

    ctx.strokeStyle = "#00ffff";
    ctx.strokeRect(mouseX + 10, mouseY + 10, 160, 60);

    ctx.fillStyle = "#ffffff";
    ctx.font = "14px Arial";
    ctx.fillText(nearest.name, mouseX + 18, mouseY + 30);
    ctx.fillText("Cluster: " + nearest.cluster, mouseX + 18, mouseY + 50);

    canvas.style.cursor = "pointer";

    // Click → open galaxy viewer

}
