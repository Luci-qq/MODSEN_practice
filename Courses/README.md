# MODSEN_Courses

Здесь кратко описаны задачи поставленные курсом и мои решения

# HTTP

Задача: получить все статусы ответов HTTP

## Кратко о статусах, которые можно получить используя HTTP requests:

1.  Информационные ответы (100 – 199)
2.  Успешные ответы (200 – 299)
3.  Сообщения о перенаправлении (300 – 399)
4.  Ошибки клиента (400 – 499)
5.  Ошибки сервера (500 – 599)

## API которые я использовал:

1. https://reqres.in/api
2. https://jsonplaceholder.typicode.com

## Решение:

```plaintext
Successful Response - 200
Successful Response - 201
Redirect Response - 301
ErrorClient Response - 400
ErrorClient Response - 404
```

## Почему не смог получить 100ые и 500ые статусы ответа

Ответы 1xx (100-е коды):

- Предназначение для информационного обмена: Коды статуса 100-е используются для промежуточных информационных ответов. Наиболее часто используется код 100 (Continue), который сообщает клиенту, что сервер получил начальную часть запроса и клиент может продолжить отправку оставшейся части.
- Редко используются в реальной жизни: Хотя эти коды существуют, они используются редко.
  Клиенты и серверы в основном работают с кодами 200 и выше. Например, код 101 (Switching Protocols) используется для переключения протоколов,
  что также нечасто встречается.
- Автоматическое управление: Большинство современных HTTP-библиотек и фреймворков автоматически управляют
  промежуточными 1xx ответами, так что клиентские приложения редко видят эти коды напрямую.
  Ответы 5xx (500-е коды)
- Серверные ошибки: Коды статуса 500-е означают, что на сервере произошла ошибка, которая мешает выполнению запроса. Например,
  код 500 (Internal Server Error) указывает на общую проблему на стороне сервера.
- Предполагается стабильная работа сервера: В нормальных условиях серверы настроены и протестированы для стабильной работы,
  минимизируя возникновение ошибок. Администраторы и разработчики принимают меры по предотвращению сбоев.
- Обработка ошибок: Современные серверные системы часто имеют механизмы для обработки и логирования ошибок,
  а также для возврата клиентам более дружественных сообщений об ошибках, что может скрывать исходные 500-е коды.
  Примеры:
  100 (Continue): Клиент отправляет запрос с большой загрузкой данных и ожидает подтверждения от сервера, что можно продолжать отправку.
  500 (Internal Server Error): Сервер не может обработать запрос из-за внутренней ошибки, например, из-за сбоя в работе кода или базы данных.
  Таким образом, в обычной ситуации коды 100 и 500 встречаются реже из-за специфичности их применения и мер по предотвращению ошибок на сервере.

# Git

Задача полностью пройти приложение https://learngitbranching.js.org/

## Решение:

Main:

- 1: Introduction to Git Commits

  ```plaintext
  git commit
  git commit
  ```

- 2: Branching in Git

```plaintext
git branch bugFix
git checkout bugFix
```

- 3: Merging in Git

```plaintext
git branch bugFix
git checkout bugFix
git commit
git checkout main
git commit
git merge bugFix
```

- 4: Rebase Introduction

```plaintext
git branch bugFix
git checkout bugFix
git commit
git checkout main
git commit
git checkout bugFix
git rebase main
```

- 1: Detach yo' HEAD

```plaintext
git checkout C4
```

- 2: Relative Refs (^)

```plaintext
git checkout bugFix^
```

- 3: Relative Refs #2 (~)

```plaintext
git checkout C1
git branch -f main C6
git branch -f bugFix bugFix~3
```

- 4: Reversing Changes in Git

```plaintext
git reset HEAD~1
git checkout pushed
git revert HEAD
```

- 1: Cherry-pick Intro

```plaintext
git cherry-pick C3 C4 C7
```

- 2: Interactive Rebase Intro

```plaintext
git rebase -i HEAD~4
```

- 1: Grabbing Just 1 Commit

```plaintext
git checkout main
git cherry-pick C4
```

- 2: Juggling Commits

```plaintext
git rebase -i main
git commit --amend
git rebase -i main
git branch -f main caption
```

- 3: Juggling Commits #2

```plaintext
git checkout main
git cherry-pick C2
git commit --amend
git cherry-pick caption
```

- 4: Git Tags

```plaintext
git checkout C2
git tag v1 C2
git tag v0 C1
```

- 5: Git Describe

```plaintext
  git describe main
  git describe side
  git describe bugFix
  git commit
```

- 1: Rebasing over 9000 times

```plaintext
git rebase main bugFix
git rebase bugFix side
git rebase side another
git rebase another main
```

- 2: Multiple parents

```plaintext
git branch bugWork HEAD~^2~
```

- 3: Branch Spaghetti

```plaintext
git checkout one
git cherry-pick C4 C3 C2
git checkout two
git cherry-pick C5 C4 C3 C2
git branch -f three C2
```

Remote:

- 1: Clone Intro

```plaintext
git clone
```

- 2: Remote Branches

```plaintext
git commit
git checkout o/main
git commit
```

- 3: Git Fetchin'

```plaintext
git fetch
```

- 4: Git Pullin'

```plaintext
git pull
```

- 5: Faking Teamwork

```plaintext
git clone
git fakeTeamwork main 2
git commit
git pull
```

- 6: Git Pushin'

```plaintext
git commit
git commit
git push
```

- 7: Diverged History

```plaintext
git clone
git fakeTeamwork
git commit
git pull --rebase
git push
```

- 8: Locked Main

```plaintext
git reset --hard o/main
git checkout -b feature C2
git push origin feature
```

- 1: Push Main!

```plaintext
git rebase side1 side2
git rebase side2 side3
git rebase side3 main
git pull --rebase
git push
```

- 2: Merging with remotes

```plaintext
git checkout main
git pull
git merge side1
git merge side2
git merge side3
git push
```

- 3: Remote Tracking

```plaintext
git checkout -b side o/main
git commit -m "My commit"
git pull --rebase
git push
```

- 4: Git push arguments

```plaintext
git push origin main
git push origin foo
```

- 5: Git push arguments -- Expanded!

```plaintext
git push origin main~1:foo
git push origin foo:main
```

- 6: Fetch arguments

```plaintext
git fetch origin c6:main
git fetch origin c3:foo
git checkout foo
git merge main
```

- 7: Source of nothing

```plaintext
git push origin :foo
git fetch origin :bar
```

- 8: Pull arguments

```plaintext
git pull origin c3:foo
git pull origin c2:side
```
