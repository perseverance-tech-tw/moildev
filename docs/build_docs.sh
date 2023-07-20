#!/bin/bash
set -x

# *************************** Install dependencies *************************
apt-get update
apt-get -y install git rsync python3-sphinx python3-sphinx-rtd-theme python3-stemmer python3-git python3-pip python3-virtualenv python3-setuptools

python3 -m pip install --upgrade rinohtype pygments

# prevent git "detected dubious ownership" errors
git config --global --add safe.directory "*"

cd docs
pwd
ls -lah
export SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)

# make a new temp dir which will be our GitHub Pages docroot
docroot=`mktemp -d`

export REPO_NAME="${GITHUB_REPOSITORY##*/}"

# ***************************  Build Docs *************************
# first, cleanup any old builds' static assets
make clean

# get a list of branches, excluding 'HEAD' and 'gh-pages'
versions="`git for-each-ref '--format=%(refname:lstrip=-1)' refs/remotes/origin/ | grep -viE '^(HEAD|gh-pages)$'`"
for current_version in ${versions}; do

   # make the current language available to conf.py
   export current_version
   git checkout ${current_version}

   echo "INFO: Building sites for ${current_version}"

   # skip this branch if it doesn't have our docs dir & sphinx config
   if [ ! -e 'conf.py' ]; then
      echo -e "\tINFO: Couldn't find 'conf.py' (skipped)"
      continue
   fi

   languages="en `find locales/ -mindepth 1 -maxdepth 1 -type d -exec basename '{}' \;`"
   for current_language in ${languages}; do

      # make the current language available to conf.py
      export current_language

      echo "INFO: Building for ${current_language}"

      # HTML #
      sphinx-build -b html . _build/html/${current_language}/${current_version} -D language="${current_language}"

      # PDF #
      sphinx-build -b rinoh . _build/rinoh -D language="${current_language}"
      mkdir -p "${docroot}/${current_language}/${current_version}"
      cp "_build/rinoh/target.pdf" "${docroot}/${current_language}/${current_version}/Moildev-docs_${current_language}_${current_version}.pdf"

      # EPUB #
      sphinx-build -b epub . _build/epub -D language="${current_language}"
      mkdir -p "${docroot}/${current_language}/${current_version}"
      cp "_build/epub/target.epub" "${docroot}/${current_language}/${current_version}/Moildev-docs_${current_language}_${current_version}.epub"

      # copy the static assets produced by the above build into our docroot
      rsync -av "_build/html/" "${docroot}/"

   done

done

# return to main branch
git checkout main

# ***************************  Update GitHub Pages *************************

git config --global user.name "${GITHUB_ACTOR}"
git config --global user.email "${GITHUB_ACTOR}@users.noreply.github.com"

pushd "${docroot}"

# don't bother maintaining history; just generate fresh
git init
git remote add deploy "https://token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
git checkout -b gh-pages

# add .nojekyll to the root so that github won't 404 on content added to dirs
# that start with an underscore (_), such as our "_content" dir..
touch .nojekyll

# add redirect from the docroot to our default docs language/version
cat > index.html <<EOF
<!DOCTYPE html>
<html>
   <head>
      <title>Moilapp Docs</title>
      <meta http-equiv = "refresh" content="0; url='/${REPO_NAME}/en/${current_version}/'" />
   </head>
   <body>
      <p>Please be patient while we redirect you to our <a href="/${REPO_NAME}/en/${current_version}/">documentation</a>.</p>
   </body>
</html>
EOF

# Add README
cat > README.md <<EOF
# GitHub Pages

Nothing to see here. The contents of this branch are essentially a cache that's not intended to be viewed.


If you're looking to update our documentation, check the relevant version of developed branch.

EOF

# copy the resulting html pages built from sphinx above to our new git repo
git add .

# commit all the new files
msg="Updating Docs for commit ${GITHUB_SHA} made on `date -d"@${SOURCE_DATE_EPOCH}" --iso-8601=seconds` from ${GITHUB_REF} by ${GITHUB_ACTOR}"
git commit -am "${msg}"

# overwrite the contents of the gh-pages branch on our github.com repo
git push deploy gh-pages --force

popd # return to main repo sandbox root

# exit cleanly
exit 0