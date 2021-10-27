# Keep

  A collection of helper utilities for working in the shell. Useful for quickly
    storing commands and directories from the commandline, so you can come back
    to them later.

## Inspirations

At work, I've often found myself working on one project for a long time,
  accumulating a series of commands I use frequently to operate in that
  development environment, then context switching to a different project for a
  few months. When I find myself coming back to that first project, I've lost
  all context on what the important commands are, what paths are important,
  etc.
So I wrote this tool as a way of managing these workspaces from the
  commandline with a uniform interface.

There are two main concepts here: `do`ing commands and `go`ing to directories.
Both of these are things that can be done within the context of a `work`space.

Because I work on `conhost` (and tangentially to `cmd.exe`, but mostly to
 just people no we can't add that), these are scripts built for `cmd`. They
 don't work with powershell. I'm sure they could, but I don't really care to
 make that happen. I work in cmd, so these work in cmd.

## Commands

### `#work`

Lists all of your workspaces, or switch to a new workspace.
Workspaces have a root directory that they automatically switch you to, and
  they can be set up with an initial command to run. This can be helpful for
  running setup commands that you might want to everytime you load that
  workspace.
For example, setting environment variables, running `git status`, setting a
  color scheme with [colortool](https://www.github.com/microsoft/console), etc.

### `#stash` and `#do`

`#stash <commandline>` is used to store a command from the commandline.

`#do <command id>` lets you execute a saved command

### `#keep` and `#go`

`#keep <path>` is used to store a directory from the commandline.
  Use `#keep .` to keep the current working directory.

`#go <directory id>` takes you to a given directory.

### Others

`#new <path> <workspace name>` creates a new workspace
`#backend` will print the path to the backend file, so you can try editing it
  by hand.
`#list` prints out all the directories and the commands for the current
  workspace.


## Notes

When keeping a directory or stashing a command, cmd is going to try and
  evaluate any environment variables _before_ the command/directory is saved.
So if you want to keep the `%USERPROFILE%` directory, then you'll actually
  need to run `#keep %%USERPROFILE%%`, using the double '%' chars to escape
  the evaluation.
On the way out, cmd is going to expand them again.
So if `%%USERPROFILE%%` is kept as directory #1, `#go 1` will try to change
  directory to `C:\Users\<your username>` (or whatever `%userprofile`% is set
  to).

