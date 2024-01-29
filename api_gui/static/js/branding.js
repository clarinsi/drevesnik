var site_lang = "{{ site_lang }}";

async function addBranding() {
	const branding = await fetchBranding();
    document.querySelectorAll('[branding]').forEach(element => {
		brandingContent = ""
		for (var i = 0; i < branding.length; i++) {
			brandingContent += '<a href="' + branding[i]["url"] + '"><img src="' + branding[i]["image"] + '" alt="' + branding[i]["alt"] + '"></a>'
		}
		element.innerHTML = brandingContent;
    });
}

async function fetchBranding() {
    const response = await fetch(`/drevesnik/get_branding`);
    return response.json();
}

window.addEventListener('DOMContentLoaded', async () => {
    addBranding();
});
