const fs = require('fs');
const SP = process.env.SP;
const acorn = require(SP + '/node_modules/acorn');
const src = fs.readFileSync(SP + '/t5.js', 'utf8');

/* 1. Does it parse as strict ES5? */
let ast;
try {
  ast = acorn.parse(src, { ecmaVersion: 5, sourceType: 'script', locations: true });
  console.log('ES5 parse (ecmaVersion:5): PASS');
} catch (e) {
  console.log('ES5 parse: FAIL ->', e.message);
  ast = acorn.parse(src, { ecmaVersion: 2020, sourceType: 'script', locations: true });
}

/* 2. Any FunctionDeclaration whose direct parent is a plain block? */
const FUNC = new Set(['FunctionDeclaration', 'FunctionExpression', 'ArrowFunctionExpression', 'Program']);
const bad = [];
(function walk(node, parent, grand) {
  if (!node || typeof node.type !== 'string') return;
  if (node.type === 'FunctionDeclaration' && parent && parent.type === 'BlockStatement') {
    // legal only when the block is a function body
    if (!grand || !FUNC.has(grand.type)) {
      bad.push({ name: node.id && node.id.name, line: node.loc.start.line, inside: grand && grand.type });
    }
  }
  for (const k in node) {
    const v = node[k];
    if (Array.isArray(v)) v.forEach(c => c && typeof c.type === 'string' && walk(c, node, parent));
    else if (v && typeof v.type === 'string') walk(v, node, parent);
  }
})(ast, null, null);

if (bad.length) {
  console.log('block-scoped function declarations (GTM will reject these):');
  bad.forEach(b => console.log(`   line ${b.line}  function ${b.name}()  inside ${b.inside}`));
} else {
  console.log('block-scoped function declarations: NONE');
}
