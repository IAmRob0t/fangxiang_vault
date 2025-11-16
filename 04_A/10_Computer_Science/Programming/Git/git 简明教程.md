---
tags:
  - git
---
# Git 常用命令

| GIT命令                | 说明              | 示例                                     |
| -------------------- | --------------- | -------------------------------------- |
| `clone`              | 克隆，从远程下载仓库      | `git clone https:/xxx.yyy.com/zzz.git` |
| `pull`               | 拉取，从远程更新仓库      | `git pull origin`                      |
| `log`                | 查看本地仓库的记录       | `git log`<br>快捷键：f前翻、b后翻、q退出           |
| `status`             | 查看本地仓库状态，比如有无修改 | `git status`                           |
| `remote show origin` | 查看服务仓库状态，比如有无更新 | `git remote show   origin`             |
| `pull origin`        | 更新命令，从服务器下载     | `git pull origin`                      |

> [!warning] 注意
> 不执行 `git remote show origin` 查看状态，而是直接执行 `git pull origin` 也是可以的，后面这个命令会自动检查，有更新它就会下载更新部分，没有更新也会提示你

