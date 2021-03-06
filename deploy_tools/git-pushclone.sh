#!/bin/bash
#
# This clones a repository *to* a remote server
# and makes this new repository a remote
# repository of the current one. SSH protocol is used.
# In essence, this makes up for the fact that 'git clone' doesn't support
# the normal URL schemes for the remote.
#
# This implements a push-style of cloning, which is necessary whenever
# one does not want to clone from the remote machine. Examples are:
#
# 1. No incoming access to local server:
#    When development has occurred on a local machine to which one does not
#    wish to grant any remote access, but it is desired to 'publish' the
#    development to a server from which others can then get access.
#
# 2. A communal login to remote server:
#    When one does not have individual
#    access to the remote server but can only login as a group user: in this
#    case, initiating a clone from the remote server would require putting
#    credentials for the local repository server in the group account of the
#    server.
#
# Author: Robert Muil.
# from https://raw.githubusercontent.com/robertmuil/muiltools/master/bin/git-pushclone

usage () {
	echo "Usage:"
	echo ""
	echo "`basename $0` [-Btny] [-s <sshopts>] <repository_to_clone> <server> <remote_path> [<remote_name>]"
	echo ""
	echo " -B: don't make remote a bare copy (i.e. allow it to have a working copy)."
	echo " -t: set local branch to track corresponding remote branch (upstream)."
	echo " -n: no-action - don't actually do anything, just show what would be done."
	echo " -y: assume-yes - don't prompt, just do"
	echo " -s: sshopts are options to pass to the ssh command, such as to use a different key file"
	echo ""
	echo " <repository_to_clone>: local repository to clone."
	echo " <server>: the full server URL to clone to, including username if required."
	echo " <remote_path>: the base directory under which the remote repo will be placed."
	echo " <remote_name> (optional): name to refer to the remote repository from this repository (defaults to first component of server)."
	exit 1
}

tmpdir="tmp"

remote_bare=true
track_upstream=false
do_work=true
assume_yes=false
update_backlink=true
ssh_opts=""

while getopts "nyBts:?h" opt; do
	case $opt in
		B) remote_bare=false;;
		t) track_upstream=true;;
		n) do_work=false;;
		y) assume_yes=true;;
		s) ssh_opts=$OPTARG;;
		?|h)
			usage
			;;
		*)
			echo "Unknown option: -$opt"
			usage
			;;
	esac
done
shift $((OPTIND-1))

orig_repo="$1"
srv="$2"
remotepath="$3"
remotename="$4"
ssh="ssh $ssh_opts"
scp="scp $ssh_opts"

if [ -z "$orig_repo" -o -z "$srv" -o -z "$remotepath" ]; then
	usage;
fi

set -o nounset
set -o errexit

clone_opts=""
if $remote_bare; then
	clone_opts="$clone_opts --bare"
	bare_repo="${orig_repo}.git"
else
	bare_repo="${orig_repo}"
fi
if [ -z "$remotename" ]; then
	#pretty sure using two awk invocations is not optimal, but it works
	remotename=$(echo $srv | awk -F'@' '{print $(NF)}' | awk -F'.' '{print $1}')
fi

echo orig_repo=$orig_repo
echo bare_repo=$bare_repo
echo server=$srv
echo clone_opts=$clone_opts
echo ssh_opts=$ssh_opts
echo remotepath=$remotepath
echo remotename=$remotename

if $do_work; then
	mkdir -p "$tmpdir"
fi
if [ -d "$tmpdir/${bare_repo}" ]; then
	echo "Error: '${tmpdir}/${bare_repo}' already exists."
	exit 3
fi

if $do_work; then
	git clone$clone_opts "$orig_repo" "$tmpdir/${bare_repo}"
else
	echo "DUMMY RUN: NOT OPERATING"
	echo "would do: $ git clone$clone_opts $orig_repo $tmpdir/${bare_repo}"
fi

if $update_backlink; then
	pushd "$tmpdir/${bare_repo}" &> /dev/null
	this_repo_dir=$(git config --get remote.origin.url)
	backlink="ssh://$USER@`hostname -f`/$this_repo_dir"
	echo "Setting remote's backlink to this repo from '${this_repo_dir}' to '${backlink}'..."
	if $do_work; then
		git remote set-url origin "${backlink}"
	else
		echo "would do: $ git remote set-url origin '${backlink}'"
	fi
	popd &> /dev/null
fi

echo "Ready to copy from \"$tmpdir/${bare_repo}\" to \"${remotepath}\" on \"${srv}\"..."
if $assume_yes; then
	echo "Assuming yes, continuing."
else
	echo "Press enter to continue, Ctrl-C to abort..."
	read
fi
if $do_work; then
	if $ssh ${srv} test -d "${remotepath}/${bare_repo}"; then
		echo "WARNING: '${remotepath}/${bare_repo}' exists on ${srv}... Continue? (Ctrl-C to abort)"
		read
	fi
	echo "Copying..."
	$scp -p -r "$tmpdir/${bare_repo}" "${srv}:${remotepath}/${bare_repo}"
	echo "Done copying."
	archive="$tmpdir/${bare_repo}."$(date +%Y-%m-%dT%H%M%S)".tgz"
	echo "Archiving local clone to '${archive}'..."
	tar czf "${archive}" "${tmpdir}/${bare_repo}"
	echo "Removing local clone..."
	rm -rf "${tmpdir}/${bare_repo}"
fi

echo "Configuring local-remote link..."
pushd "${orig_repo}" &> /dev/null
current_branch=`git rev-parse --abbrev-ref HEAD`
echo "Current branch is '$current_branch'."

if $do_work; then
	if git remote add "${remotename}" "ssh://${srv}/${remotepath}/${bare_repo}" 2>/dev/null; then
		echo "Fetching from remote..."
		if git fetch "$remotename"; then
			echo "success."
		else
			echo "could not fetch from remote. Not unexpected, and should not matter."
		fi
		if $track_upstream; then
			echo "Setting upstream branch ($current_branch) to track."
			git branch --set-upstream-to "$remotename"/"$current_branch"
		fi
	fi
fi
popd &> /dev/null
echo "Successfully finished cloning to remote."
