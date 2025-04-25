//var site_lang = "{{ site_lang }}";
//lang je definiran v html file-u
async function addBranding() {
	const branding = await fetchBranding();
	document.querySelectorAll('[branding]').forEach(element => {
		/*
		brandingContent = ""
		for (var i = 0; i < branding.length; i++) {
			brandingContent += '<div class="brand"><div>'+branding[i][site_lang + "_desc"]+'</div><a href="' + branding[i]["url"] + '"><img src="' + branding[i]["image"] + '" alt="' + branding[i]["alt"] + '"></a></div>'
		}
		element.innerHTML = brandingContent;
		*/

		//console.log(branding)

		try {

			let site_lang = usr_lang;
			if (site_lang !== "en" && site_lang !== "sl") {
				site_lang = "sl";
			}

			for (let i = 0; i < branding.length; i++) {
				const isApache =  typeof branding[i]?.["sl_text"] === "string" && branding[i]["sl_text"].toLocaleLowerCase().includes('apache');
				const brand_wrapper = document.createElement('div');
				brand_wrapper.classList.add('brand');
				if ( typeof branding[i]?.["url"] === "string" && branding[i]["url"].toLocaleLowerCase().includes("clarin")) {
					brand_wrapper.classList.add('clarin');
				}
				const txt = document.createTextNode(branding[i][site_lang + "_desc"])
				const brand_text = document.createElement('div');

				if (isApache) {
					brand_text.classList.add('info-title');
				}

				brand_text.append(txt)
				brand_wrapper.append(brand_text);

				if (isApache) {
					brand_wrapper.classList.add("info");
					brand_wrapper.classList.remove("brand");
					const more_info = document.createElement('div');
					more_info.innerHTML = branding[i][site_lang + '_text'];
					more_info.style = "font-size: 12px; color: white;";

					brand_wrapper.append(more_info);
				}


				if (branding[i]["url"] && branding[i]["image"] && branding[i]["alt"]){

					const brand_link = document.createElement('a');
					brand_link.href = branding[i]["url"];
					const brand_img = document.createElement('img');
					brand_img.src = modifyURL(branding[i]["image"]);
					//brand_img.src = branding[i]["image"];
					brand_img.alt = branding[i]["alt"];
	
					brand_link.append(brand_img);

					if(isApache){
						brand_wrapper.classList.add('apache');
					}
					brand_wrapper.append(brand_link);

				}


				element.prepend(brand_wrapper);
			}

		} catch (e) {
			console.error('An error occured: \n', e)
		}

	});
}

async function fetchBranding() {
	const mod_url = modifyURL('/drevesnik/get_branding');
	const response = await fetch(mod_url);
	return response.json();

	//const response = await fetch(`/drevesnik/get_branding`);
	//return response.json();
}

window.addEventListener('DOMContentLoaded', async () => {
	addBranding();
});
