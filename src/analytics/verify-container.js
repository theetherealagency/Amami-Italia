const fs = require('fs');
const path = require('path');
const { JSDOM } = require(process.env.SP + '/node_modules/jsdom');
const REPO = '/Users/muskangilani/amami-italia';

const scriptSrc = fs.readFileSync(REPO + '/analytics/gtm-event-tracking.html', 'utf8');
const js = scriptSrc.replace(/^[\s\S]*?<script>/, '').replace(/<\/script>[\s\S]*$/, '');
/* strip regex literals so 'tel:'/'mailto:' inside patterns aren't read as payload keys */
const jsClean = js.replace(/\/\^?[^\/\n]+\/[gimsuy]*/g, 'RX');
const container = JSON.parse(fs.readFileSync(REPO + '/analytics/GTM-MNHMB7C9-container-import.json', 'utf8'));
const cv = container.containerVersion;

/* ---- what the container declares ---- */
const tagEvents = cv.tag.filter(t => t.type === 'gaawe').map(t => ({
  name: t.parameter.find(p => p.key === 'eventName').value,
  params: (t.parameter.find(p => p.key === 'eventSettingsTable') || { list: [] }).list
    .map(m => m.map.find(k => k.key === 'parameter').value),
  trigger: t.firingTriggerId[0],
}));
const triggerByName = {};
cv.trigger.forEach(t => {
  const ev = t.customEventFilter[0].parameter.find(p => p.key === 'arg1').value;
  triggerByName[ev] = t.triggerId;
});
const dlvNames = new Set(cv.variable.filter(v => v.type === 'v')
  .map(v => v.parameter.find(p => p.key === 'name').value));

/* ---- what the script actually emits (static parse of push() calls) ---- */
const emitted = {};
const re = /push\('([a-z_]+)',\s*\{([^}]*)\}/g;
let m;
while ((m = re.exec(jsClean))) {
  const ev = m[1];
  const keys = [...m[2].matchAll(/(\w+)\s*:/g)].map(x => x[1]);
  emitted[ev] = new Set([...(emitted[ev] || []), ...keys]);
}
/* fire() calls inherit link_text/link_url/link_location, plus cta_style when CTA */
const FIRE_BASE = ['link_text', 'link_url', 'link_location'];
const fireRe = /fire\('([a-z_]+)',\s*\{([^}]*)\}/g;
while ((m = fireRe.exec(jsClean))) {
  const ev = m[1];
  const keys = [...m[2].matchAll(/(\w+)\s*:/g)].map(x => x[1]);
  emitted[ev] = new Set([...(emitted[ev] || []), ...keys, ...FIRE_BASE]);
}

console.log('\n═══ CONTAINER INTEGRITY ═══');
let problems = [];
console.log(`  tags:      ${cv.tag.length}  (1 GA4 config + 1 custom HTML + ${tagEvents.length} event tags)`);
console.log(`  triggers:  ${cv.trigger.length}`);
console.log(`  variables: ${cv.variable.length}  (${dlvNames.size} data layer + 1 constant)`);

cv.tag.forEach(t => { if (!t.firingTriggerId || !t.firingTriggerId.length) problems.push(`tag "${t.name}" has NO trigger`); });
const usedTriggers = new Set(cv.tag.flatMap(t => t.firingTriggerId || []));
cv.trigger.forEach(t => { if (!usedTriggers.has(t.triggerId)) problems.push(`trigger "${t.name}" is never used`); });

console.log('\n═══ TAG ↔ TRIGGER ↔ SCRIPT ═══');
const rows = [];
tagEvents.forEach(t => {
  const trigOk = triggerByName[t.name] === t.trigger;
  const emits = emitted[t.name];
  const missingVars = t.params.filter(p => !dlvNames.has(p));
  const unmapped = emits ? [...emits].filter(p => !t.params.includes(p)) : [];
  rows.push({ ev: t.name, trigOk, emits: !!emits, missingVars, unmapped });
  if (!trigOk) problems.push(`${t.name}: trigger mismatch`);
  if (!emits) problems.push(`${t.name}: tag exists but script never pushes it`);
  missingVars.forEach(p => problems.push(`${t.name}: parameter "${p}" has no Data Layer Variable`));
  unmapped.forEach(p => problems.push(`${t.name}: script sends "${p}" but tag does not map it`));
});
rows.forEach(r => {
  const flags = [r.trigOk ? 'trig✓' : 'trig✗', r.emits ? 'script✓' : 'script✗',
                 r.missingVars.length ? 'vars✗' : 'vars✓',
                 r.unmapped.length ? 'map✗' : 'map✓'].join(' ');
  console.log(`  ${r.ev.padEnd(21)} ${flags}` +
    (r.missingVars.length ? `  missing DLV: ${r.missingVars}` : '') +
    (r.unmapped.length ? `  unmapped: ${r.unmapped}` : ''));
});

/* script emits an event with no tag? */
Object.keys(emitted).forEach(ev => {
  if (!tagEvents.find(t => t.name === ev)) problems.push(`script pushes "${ev}" but container has NO tag for it`);
});

console.log('\n═══ RESULT ═══');
if (problems.length) { problems.forEach(p => console.log('  ✗ ' + p)); }
else console.log('  ✓ container is internally consistent and matches the script exactly');
console.log(`  ${problems.length} problem(s)\n`);
process.exit(0);
