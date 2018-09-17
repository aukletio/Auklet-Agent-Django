// Setup the GitHub API connection.
const cp = require("child_process");
const rp = require('request-promise');
const plh = require('parse-link-header');
const fs = require('fs');
const apiPrefix = 'https://api.github.com/';
const github = rp.defaults({
  baseUrl: apiPrefix,
  headers: {
    'User-Agent': process.env.BOT_GIT_USERNAME,
    'Authorization': `Token ${process.env.CHANGELOG_GITHUB_TOKEN}`
  },
  json: true,
  resolveWithFullResponse: true
});
// Grab inputs.
const org = process.env.CIRCLE_PROJECT_USERNAME;
const repo = process.env.CIRCLE_PROJECT_REPONAME;
const branch = process.env.CIRCLE_BRANCH;
const repoDir = process.argv[2];
const baseVersion = process.argv[3];
const prNumber = process.argv[4];
console.log('Calculating next version based on closed issues/PRs since the last production release...');

// 1. Get the entire commit history for the tag.
console.log('Finding all commits in the target production tag...');
execPromise(`git log --pretty=%H ${baseVersion} | jq --raw-input --slurp 'split("\n") | map(select(length > 0))'`, {
  cwd: repoDir
}).then(function(tagStdout) {
  tagCommits = JSON.parse(tagStdout);
  // 2. Get the entire commit history for HEAD.
  console.log('Finding all commits in HEAD...');
  execPromise('git log --pretty=%H HEAD | jq --raw-input --slurp \'split("\n") | map(select(length > 0))\'', {
    cwd: repoDir
  }).then(function(headStdout) {
    headCommits = JSON.parse(headStdout);
    // 3. Get all closed PRs in this repo.
    console.log('Getting all closed PRs in this repo...');
    getPaginated({
      uri: `/repos/${org}/${repo}/pulls?per_page=100&state=closed&sort=updated`
    }).then(function(closedPrs) {
      // 4. Compare the list of closed PRs to the list of tag commits
      // and figure out what kinds of unmerged changes there are.
      cleanseResults(tagCommits, headCommits, closedPrs);
    }).catch(handleError);
  }).catch(handleError);
}).catch(handleError);

function cleanseResults(tagCommits, headCommits, closedPrs) {
  // Not all closed PRs are merged. We only want merged PRs.
  // Also, skip all release PRs.
  console.log('Selecting non-release PRs that have been merged into HEAD but not into the target tag...');
  var eligiblePrs = closedPrs.filter(function(pr) {
    var labels = pr.labels.map(function(label) { return label.name; });
    return pr.merged_at !== null && !labels.includes('release') && headCommits.includes(pr.merge_commit_sha);
  });
  // If this is a PR, add it to the list of eligible PRs.
  if (prNumber) {
    github.get({
      uri: `/repos/${org}/${repo}/pulls/${prNumber}`
    }).then(function(response) {
      // Only 200 is an acceptable response.
      if (response.statusCode === 200) {
        console.log('Including this PR in the list of impacting PRs...');
        eligiblePrs.push(response.body);
        parseResults(tagCommits, eligiblePrs);
      } else {
        handleError(getHttpError(response));
      }
    }).catch(handleError);
  } else {
    parseResults(tagCommits, eligiblePrs);
  }
}

function parseResults(tagCommits, eligiblePrs) {
  // Throw an error if there are no eligible PRs.
  if (eligiblePrs.length === 0) {
    handleError(new Error('There are no impacting PRs; this is impossible!'));
  } else {
    // Sort the list of PRs by number.
    eligiblePrs.sort(function(a, b) { return a.number - b.number; });
    // Get all the commits in the base tag.
    var mode = 'none';
    console.log('PRs impacting the new codebase version:');
    for (let pr of eligiblePrs) {
      if (!tagCommits.includes(pr.merge_commit_sha)) {
        // This PR is newly merged since the base tag.
        // Figure out what type of PR it is.
        // Unlabeled PRs are treated as bugs.
        var labels = pr.labels.map(function(label) { return label.name; });
        var label = '';
        if (labels.includes('breaking')) label = 'breaking';
        else if (labels.includes('enhancement')) label = 'enhancement';
        else if (labels.includes('devops')) label = 'devops';
        else label = 'bug';
        console.log(`- #${pr.number} (${pr.html_url}) ${pr.title} [${label}]`);
        // Update the mode accordingly.
        if (label === 'breaking') mode = 'major';
        else if (label === 'enhancement'
          && mode !== 'major') mode = 'minor';
        else if (label === 'bug'
          && mode !== 'major'
          && mode !== 'minor') mode = 'patch';
      }
    }
    // Done. Send the mode back to the script.
    console.log(`Resulting version change: ${mode}`);
    fs.writeFileSync('mode.txt', mode);
  }
}

// *** Utility functions ***
// Error handling function.
function handleError(err) {
  console.log(err);
  process.exitCode = 1;
}
// child_process.exec, as a promise.
function execPromise(cmd, options) {
  return new Promise((resolve, reject) => {
    cp.exec(cmd, options, (error, stdout, stderr) => {
      if (error) {
        reject(error);
      } else if (stderr) {
        reject(stderr);
      } else {
        resolve(stdout);
      }
    });
  });
}
// Function that does paginated GET requests on the GitHub API
// and returns all relevant results in an array.
function getPaginated(options, resultList = []) {
  return new Promise(function(resolve, reject) {
    github.get(options).then(function(response) {
      if (response.statusCode === 200) {
        // Add these results to our list.
        resultList = resultList.concat(response.body);
        // Follow pagination if necessary.
        var next = '';
        if (response.headers.hasOwnProperty('link')) {
          next = plh(response.headers.link).next;
          if (next) next = next.url;
          if (next) next = next.replace(apiPrefix, '');
        }
        if (next) {
          var newOptions = Object.assign({}, options);
          newOptions.uri = next;
          // Wait for 1 second before getting the next page, to avoid abuse rate limits.
          setTimeout(function() {
            getPaginated(newOptions, resultList).then(function(newResultList) {
              resolve(newResultList);
            });
          }, 1000);
        } else {
          resolve(resultList);
        }
      } else {
        reject(getHttpError(response));
      }
    }).catch(function(e) { reject(e); });
  });
}
// Returns an error object from an HTTP response object.
function getHttpError(response) {
  return new Error(`HTTP request failure: ${response.statusCode} ${response.statusMessage}`)
}
