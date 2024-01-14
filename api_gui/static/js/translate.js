var site_lang = "{{ site_lang }}";

async function addTranslatedContent(lang) {
	console.log("langData");
	const langData = await fetchLanguageData(lang);
	console.log(langData);
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
		if (element.tagName.toLowerCase() === 'input') {
			element.value = langData[key]
		}
		else {
			element.innerHTML = langData[key];
		}
    });
}

async function fetchLanguageData(lang) {
    const response = await fetch(`/drevesnik/translations/${lang}.json`);
    return response.json();
}

window.addEventListener('DOMContentLoaded', async () => {
	console.log(site_lang);
    addTranslatedContent(site_lang);
});
