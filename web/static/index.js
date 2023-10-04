document.getElementById('solve-cube').addEventListener('click', () => {
	fetch('/solve', { method: 'POST' });
});
