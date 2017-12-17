# Design Brainstorming

  Everything is stored as json, so that it is easy to read.


## Workspaces

  These are the toplevel entries, a collection of directories and
  `#work`: list workspaces
  `#work [ID]`: switch to workspace `[ID]`

  Has an ID (auto generated), name (unique, optional) and a collection of notes

  two sets of json. The toplevel one, that's just id's and paths (to the actual json), and an actual json that has the name, notes, directories, commands, etc.
  EH no don't love that.
  Just one big set of json

  ### Workspace List Schema
  ```
{
    'workspaces': [{
        'id': int
        , 'root': str // The root dir of the workspace. Switched to when #work %d is called
        , 'name': str, opt
        , 'notes': [str]
        , 'dirs': [{
            'id': int
            , 'path': str
            , 'name': str
            , 'notes': [str]
        }]
        , 'commands': [{
            'id': int
            , 'path': str
            , 'name': str
            , 'notes': [str]
        }]
    }]
}
  ```


  ### Workspace Schema
  ```
  {
    'name': str, opt
    , 'notes': [str]
    , 'root': the

  }
  ```


  Created with `#new`
  Or I guess it could be created with `#work .`

## `keep` and `go`

  Remember a directory so that it can easily be switched to.

  Directory entries should have ID (auto increment), optional name, notes

  `#go` Goes to a directory

## `?something?`(`#stash` ?) and `do`

  Also `#in <dir_id> #do <command_id>`
  Does #in..do pushd, cd, do, popd? Or just cd, do?

## `archive`

  Stores away a dir, command or workspace in the "archive", just another set of data that we can later sort through.


## namespaced commands

  Say I have a command in another workspace I want to use, how do?

  `#work 1` - Switch to workspace 1
  `#do 2:1` - Do command 1 from workspace 2
  `#do :1` - Do command 1 from the global workspace

