var site_lang = "{{ site_lang }}";

async function addTranslatedContent(lang) {
	console.log("langData");
	const langData = await fetchLanguageData(lang);
	const langDataSl = await fetchLanguageData("sl");
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
		if (element.tagName.toLowerCase() === 'input') {
			if (langData.hasOwnProperty(key)) {
				element.value = langData[key];
			}
			else {
				element.value = langDataSl[key];
			}
		}
		else {
			if (langData.hasOwnProperty(key)) {
				element.innerHTML = langData[key];
			}
			else {
				element.innerHTML = langDataSl[key];
			}
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
