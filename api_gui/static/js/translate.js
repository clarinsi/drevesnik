async function addTranslatedContent(lang) {

	let langData;
	try {
		langData = await fetchLanguageData(lang);
	} catch (error) {
		console.error('Error fetching langData for lang:', lang, error);
		langData = null;
	}
	let langDataSl;
	try {
		langDataSl = await fetchLanguageData("sl");
	} catch (error) {
		console.error('Error fetching langData for sl:', error);
		langDataSl = null;
	}

	document.querySelectorAll('[data-i18n]').forEach(element => {
		try {

			const key = element.getAttribute('data-i18n');
			if (element.tagName.toLowerCase() === 'input') {
				if (langData !== null && langData.hasOwnProperty(key)) {
					element.value = langData[key];
				}
				else {
					element.value = langDataSl[key];
				}
			} else if (element.classList.contains('logo')) {
				if (langData !== null && langData.hasOwnProperty(key)) {
					const logo_mod = modifyURL(langData[key]);
					element.innerHTML = logo_mod;
				} else if (langDataSl.hasOwnProperty(key)) {
					const logo_mod = modifyURL(langDataSl[key]);
					element.innerHTML = logo_mod;
				}
			} else {
				if (document.querySelector('body#idx_page')) {

					if (langData !== null && langData.hasOwnProperty(key)) {
						if (langData[key].includes("</a>")) {
							//element.innerHTML = langData[key];
							element.innerHTML = modifyURL(langData[key]);
						} else {
							element.append(document.createTextNode(langData[key]))
						}
					}
					else if (langDataSl.hasOwnProperty(key)) {
						if (langDataSl[key].includes("</a>")) {
							//element.innerHTML = langDataSl[key];
							element.innerHTML = modifyURL(langDataSl[key]);
						} else {
							element.append(document.createTextNode(langDataSl[key]))
						}
					} else {
						console.error(`Unable to find translation for '${key}' on the following element:\n`, element);
					}

				} else {
					// only triggers on /show/ url -> template query.html
					const isContext = checkForContext();

					if (langData !== null && langData.hasOwnProperty(key)) {
						if (isContext.checkString(langData[key])) {
							if (!isContext.checkElement(element)) {
								element.append(document.createTextNode(langData[key]))
							}
						} else {
							if (key.includes('_w_img')) {

								let translation = langData[key];
								let translation_parts = translation.split(" ");
								const index = translation_parts.findIndex(item => item.startsWith("src"));
								const replace = translation_parts[index].replace("src='/", `src='${www_address}`); // www_address is defined in the html template
								translation_parts[index] = replace;
								translation = translation_parts.join(" ");
								element.innerHTML = translation;

							} else {
								element.innerHTML = langData[key];
							}
						}
					}
					else if (langDataSl.hasOwnProperty(key)) {
						if (isContext.checkString(langDataSl[key])) {
							if (!isContext.checkElement(element)) {
								element.append(document.createTextNode(langDataSl[key]))
							}
						} else {
							if (key.includes('_w_img')) {

								let translation = langData[key];
								let translation_parts = translation.split(" ");
								const index = translation_parts.findIndex(item => item.startsWith("src"));
								const replace = translation_parts[index].replace("src='/", `src='${www_address}`); // www_address is defined in the html template
								translation_parts[index] = replace;
								translation = translation_parts.join(" ");
								element.innerHTML = translation;

							} else {
								element.innerHTML = langDataSl[key];
							}
						}
					} else {
						console.error(`Unable to find translation for '${key}' on the following element:\n`, element);
					}

				}
			}
		} catch (e) {
			console.error('Something went wrong while translating the following element:', element);
			console.error(e);
		}
	});
	updateMenuLinks()


	function checkForContext() {
		const context = "context";
		const sobesedilo = "sobesedilo";
		function checkString(string) {
			let isContext = false;
			if (string.toLocaleLowerCase().includes(sobesedilo) || string.toLocaleLowerCase().includes(context)) {
				isContext = true;
			}
			return isContext
		}
		function checkElement(element) {
			const el_string = element.textContent;
			let isContext = false;
			if (el_string.toLocaleLowerCase().includes(sobesedilo) || el_string.toLocaleLowerCase().includes(context)) {
				isContext = true;
			}
			return isContext;
		}
		return {
			checkString,
			checkElement
		}
	}
}

async function fetchLanguageData(lang) {
	const mod_url = modifyURL(`/drevesnik/translations/${lang}.json`);
	const response = await fetch(mod_url);
	return response.json();
	//const response = await fetch(`/drevesnik/translations/${lang}.json`);
	//return response.json();
}

window.addEventListener('DOMContentLoaded', async () => {
	addTranslatedContent(usr_lang);
});


/** --------------------------------------------- **/
/* top menu - language button path adjustments */

function updateMenuLinks() {

	const lang = usr_lang.toLocaleLowerCase() === 'en' ? 'en' : 'sl';
	const body = document.querySelector('body');
	const menu_links = document.querySelectorAll('.menu-links a');
	menu_links.forEach(el => {
		if (!el.classList.contains('done')) {
			if (el.classList.contains('link-language')) {

				switch (body.id) {
					case "help_page":
						el.href = buildCorrectPathname(window.location.pathname, "help");
						el.classList.add('done');
						break;
					case "query_page":
						el.href = buildCorrectPathname(window.location.pathname, "show");
						el.classList.add('done');
						break;
					case "freq_page":
						el.href = buildCorrectPathname(window.location.pathname, "freqs");
						el.classList.add('done');
						break;
					default:
						el.href = modifyURL(el.href);
						el.classList.add('done');
						break;
				}

			} else {
				el.href = modifyURL(el.href);
				el.classList.add('done');
			}
		}
	})

	function buildCorrectPathname(original_path, string) {
		let temp_path = []
		let pathname = "";
		let mod_path = modifyURL(original_path);
		let mod_array = mod_path.split("/");

		if (lang === 'en') {
			temp_path = mod_array.filter((path) => path.toLocaleLowerCase() !== 'en');
			pathname = temp_path.join("/");
		} else {

			if (string === 'show'){
				temp_path = mod_array;
			} else {
				temp_path = mod_array.filter((path) => path.toLocaleLowerCase() !== 'sl');
			}
			const idx = temp_path.indexOf(string);
			temp_path.splice(idx + 1, 0, 'en');
			pathname = temp_path.join("/");
		}

		return pathname;
	}
}