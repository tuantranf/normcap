# How To Release new version

(Notes to myself)

## Prepare

1. Commit latest changes to `dev`, and see if tests run through
2. Increase version number (major.minor.patch):

```sh
bumpversion major
bumpversion minor
bumpversion patch
```

## Merge

1. Create pull request from master to dev
2. See, if all tests ran through
3. Merge branch

## Tag version

1. Tag version and push:

```sh
git checkout -b master
git pull
git tag v0.1.4
git push follow-tags
```

2. Check if build ran through

## Upload to pypi
