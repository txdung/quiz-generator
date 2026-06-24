const XLSX = require('xlsx');
const fs = require('fs');

// Read current HTML
const html = fs.readFileSync('./quiz_generator/quiz_generator.html', 'utf-8');

// Extract current embeddedQuestions
const fullTag = 'let embeddedQuestions = [';
const fullTagIdx = html.indexOf(fullTag);
let depth = 0, i = fullTagIdx + fullTag.length - 1;
let arrayStart = -1, arrayEnd = -1;
while (i < html.length) {
    if (html[i] === '[') { if (depth === 0) arrayStart = i; depth++; }
    else if (html[i] === ']') { depth--; if (depth === 0) { arrayEnd = i; break; } }
    i++;
}
const arrayText = html.substring(arrayStart + 1, arrayEnd);
let allQuestions = JSON.parse('[' + arrayText + ']');
console.log('Current VHF questions:', allQuestions.filter(q => q.mode === 'vhf').length);
console.log('Current Radar questions:', allQuestions.filter(q => q.mode === 'radar').length);

// Radar files to process
const radarFiles = [
    { filename: 'NH Câu hỏi, ĐA Lý thuyết_Nguyên lý PSR _16.5.2026.xlsx', sheetName: 'PSR (Sơ cấp)' },
    { filename: 'NH Câu hỏi, ĐA Lý thuyết_Nguyên lý SSR _5.2026.xlsx', sheetName: 'SSR (Thứ cấp)' },
    { filename: 'NH Câu hỏi, ĐA Lý thuyết_Radar_Indra_PSR_SSR INDRA_5.2026.xlsx', sheetName: 'Indra PSR SSR' }
];

let radarCount = 0;
radarFiles.forEach(file => {
    const filepath = 'C:/Users/txdun/my-pi-project/quiz_generator/' + file.filename;
    try {
        const wb = XLSX.readFile(filepath);
        const sheet = wb.Sheets[wb.SheetNames[0]];
        const rows = XLSX.utils.sheet_to_json(sheet, { header: 1 });
        
        let fileCount = 0;
        for (let r = 0; r < rows.length; r++) {
            const row = rows[r];
            if (!row || row.length < 7) continue;
            
            const num = row[0];
            if (typeof num !== 'number' || num < 1) continue;
            
            const text = String(row[1] || '').trim();
            if (!text || text.includes('Số TT') || text.includes('Nội dung câu hỏi')) continue;
            
            // Get correct answer
            let correct = String(row[2] || '').trim().toUpperCase();
            const numMap = { '1': 'A', '2': 'B', '3': 'C', '4': 'D' };
            if (numMap[correct]) correct = numMap[correct];
            if (!['A', 'B', 'C', 'D'].includes(correct)) continue;
            
            // Get options
            function cleanOpt(opt) {
                if (!opt) return '';
                return String(opt).replace(/^[A-D][.\s)]+\s*/i, '').trim();
            }
            
            const optA = cleanOpt(String(row[3] || ''));
            const optB = cleanOpt(String(row[4] || ''));
            const optC = cleanOpt(String(row[5] || ''));
            const optD = cleanOpt(String(row[6] || ''));
            if (!optA || !optB) continue;
            
            allQuestions.push({
                number: num,
                text: text,
                correct: correct,
                sheet: file.sheetName,
                mode: 'radar',
                options: { A: optA, B: optB, C: optC, D: optD }
            });
            fileCount++;
            radarCount++;
        }
        console.log('Added ' + fileCount + ' radar questions from ' + file.sheetName);
    } catch (e) {
        console.log('Error reading ' + file.filename + ': ' + e.message);
    }
});

console.log('Total radar questions added:', radarCount);
console.log('Total VHF questions:', allQuestions.filter(q => q.mode === 'vhf').length);
console.log('Total questions:', allQuestions.length);

// Update HTML with new embeddedQuestions
const newBlock = JSON.stringify(allQuestions, null, 4);
const before = html.substring(0, fullTagIdx + fullTag.length);
const after = html.substring(arrayEnd + 1);
const newHtml = before + newBlock + after;

fs.writeFileSync('./quiz_generator/quiz_generator.html', newHtml);

// Update info box
const newHtml2 = newHtml.replace(
    'id="infoTitle">✅ Câu hỏi nhúng sẵn — chọn sheet bên dưới',
    `id="infoTitle">✅ ${allQuestions.filter(q => q.mode === 'vhf').length} VHF + ${allQuestions.filter(q => q.mode === 'radar').length} Radar — chọn chế độ bên dưới`
);

fs.writeFileSync('./quiz_generator/quiz_generator.html', newHtml2);

console.log('✅ HTML updated!');
console.log('VHF sheets:', [...new Set(allQuestions.filter(q => q.mode === 'vhf').map(q => q.sheet))]);
console.log('Radar sheets:', [...new Set(allQuestions.filter(q => q.mode === 'radar').map(q => q.sheet))]);
