import random
import asyncio

async def human_like_delay(page, min_ms=500, max_ms=1500):
    """Waits for a random amount of time to simulate human processing speed."""
    delay = random.uniform(min_ms, max_ms)
    await page.wait_for_timeout(delay)

async def human_mouse_move(page):
    """Simulates realistic mouse jitter and movement."""
    # Move mouse to a random position with random steps to simulate human curve
    for _ in range(random.randint(3, 7)):
        x = random.randint(100, 800)
        y = random.randint(100, 600)
        await page.mouse.move(x, y, steps=random.randint(5, 10))
        await page.wait_for_timeout(random.uniform(50, 150))

async def human_type(page, selector, text, mistake_prob=0.1):
    """
    Types text into a selector like a human, with occasional mistakes and corrections.
    
    Args:
        page: The Playwright page object.
        selector: The input field selector.
        text: The text to type.
        mistake_prob: Probability (0.0 to 1.0) of making a mistake per character.
    """
    await page.click(selector)
    
    chars = list(text)
    # Mapping of keys to their neighbors on a QWERTY keyboard for realistic typos
    qwerty_neighbors = {
        '1': '2q', '2': '13qw', '3': '24we', '4': '35er', '5': '46rt', '6': '57ty', '7': '68yu', '8': '79ui', '9': '80io', '0': '9op',
        'q': '12wa', 'w': 'qase23', 'e': 'wsdr34', 'r': 'edft45', 't': 'rfgy56', 'y': 'tghu67', 'u': 'yhij78', 'i': 'ujko89', 'o': 'iklp90', 'p': 'ol0',
        'a': 'qwsz', 's': 'qazxde', 'd': 'wsxcfr', 'f': 'edcvgt', 'g': 'rfvbhy', 'h': 'tgbnju', 'j': 'yhnmki', 'k': 'ujmlo', 'l': 'ikp',
        'z': 'asx', 'x': 'zsdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn', 'n': 'bhjm', 'm': 'njk'
    }

    for char in chars:
        # Mistake logic: occasional random wrong key if neighbor known
        if random.random() < mistake_prob and char.lower() in qwerty_neighbors:
            wrong_char = random.choice(qwerty_neighbors[char.lower()])
            await page.keyboard.type(wrong_char)
            await page.wait_for_timeout(random.uniform(100, 400)) # Reaction time
            await page.keyboard.press("Backspace")
            await page.wait_for_timeout(random.uniform(100, 300)) # Correction time
        
        await page.keyboard.type(char)
        await page.wait_for_timeout(random.uniform(50, 200)) # Random delay between keys

async def stealth_mask_webdriver(page):
    """Injects a script to hide the navigator.webdriver property."""
    await page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)

async def stealth_spoof_canvas(page):
    """
    Injects a script to add random noise to HTML5 Canvas readouts.
    This prevents consistent canvas fingerprinting.
    """
    await page.add_init_script("""
        const toBlob = HTMLCanvasElement.prototype.toBlob;
        const toDataURL = HTMLCanvasElement.prototype.toDataURL;
        const getImageData = CanvasRenderingContext2D.prototype.getImageData;
        
        // Generate a random noise value for this session
        const noise = {
            r: Math.floor(Math.random() * 10) - 5,
            g: Math.floor(Math.random() * 10) - 5,
            b: Math.floor(Math.random() * 10) - 5,
            a: Math.floor(Math.random() * 10) - 5
        };

        const shift = function(context, width, height) {
            const imageData = getImageData.call(context, 0, 0, width, height);
            for (let i = 0; i < height; i++) {
                for (let j = 0; j < width; j++) {
                    const index = ((i * (width * 4)) + (j * 4));
                    imageData.data[index] = imageData.data[index] + noise.r;
                    imageData.data[index + 1] = imageData.data[index + 1] + noise.g;
                    imageData.data[index + 2] = imageData.data[index + 2] + noise.b;
                    imageData.data[index + 3] = imageData.data[index + 3] + noise.a;
                }
            }
            context.putImageData(imageData, 0, 0);
        };

        HTMLCanvasElement.prototype.toBlob = function() {
            shift(this.getContext('2d'), this.width, this.height);
            return toBlob.apply(this, arguments);
        };

        HTMLCanvasElement.prototype.toDataURL = function() {
            shift(this.getContext('2d'), this.width, this.height);
            return toDataURL.apply(this, arguments);
        };
    """)

async def stealth_spoof_audio(page):
    """
    Injects a script to add random noise to AudioContext readouts.
    """
    await page.add_init_script("""
        const getChannelData = AudioBuffer.prototype.getChannelData;
        
        AudioBuffer.prototype.getChannelData = function() {
            const results = getChannelData.apply(this, arguments);
            for (let i = 0; i < results.length; i += 100) {
                // Add tiny random noise every 100 samples
                results[i] += (Math.random() * 0.0001);
            }
            return results;
        };
    """)
