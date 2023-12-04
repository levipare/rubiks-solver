document.getElementById('solve-cube').addEventListener('click', () => {
let cubeState = document.getElementById('manual-state').value	
fetch('/solve', { method: 'POST', body: JSON.stringify({state: cubeState}) });
});


document.getElementById('scramble-cube').addEventListener('click', () => {
	fetch('/scramble', { method: 'POST' });
});


document.getElementById('capture-state').addEventListener('click', async (e) => {
	let res = await fetch('/state');
        let json = await res.json();
        document.getElementById('manual-state').value = json["state"];
});

document.getElementById('abort').addEventListener('click', () => {
	fetch('/abort', { method: 'POST' });
});
