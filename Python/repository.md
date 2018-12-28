# Repository

## git

```python
import git

def cleanGit():
	with git.Repo.init(path=ROOTDIR) as repo:
		repo.index.checkout(force=True)
		repo.git.clean('-df')
		repo.remote().pull()

def pushGit(commit):
	with git.Repo.init(path=ROOTDIR) as repo:
		repo.git.add('--all')
		repo.git.commit('-m', commit)
		repo.remotes.origin.push()

```