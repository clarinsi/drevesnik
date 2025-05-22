
function showError(msg) {
    const error_wrapper = document.createElement('div');
    error_wrapper.className = 'index-error';
    const maker = errorElementMaker();

    const content = maker.errorWrapper();
    const text = maker.textWrapper();
    const timer = maker.timer();

    text.innerHTML = msg;

    content.append(text);
    content.append(timer);
    error_wrapper.append(content);

    const error_field = document.querySelector("#error");
    error_field.style.display = "block";
    error_field.append(error_wrapper);

    error_wrapper.style.height = error_wrapper.offsetHeight + 'px';

    /* helper function*/
    function errorElementMaker() {
        function errorWrapper() {
            const error_element = document.createElement('div');
            error_element.className = 'error-content';
            return error_element;
        }
        function timer() {
            const timer = document.createElement('div');
            timer.className = 'error-timer';
            timer.style = "width: 100%";

            let width = 100;
            const intervalId = setInterval(() => {
                width -= 1;
                timer.style.width = width + "%";
                if (width <= 0) {
                    clearInterval(intervalId);
                    timer.style.height = "0";
                    timer.closest('.index-error').style.height = "0";
                    timer.closest('.index-error').style.marginBottom = "0";
                    timer.closest('.error-content').style.padding = "0";
                    timer.closest('.error-content').style.borderColor = "transparent";
                    timer.closest
                    setTimeout(() => {
                        timer.closest('.index-error').remove();
                    }, 600);
                }
            }, 20)
            return timer;
        }
        function textWrapper() {
            const text_wrapper = document.createElement('pre');
            text_wrapper.className = "error-text";
            return text_wrapper;
        }
        return {
            errorWrapper,
            timer,
            textWrapper
        }
    }
}