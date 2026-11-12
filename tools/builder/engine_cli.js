#!/usr/bin/env node
// Usage: node tools/builder/engine_cli.js plan.json  -> prints evaluate() JSON; exit 0 PASS, 1 CONDITIONAL, 2 FAIL/malformed
'use strict';
const fs = require('fs');
const { evaluate } = require('./engine.js');
if (process.argv.length !== 3) { console.error('Usage: node tools/builder/engine_cli.js path/to/plan.json'); process.exit(2); }
try {
  const result = evaluate(JSON.parse(fs.readFileSync(process.argv[2], 'utf8')));
  console.log(JSON.stringify(result, null, 2));
  process.exit(result.status === 'PASS' ? 0 : result.status === 'CONDITIONAL' ? 1 : 2);
} catch (e) {
  console.error('Cannot validate: ' + e.message);
  process.exit(2);
}
