function createAudioPlayer() {
    let currentSound = null;
    let currentUI = null
    const soundCache = new Map();


    const getSound = (src, onLoad, onError, onPlay, onEnd) => {
        if (!soundCache.has(src)) {
            const sound = new Howl({
                src: [src],
                volume: 0.8,
                html5: true,
                preload: true
            });

            sound.once('load', () => {
                onLoad?.();
            });

            sound.once('loaderror', () => {
                console.error(`Failed to load audio: ${src}`);
                soundCache.delete(src);
                onError?.();
            });

            sound.on('playerror', () => {
                console.error(`Failed to play audio: ${src}`);
                onError?.();
            });

            sound.on('play', () => {
                onPlay?.();
            });

            sound.on('end', () => {
                onEnd?.();
            });

            soundCache.set(src, sound);
        }

        return soundCache.get(src);
    };

    const playExclusive = (sound, soundEl, labels) => {
        if (currentSound?.playing()) {
            currentSound.stop();
            // reset previous button UI
            if (currentUI) {
                currentUI.el.textContent = currentUI.labels.play;
                currentUI.el.style.fontStyle = '';
            }
        }
        currentSound = sound;
        currentUI = { el: soundEl, labels };
        sound.play();
    };

    const initElement = (el) => {
        const src = el.dataset.audio;
        el.textContent = langTrans?.['recording'] || (site_lang.toLowerCase() === 'sl' ? 'Audio posnetek: ' : 'Audio recording: ');
        const soundEl = document.createElement('span');

        if (src === 'None' || !isUrl(src)) {
            soundEl.style.cssText = 'color: gray;'
            soundEl.textContent = langTrans?.['unavailable'] || (site_lang.toLowerCase() === 'sl' ? 'ni na voljo' : 'not available');
            el.append(soundEl);
            return
        };

        soundEl.classList.add('sound');

        const labels = {
            play: langTrans?.['play'] || (site_lang.toLowerCase() === 'sl' ? 'Predvajaj' : 'Play'),
            loading: langTrans?.['loading'] || (site_lang.toLowerCase() === 'sl' ? 'Nalaganje...' : 'Loading...'),
            playing: langTrans?.['playing'] || (site_lang.toLowerCase() === 'sl' ? 'Se predvaja...' : 'Playing...'),
            error: langTrans?.['error'] || (site_lang.toLowerCase() === 'sl' ? 'Prišlo je do napake' : 'An error occurred')
        };

        soundEl.textContent = labels.play;
        el.append(soundEl);

        let sound = null;

        soundEl.addEventListener('click', () => {
            if (!sound) {
                soundEl.textContent = labels.loading;

                sound = getSound(
                    src,
                    () => { soundEl.textContent = labels.play; soundEl.style.fontStyle = ''; },                    // onLoad
                    () => { sound = null; soundEl.textContent = labels.error; soundEl.style.fontStyle = ''; },     // onError
                    () => { soundEl.textContent = labels.playing; soundEl.style.fontStyle = 'italic'; },           // onPlay
                    () => { soundEl.textContent = labels.play; soundEl.style.fontStyle = ''; }                     // onEnd
                );
            }

            if (!sound) return; // guard against loaderror nulling sound above

            if (sound.state() === 'loaded') {
                playExclusive(sound, soundEl, labels);
            } else {
                sound.once('load', () => {
                    playExclusive(sound, soundEl, labels);
                });
            }
        });
    };

    const init = (selector = '.audio-item') => {
        document.querySelectorAll(selector).forEach(el => {
            if (el.dataset.audioInit) return; // skip already initialized
            el.dataset.audioInit = 'true';
            initElement(el);
        });
    };

    function isUrl(str) {
      try {
        new URL(str);
        return true;
      } catch {
        return false;
      }
    }

    return { init };
}