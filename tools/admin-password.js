#!/usr/bin/env node
// Make the ADMIN_PASSWORD_HASH value for the admin portal from a password.
//
//   node tools/admin-password.js 'the new password'
//
// Put the printed line in Vercel (project amami-italia → Settings → Environment
// Variables → ADMIN_PASSWORD_HASH, Production) and redeploy. Changing it signs
// out every open session. The password itself is never stored anywhere.
const crypto = require('crypto');

const pw = process.argv[2];
if (!pw || pw.length < 10) {
  console.error('Give a password of at least 10 characters.');
  process.exit(1);
}
const N = 16384, r = 8, p = 1;
const salt = crypto.randomBytes(16);
const hash = crypto.scryptSync(pw, salt, 32, { N, r, p });
console.log(['scrypt', N, r, p, salt.toString('base64'), hash.toString('base64')].join('$'));
