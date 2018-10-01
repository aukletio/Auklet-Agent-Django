console.log('Converting SemVer version to PEP-440 version...');
const version = process.argv[2];
// [N!]N(.N)*[{a|b|rc}N][.postN][.devN]
var version440 = '';
if (version === '0.1.0-a.local.circleci.build') {
  version440 = '0.1.0a0.dev0+local.circleci.build';
} else if (version === '0.1.0-a.pr.circleci.build') {
  version440 = '0.1.0a0.dev0+pr.circleci.build';
} else if (version.indexOf('-beta.') !== -1) {
  const re = /(.+)-beta\.(.+)\+(.+)/;
  version440 = version.replace(re, '$1b$2');
} else if (version.indexOf('-rc.') !== -1) {
  const re = /(.+)-rc\.(.+)\+(.+)/;
  version440 = version.replace(re, '$1rc$2');
} else if (version.indexOf('-a.pr.') !== -1) {
  const re = /(.+)-a\.pr\.(.+)\+(.+)/;
  version440 = version.replace(re, '$1a$2');
} else if (version.indexOf('-a.branch.') !== -1) {
  const re = /(.+)-a\.branch\.(.+)\+(.+)/;
  version440 = version.replace(re, '$1a0.dev0+branch.$2');
} else {
  const re = /(.+)\+(.+)/;
  version440 = version.replace(re, '$1');
}
console.log(`PEP-440 version: ${version440}`);
const fs = require('fs');
fs.writeFileSync('.version440', version440);
