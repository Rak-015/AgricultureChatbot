const $ = (selector) => document.querySelector(selector);

function toast(message) {
    const el = document.createElement('div');
    el.className = 'toast';
    el.textContent = message;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 3200);
}

async function postForm(url, form) {
    const response = await fetch(url, { method: 'POST', body: new FormData(form) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Request failed');
    return data;
}

$('#initDbBtn').addEventListener('click', async () => {
    try {
        const response = await fetch('/api/init-db', { method: 'POST' });
        const data = await response.json();
        toast(data.message);
    } catch (error) {
        toast('Could not initialize database. Check MySQL settings.');
    }
});

$('#leafImage').addEventListener('change', (event) => {
    $('#fileName').textContent = event.target.files[0]?.name || 'Choose corn, potato, or tomato leaf image';
});

$('#diseaseForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const result = $('#diseaseResult');
    result.innerHTML = '<p class="muted">Analyzing leaf image...</p>';
    try {
        const data = await postForm('/api/disease', event.target);
        result.innerHTML = '<div class="result-card"><img src="' + data.image_url + '" alt="Uploaded leaf image"><div><span class="confidence">' + data.confidence + '% confidence</span><h3>' + data.disease_name + '</h3><p>' + data.description + '</p><p><strong>Treatment:</strong> ' + data.treatment + '</p><p><strong>Prevention:</strong> ' + data.prevention + '</p></div></div>';
    } catch (error) {
        result.innerHTML = '<p class="muted">' + error.message + '</p>';
    }
});

$('#soilForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const target = $('#soilResult');
    target.style.display = 'block';
    target.textContent = 'Checking soil fertility...';
    try {
        const data = await postForm('/api/soil', event.target);
        target.innerHTML = '<strong>' + data.status + '</strong><br>Recommended fertilizer: ' + data.fertilizer + '<br>' + data.suggestions.map((s) => '- ' + s).join('<br>');
    } catch (error) {
        target.textContent = error.message;
    }
});

$('#cropForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const target = $('#cropResult');
    target.style.display = 'block';
    target.textContent = 'Finding best crop...';
    try {
        const data = await postForm('/api/crop', event.target);
        target.innerHTML = '<strong>' + data.crop + '</strong><br>' + data.reason + '<br><strong>Growing tips:</strong> ' + data.tips;
    } catch (error) {
        target.textContent = error.message;
    }
});

function addBubble(text, type) {
    const history = $('#chatHistory');
    const bubble = document.createElement('div');
    bubble.className = type + ' bubble';
    bubble.textContent = text;
    history.appendChild(bubble);
    history.scrollTop = history.scrollHeight;
    return bubble;
}

$('#chatForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const input = $('#chatMessage');
    const message = input.value.trim();
    if (!message) return;
    addBubble(message, 'user');
    input.value = '';
    const typing = addBubble('AGRI-BOT is typing...', 'bot typing');
    try {
        const response = await fetch('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message }) });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Chat failed');
        typing.className = 'bot bubble';
        typing.textContent = data.reply;
    } catch (error) {
        typing.className = 'bot bubble';
        typing.textContent = error.message;
    }
});
