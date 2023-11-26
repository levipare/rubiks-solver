document.getElementById('solve-cube').addEventListener('click', () => {
	fetch('/solve', { method: 'POST' });
});


document.getElementById('scramble-cube').addEventListener('click', () => {
	fetch('/scramble', { method: 'POST' });
});


document.getElementById('abort').addEventListener('click', () => {
	fetch('/abort', { method: 'POST' });
});
