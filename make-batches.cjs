const fs = require('fs');
const path = require('path');
for (const owner of ['codex', 'grok', 'deepseek']) {
  const source = fs.readFileSync(path.join('partitions', `${owner}.pot`), 'utf8').replace(/\r\n/g, '\n');
  const blocks = source.trimEnd().split(/\n[ \t]*\n/);
  const header = blocks.shift();
  const target = path.join('batches', owner);
  fs.mkdirSync(target, { recursive: true });
  for (let i = 0; i < blocks.length; i += 100) {
    const file = `${owner}-${String(i / 100 + 1).padStart(3, '0')}.pot`;
    fs.writeFileSync(path.join(target, file), [header, ...blocks.slice(i, i + 100)].join('\n\n') + '\n');
  }
  console.log(`${owner}: ${blocks.length} messages, ${Math.ceil(blocks.length / 100)} batches`);
}
