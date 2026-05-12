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

    /*
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
    */

    const playExclusive = (sound, soundEl, pathData, elData) => {
        if (currentSound?.playing()) {
            currentSound.stop();
            // reset previous button UI
            if (currentUI) {
                
                Object.assign(soundEl, elData.play);
                const path = currentUI.el.querySelector('path');
                for (const [key, value] of Object.entries(pathData.play)) {
                    path.setAttribute(key, value);
                }
                console.log('path was assgined this data...')
                console.log('path: ', path);
                console.log('data: ', pathData.play);
            }
        }
        currentSound = sound;
        currentUI = { el: soundEl, pathData, elData };
        sound.play();
    };

    const initElement = (el) => {
        const src = el.dataset.audio;
        //el.textContent = langTrans?.['recording'] || (site_lang.toLowerCase() === 'sl' ? 'Audio posnetek: ' : 'Audio recording: ');
        //const soundEl = document.createElement('span');
        const soundEl = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        soundEl.setAttribute('width', '32');
        soundEl.setAttribute('height', '32');
        soundEl.setAttribute('viewBox', '0 0 640 640');
        soundEl.style.height = '1rem';
        soundEl.style.border = 'unset';
        soundEl.style.width = 'min-content';
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        soundEl.append(path);

        if (src === 'None' || !isUrl(src)) {
            return;
            soundEl.style.cssText = 'color: gray;'
            soundEl.textContent = langTrans?.['unavailable'] || (site_lang.toLowerCase() === 'sl' ? 'ni na voljo' : 'not available');
            soundEl.style.display = 'none';
            el.append(soundEl);
            el.style.display = "none";
            return;
        };

        soundEl.classList.add('sound');

        const labels = {
            play: langTrans?.['play'] || (site_lang.toLowerCase() === 'sl' ? 'Predvajaj' : 'Play'),
            loading: langTrans?.['loading'] || (site_lang.toLowerCase() === 'sl' ? 'Nalaganje...' : 'Loading...'),
            playing: langTrans?.['playing'] || (site_lang.toLowerCase() === 'sl' ? 'Se predvaja...' : 'Playing...'),
            error: langTrans?.['error'] || (site_lang.toLowerCase() === 'sl' ? 'Prišlo je do napake' : 'An error occurred')
        };

        const elData = {
            play: {
                alt: labels.play,
                title: labels.play,
            },
            loading: {
                alt: labels.loading,
                title: labels.loading,
            },
            playing: {
                alt: labels.playing,
                title: labels.playing,
            }
        }
        const pathData = {
            play: {
                d: 'M112 416L160 416L294.1 535.2C300.5 540.9 308.7 544 317.2 544C336.4 544 352 528.4 352 509.2L352 130.8C352 111.6 336.4 96 317.2 96C308.7 96 300.5 99.1 294.1 104.8L160 224L112 224C85.5 224 64 245.5 64 272L64 368C64 394.5 85.5 416 112 416zM505.1 171C494.8 162.6 479.7 164.2 471.3 174.5C462.9 184.8 464.5 199.9 474.8 208.3C507.3 234.7 528 274.9 528 320C528 365.1 507.3 405.3 474.8 431.8C464.5 440.2 463 455.3 471.3 465.6C479.6 475.9 494.8 477.4 505.1 469.1C548.3 433.9 576 380.2 576 320.1C576 260 548.3 206.3 505.1 171.1zM444.6 245.5C434.3 237.1 419.2 238.7 410.8 249C402.4 259.3 404 274.4 414.3 282.8C425.1 291.6 432 305 432 320C432 335 425.1 348.4 414.3 357.3C404 365.7 402.5 380.8 410.8 391.1C419.1 401.4 434.3 402.9 444.6 394.6C466.1 376.9 480 350.1 480 320C480 289.9 466.1 263.1 444.5 245.5z',
            },
            loading: {
                d: 'M128 128C128 92.7 156.7 64 192 64L341.5 64C358.5 64 374.8 70.7 386.8 82.7L493.3 189.3C505.3 201.3 512 217.6 512 234.6L512 512C512 547.3 483.3 576 448 576L192 576C156.7 576 128 547.3 128 512L128 128zM336 122.5L336 216C336 229.3 346.7 240 360 240L453.5 240L336 122.5zM303 505C312.4 514.4 327.6 514.4 336.9 505L400.9 441C410.3 431.6 410.3 416.4 400.9 407.1C391.5 397.8 376.3 397.7 367 407.1L344 430.1L344 344C344 330.7 333.3 320 320 320C306.7 320 296 330.7 296 344L296 430.1L273 407.1C263.6 397.7 248.4 397.7 239.1 407.1C229.8 416.5 229.7 431.7 239.1 441L303.1 505z',
            },
            playing: {
                d: 'M552 256L408 256C398.3 256 389.5 250.2 385.8 241.2C382.1 232.2 384.1 221.9 391 215L437.7 168.3C362.4 109.7 253.4 115 184.2 184.2C109.2 259.2 109.2 380.7 184.2 455.7C259.2 530.7 380.7 530.7 455.7 455.7C463.9 447.5 471.2 438.8 477.6 429.6C487.7 415.1 507.7 411.6 522.2 421.7C536.7 431.8 540.2 451.8 530.1 466.3C521.6 478.5 511.9 490.1 501 501C401 601 238.9 601 139 501C39.1 401 39 239 139 139C233.3 44.7 382.7 39.4 483.3 122.8L535 71C541.9 64.1 552.2 62.1 561.2 65.8C570.2 69.5 576 78.3 576 88L576 232C576 245.3 565.3 256 552 256z',
            }
        }

        //soundEl.textContent = labels.play;
        for (const [key, value] of Object.entries(pathData.play)) {
            path.setAttribute(key, value);
        }
        
        el.append(soundEl);

        let sound = null;

        soundEl.addEventListener('click', () => {
            if (!sound) {
                //soundEl.textContent = labels.loading;
                const path = soundEl.querySelector('path');
                Object.assign(soundEl, elData.play);
                for (const [key, value] of Object.entries(pathData.loading)) {
                    path.setAttribute(key, value);
                }
                console.log('path was assgined this data...')
                console.log('path: ', path);
                console.log('data: ', pathData.loading);

                sound = getSound(
                    src,
                    /*
                    () => { soundEl.textContent = labels.play; soundEl.style.fontStyle = ''; },                    // onLoad
                    () => { sound = null; soundEl.textContent = labels.error; soundEl.style.fontStyle = ''; },     // onError
                    () => { soundEl.textContent = labels.playing; soundEl.style.fontStyle = 'italic'; },           // onPlay
                    () => { soundEl.textContent = labels.play; soundEl.style.fontStyle = ''; }                     // onEnd
                    */
                    () => {
                        Object.assign(soundEl, elData.play);
                        for (const [key, value] of Object.entries(pathData.play)) {
                            path.setAttribute(key, value);
                        }
                    },                        // onLoad
                    () => { sound = null; soundEl.display = 'none'; },                     // onError
                    () => {
                        Object.assign(soundEl, elData.playing);
                        for (const [key, value] of Object.entries(pathData.playing)) {
                            path.setAttribute(key, value);
                        }
                    },                     // onPlay
                    () => { 
                        Object.assign(soundEl, elData.play);
                        for (const [key, value] of Object.entries(pathData.play)) {
                            path.setAttribute(key, value);
                        }
                    }                         // onEnd
                );
            }

            if (!sound) return; // guard against loaderror nulling sound above

            /*
            if (sound.state() === 'loaded') {
                playExclusive(sound, soundEl, labels);
            } else {
                sound.once('load', () => {
                    playExclusive(sound, soundEl, labels);
                });
            }
            */
            
            if (sound.state() === 'loaded') {
                playExclusive(sound, soundEl, pathData, elData);
            } else {
                sound.once('load', () => {
                    playExclusive(sound, soundEl, pathData, elData);
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