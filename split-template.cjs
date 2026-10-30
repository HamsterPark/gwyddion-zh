// Split a frozen gettext template without modifying message blocks.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const root = __dirname;
const source = path.join(root, 'source', 'gwyddion-2.71.pot');
const original = fs.readFileSync(source);
const data = original.toString('utf8');
if (Buffer.from(data, 'utf8').compare(original)) throw Error('Input is not valid UTF-8');
const blocks = data.replace(/\r\n/g, '\n').trimEnd().split(/\n[ \t]*\n/);
const header = blocks.shift();
if (!header || !/^msgid ""$/m.test(header)) throw Error('Missing POT header');
function field(block, name) {
  const lines = block.split('\n');
  let pos = lines.findIndex(x => x.startsWith(name + ' '));
  if (pos < 0) return null;
  const pieces = [lines[pos].slice(name.length + 1)];
  while (++pos < lines.length && lines[pos].startsWith('"')) pieces.push(lines[pos]);
  return pieces.map(x => JSON.parse(x)).join('');
}
function references(block) {
  return [...block.matchAll(/^#: (.*)$/gm)].flatMap(m => m[1].trim().split(/\s+/)).map(x => x.replace(/:\d+$/, ''));
}
// Shared messages and anything outside recognizable modules remain with Codex.
// This list is intentionally conservative: it captures families of difficult
// microscopy, levelling, roughness and statistics operations by source filename.
const difficult = /(?:grain|tip|rough|stat|acf|psdf|hhcf|correl|facet|level|flatten|linecorrect|linematch|blockstep|arc-revolve|sphere-revolve|median-bg|polylevel|trimmed-mean|rank-filter|outlier|fractal|curvature|slope|entropy|hertz|indent|lattice|terrace|force)/i;
const groups = {codex: [], grok: [], deepseek: []};
const seen = new Set();
const shared = [];
for (const block of blocks) {
  const id = field(block, 'msgid');
  if (id === null || id === '') throw Error('Unexpected empty or missing msgid');
  const context = field(block, 'msgctxt');
  const plural = field(block, 'msgid_plural');
  const key = JSON.stringify([context, id, plural]);
  if (seen.has(key)) throw Error('Duplicate message key: ' + key);
  seen.add(key);
  const refs = [...new Set(references(block))];
  const isShared = refs.length > 1;
  let target;
  if (isShared || refs.length !== 1) target = 'codex';
  else if (refs[0].startsWith('modules/file/')) target = 'grok';
  else if (!refs[0].startsWith('modules/') || difficult.test(refs[0])) target = 'codex';
  else target = 'deepseek';
  groups[target].push(block);
  if (isShared) shared.push({context, id, plural, references: refs});
}
const partition = path.join(root, 'partitions');
fs.mkdirSync(partition, {recursive: true});
for (const [name, items] of Object.entries(groups)) {
  fs.writeFileSync(path.join(partition, name + '.pot'), [header, ...items].join('\n\n') + '\n', 'utf8');
}
fs.writeFileSync(path.join(partition, 'shared-review.json'), JSON.stringify(shared, null, 2) + '\n', 'utf8');
const outputKeys = new Set();
let outputTotal = 0;
for (const name of Object.keys(groups)) {
  const outputBlocks = fs.readFileSync(path.join(partition, name + '.pot'), 'utf8').trimEnd().split(/\n[ \t]*\n/);
  if (outputBlocks.shift() !== header) throw Error('Header mismatch');
  for (const block of outputBlocks) {
    const key = JSON.stringify([field(block, 'msgctxt'), field(block, 'msgid'), field(block, 'msgid_plural')]);
    if (outputKeys.has(key) || !seen.has(key)) throw Error('Duplicate or unknown output key: ' + key);
    outputKeys.add(key);
    outputTotal++;
  }
}
if (outputTotal !== blocks.length || outputKeys.size !== seen.size) throw Error('Counts do not reconcile');
const sha = crypto.createHash('sha256').update(original).digest('hex');
const summary = `# Gwyddion 2.71 翻译分片说明\n\n` +
  `源文件：\`source/gwyddion-2.71.pot\`；SHA-256：\`${sha}\`。每片保留原模板的头、条目原文、引用、注释和标记；头是 POT 模板头，尚不是可直接编译的中文 PO 头。\n\n` +
  `| 分片 | 职责 | 条目数（不含头） |\n| --- | --- | ---: |\n` +
  `| codex.pot | 核心、库、专业难项、共享及无法归类的条目 | ${groups.codex.length} |\n` +
  `| grok.pot | 独占文件导入导出模块 | ${groups.grok.length} |\n` +
  `| deepseek.pot | 其他独占功能模块 | ${groups.deepseek.length} |\n` +
  `| 合计 | 源模板全部条目 | ${outputTotal} |\n\n` +
  `按源文件引用归类；同一条目引用超过一个不同源文件时，不论涉及哪些组，一律归 Codex。共 ${shared.length} 条共享条目列于 \`shared-review.json\`，后续按上下文核查。无引用及非 modules 路径归 Codex；单一引用的 modules/file 归 Grok；其余模块按源文件名匹配颗粒、针尖、调平、统计等术语归 Codex，其余归 DeepSeek。此为保守的文件名规则，可能遗漏专业内容或把普通项目纳入难项，需人工复核。\n\n` +
  `校验：按上下文、原文、复数原文构成键，源文件无重复；三个输出之间无重复或未知键，输出总数与源文件相同，且每片头与源模板一致。源引用为定位上下文，不是要求翻译源代码。分片是翻译模板而非已完成的译文。\n\n` +
  `交付翻译时请保留每个条目的 msgid、msgctxt、msgid_plural、引用、注释和格式标记，仅填写译文；遵循项目术语表。保留格式占位符、转义、标记和助记符，无法确定时留空并说明。回收后应对照原模板合并、核对遗漏和冲突、使用 gettext 工具检查，再通过程序实测。\n`;
fs.writeFileSync(path.join(partition, 'README.md'), summary, 'utf8');
console.log(summary);
