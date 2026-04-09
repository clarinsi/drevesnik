
const suggestions = [];
function searchHistory() {
    const nm_of_items = 10;
    function saveHistory(url) {
        try {
            const query = document.querySelector("#query input#qrt").value;

            const search = {
                query: query,
                url: url,
                korpusi: {
                    //ssj: document.querySelector("#SSJ").checked,
                    //sst: document.querySelector("#SST").checked,
                    //cckress: document.querySelector("#ccKres").checked
                },
                parameters: {

                }
            }

            if (document.querySelector("#korpusi")) {
                document.querySelectorAll("#korpusi input").forEach(el => {
                    search.korpusi[el.id] = el.checked;
                })
            }

            if (document.querySelector("#parameters")){
                document.querySelectorAll("#parameters input").forEach(el => {
                    search.parameters[el.id] = el.checked;
                })
            }

            const isDuplicate = checkForDuplicates(search);
            if (!isDuplicate) {
                // clearOldest();
                const epoch = Date.now();
                const epoch_string = epoch.toString();
                localStorage.setItem(`drevesnik-${epoch_string}`, (JSON.stringify(search)));
            }
        } catch (error) {
            console.error('Error while trying to save search query to local storage.\n', error)
        }

        function checkForDuplicates(current) {
            try {
                const search = current;
                const historyItems = getHistory();
                let isDuplicate = false;
                for (const item of historyItems) {
                    let itemName = Object.keys(item);
                    if (item[itemName].query === search.query) {

                        let istiKorpusi = true;
                        for (const korpus in item[itemName].korpusi) {
                            const korpusi = item[itemName].korpusi;
                            if (korpusi[korpus] !== search.korpusi[korpus]) {
                                istiKorpusi = false;
                                break;
                            }
                        }

                        let istiParametri = true;
                        for (const parameter in item[itemName].parameters){
                            const parametri = item[itemName].parameters;
                            if (parametri[parameter] !== search.parameters[parameter]){
                                istiParametri = false;
                                break;
                            }
                        }

                        if (istiKorpusi && istiParametri) {
                            isDuplicate = true;
                            break;
                        }
                    }
                }
                return isDuplicate;

            } catch (error) {
                console.error('Error while checking for duplicates.\n', error);
            }
        }
        function clearOldest() {
            const historyItems = getHistory();
            try {

                const historyAffixes = sortHistoryItems(historyItems);

                for (let i = 0; historyAffixes.length - i > 9; i++) {
                    const num = historyAffixes[i];
                    localStorage.removeItem(`drevesnik-${num}`);
                }
            } catch (error) {
                console.error('Error while removing search history items.\n', error)
            }
        }
    }
    function getHistory() {
        try {
            const historyItems = [];
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                if (key.startsWith('drevesnik-')) {
                    historyItems.push({ [key]: JSON.parse(localStorage.getItem(key)) });
                }
            }
            return historyItems;
        } catch (error) {
            console.error('Error while retrieving search history items.\n', error)
        }
    }
    function displayHistory() {
        try {
            const items = getHistory();

            const results = document.querySelector("#search_history_results");

            const sorted = sortHistoryItems(items);

            let i = 0;
            for (const item of sorted) {
                if (i >= nm_of_items) break;
                const hItem = displayHistoryItem(item);
                results.append(hItem);
                i++;
            }

            const hasHistory = hasMoreHistory(); //returns 0 or a num
            if (!hasHistory) return;

            const more = document.createElement('div');
            more.id = "show_more";
            more.textContent = langTrans?.['show_more'] || 'Show more';
            more.addEventListener('click', displayMoreHistory)
            document.querySelector('#search_history').append(more);

        } catch (error) {
            console.error('Error while displaying history.\n', error)
        }
    }

    function displayHistoryItem(item, location, append = 'append') {
        if (typeof item === 'object') {
            var transformed = Object.values(item)[0];
        } else if (typeof item === 'number') {
            var transformed = localStorage.getItem('drevesnik-' + item);
            transformed = JSON.parse(transformed);
        } else {
            console.log(typeof item);
        }
        try {
            const wrapper = document.createElement('a');
            //const wrapper = document.createElement('div');
            //wrapper.classList.add('fiftyfifty');
            wrapper.classList.add('threethreethree');
            wrapper.style = 'display: flex;';
            
            wrapper.href = transformed.url;
            wrapper.target = "_blank";

            const queryWrapper = document.createElement('div');
            const query = document.createTextNode(transformed.query);
            //const link = document.createElement('a');
            //link.href = transformed.url;
            //link.target = "_blank";
            //link.appendChild(query);
            //queryWrapper.appendChild(link);
            queryWrapper.appendChild(query);

            const korpusi = document.createElement('div');
            let i = 0;
            for (const korpus in transformed.korpusi) {
                if (transformed.korpusi[korpus]) {
                    if (i !== 0) {
                        const comma = document.createTextNode(', ');
                        korpusi.append(comma);
                    }
                    const k = document.createTextNode(korpus);
                    korpusi.append(k);
                    i++;
                }
            }
            if (!korpusi.textContent.length) korpusi.textContent = '/';

            const parametri = document.createElement('div');
            i = 0;

            for (const param in transformed.parameters){
                if (transformed.parameters[param]) {
                    if (i !== 0) {
                        const comma = document.createTextNode(', ');
                        parametri.append(comma);
                    }                    
                    if (langTrans && langTrans[param]){
                        const p = document.createTextNode(langTrans[param]);
                        parametri.append(p);
                    } else {
                        const p = document.createTextNode(param);
                        parametri.append(p);
                    }
                    i++
                }
            }

            if (!parametri.textContent.length){
                parametri.textContent = '/';
            }

            wrapper.append(queryWrapper);
            wrapper.append(korpusi);
            wrapper.append(parametri);

            if (location) {
                if (append === 'prepend') {
                    location.prepend(wrapper);
                    return;

                }
                location.append(wrapper);
                return;
            }
            return wrapper;

        } catch (error) {
            console.error('Error while display history items.\n', error);
        }

    }

    function lastHistoryItem() {
        try {
            const items = getHistory();
            const sortedItems = sortHistoryItems(items);

            // ordering has changed, now newest are 1st
            return sortedItems[0];
            return sortedItems[sortedItems.length - 1];

        } catch (error) {
            console.error('Error while checking the last history item.\n', error)
        }
    }

    function sortHistoryItems(items) {
        try {
            const historyAffixes = [];
            for (const item of items) {
                let itemName = Object.keys(item);
                let itemNum = itemName[0].replace('drevesnik-', '');
                let num = parseInt(itemNum);
                if (Number.isInteger(num)) {
                    historyAffixes.push(num);
                }
            }
            historyAffixes.sort(compareNumbers);
            return historyAffixes;

            function compareNumbers(a, b) {
                /*
                // older first
                return a - b;
                */
                // newer first
                return b - a;
            }

        } catch (error) {
            console.error('Error while sorting history items.\n', error)
        }
    }

    function clearOlderThen(timeToLive = 2419200) { // 2419200 -> 1 month
        const historyItems = getHistory();
        try {

            const nowSec = Math.floor(Date.now() / 1000); //seconds
            for (const item of historyItems) {
                let itemName = Object.keys(item);
                let itemNum = itemName[0].replace('drevesnik-', '');
                let num = parseInt(itemNum);
                if (Number.isInteger(num)) {

                    const itemSec = Math.floor(num / 1000);
                    if (nowSec - itemSec > timeToLive) { //if item is older then timeToLive
                        localStorage.removeItem(`drevesnik-${num}`);
                    }
                }
            }

        } catch (e) {
            console.error('Error while removing history items older then one hour.');
            console.error(e);
        }
    }
    try {
        clearOlderThen(ttl);
    } catch (error) {
        console.error('Error while clearing history items older then one hour.\n', error);
    }

    function hasMoreHistory(){
        try {
            const current = document.querySelectorAll('#search_history_results > a');
            const current_length = current.length;

            const all = getHistory();
            const all_length = all.length;


            if (all_length - current_length > 0) return current_length;
            return 0;

        } catch (err){
            console.error('Could not determine if any more history items exist...\n', err)
            return 0;
        }

    }
    function displayMoreHistory(e){
        try {
            const start_idx = hasMoreHistory();

            if (!start_idx){
                const self = e.target;
                self.style.display = 'none';
                return;
            }

            const all = getHistory();
            const all_sorted = sortHistoryItems(all);
            const remaining = all_sorted.slice(start_idx, start_idx + nm_of_items);

            const results_area = document.querySelector("#search_history_results");
            for (const r of remaining){
                displayHistoryItem(r, results_area);
            }

            const hasMore = all_sorted.slice(start_idx + nm_of_items);

            if (!hasMore.length){
                const self = e.target;
                self.style.display = 'none';
            }
        } catch (err) {
            console.error('error while trying to show more history items...\n',err);
        }
    }

    return { saveHistory, getHistory, displayHistory, displayHistoryItem, lastHistoryItem };
}