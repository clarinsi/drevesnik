
const suggestions = [];
function searchHistory() {
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
                }
            }

            if (document.querySelector("#korpusi")) {
                document.querySelectorAll("#korpusi input").forEach(el => {
                    search.korpusi[el.id] = el.checked;
                })
            }

            const isDuplicate = checkForDuplicates(search);
            if (!isDuplicate) {
                clearOldest();
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
                        if (istiKorpusi) {
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

            for (const item of sorted) {
                const hItem = displayHistoryItem(item);
                results.append(hItem);
            }

        } catch (error) {
            console.error('Error while displaying history.\n', error)
        }
    }
    function displayHistoryItem(item, location) {

        if (typeof item === 'object') {
            var transformed = Object.values(item)[0];

        } else if (typeof item === 'number') {
            var transformed = localStorage.getItem('drevesnik-' + item);
            transformed = JSON.parse(transformed);
        } else {
            console.log(typeof item);
        }
        try {
            const wrapper = document.createElement('div');
            wrapper.classList.add('fiftyfifty');
            wrapper.style = 'display: flex;'

            const queryWrapper = document.createElement('div');
            const query = document.createTextNode(transformed.query);
            const link = document.createElement('a');
            link.href = transformed.url;
            link.target = "_blank";
            link.appendChild(query);
            queryWrapper.appendChild(link);

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

            wrapper.append(queryWrapper);
            wrapper.append(korpusi);

            if (location) {
                location.append(wrapper);
                return
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
                return a - b;
            }

        } catch (error) {
            console.error('Error while sorting history items.\n', error)
        }
    }

    function clearOlderThenOneHour() {
        const historyItems = getHistory();
        try {

            const nowSec = Math.floor(Date.now() / 1000); //seconds
            for (const item of historyItems) {
                let itemName = Object.keys(item);
                let itemNum = itemName[0].replace('drevesnik-', '');
                let num = parseInt(itemNum);
                if (Number.isInteger(num)) {

                    const itemSec = Math.floor(num / 1000);
                    if (nowSec - itemSec > 3600) { //if item is older then one hour
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
        clearOlderThenOneHour();
    } catch (error) {
        console.error('Error while clearing history items older then one hour.\n', error);
    }
    return { saveHistory, getHistory, displayHistory, displayHistoryItem, lastHistoryItem };
}