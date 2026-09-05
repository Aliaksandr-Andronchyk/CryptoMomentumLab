# Деплой на VPS Артёма (Portainer)

Стек `momentum` в Portainer (http://151.241.227.47:9000) собирается из git: форк
https://github.com/SashaAndronchyk/CryptoMomentumLab, ветка `deploy`, файл `deploy/docker-compose.yml`.
Portainer сам опрашивает ветку и пересобирает стек при новых коммитах (GitOps updates).

Адрес: https://momentum.151-241-227-47.sslip.io, вход по паролю (basic auth, пользователи `sasha` и `guest`).

Переменные стека (Portainer → Stacks → momentum → Environment variables):
- `SITE` — публичное имя хоста;
- `AUTH_USERS_B64` — base64 от строк `user bcrypt-hash` (по одной на пользователя). Сменить пароль:
  `htpasswd -nbB user pass | tr : " "` → добавить строку, закодировать `base64`, обновить переменную, redeploy.

Обновить код: закоммитить в `deploy` (или влить туда `master` автора) и запушить. Вручную: Portainer → Stacks →
momentum → Pull and redeploy. Кеш свечей живёт в томе `momentum-cache`, при пересборке не теряется.
