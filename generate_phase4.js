const fs = require('fs');

function extractTextFromXml(xmlPath) {
    const xml = fs.readFileSync(xmlPath, 'utf8');
    const regex = /<w:t[^>]*>(.*?)<\/w:t>/g;
    let match;
    let text = [];
    while ((match = regex.exec(xml)) !== null) {
        text.push(match[1]);
    }
    return text.join('\n');
}

const out = extractTextFromXml('C:\\Users\\tmalu\\.gemini\\antigravity\\scratch\\CurrentPrices\\word\\document.xml');
fs.writeFileSync('C:\\Users\\tmalu\\.gemini\\antigravity\\scratch\\CurrentPrices.txt', out);
console.log('done');
