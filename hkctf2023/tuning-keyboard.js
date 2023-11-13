function parseHslValuesFromText(text) {
    hslTexts = text.split(';');
    return hslTexts.map(hslText => {
        let match = hslText.match(/hsl\((.+?)rad,(.+?)%,(.+?)%\)/);
        if (match) {
            let hueInRadians = parseFloat(match[1]);
            let hueInDegrees = hueInRadians * 180 / Math.PI;
            return [hueInDegrees, parseFloat(match[2]), parseFloat(match[3])];
        }
    });
}

// https://stackoverflow.com/a/44134328/13109740
function hslToHex(h, s, l) {
    h /= 360;
    s /= 100;
    l /= 100;
    let r, g, b;
    if (s === 0) {
        r = g = b = l; // achromatic
    } else {
        const hue2rgb = (p, q, t) => {
            if (t < 0) t += 1;
            if (t > 1) t -= 1;
            if (t < 1 / 6) return p + (q - p) * 6 * t;
            if (t < 1 / 2) return q;
            if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
            return p;
        };
        const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
        const p = 2 * l - q;
        r = hue2rgb(p, q, h + 1 / 3);
        g = hue2rgb(p, q, h);
        b = hue2rgb(p, q, h - 1 / 3);
    }
    const toHex = x => {
        const hex = Math.round(x * 255).toString(16);
        return hex.length === 1 ? '0' + hex : hex;
    };
    return `${toHex(r)}${toHex(g)}${toHex(b)}`;
}

magic = Array.from(document.querySelectorAll('animate[attributeName="fill"]')).map(nl => {
    let elmValuesText = nl.getAttribute('values');
    let hslValues = parseHslValuesFromText(elmValuesText);
    let hexValues = hslValues.map(hsl => hslToHex(...hsl));
    return hexValues;
});

// 東南西北
res = "";
for (i = 0; i < magic[0].length; i++) {
    for (j = 0; j < 4; j++) {
        res += magic[j][i];
    }
}

// send the res to good old cyberchef
// https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')From_Base64('A-Za-z0-9%2B/%3D',true,false)
