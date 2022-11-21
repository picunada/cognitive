AI-House license service



### Configure .env file
```
❯ cp .env.template backend/.env
❯ nano backend/.env
```

### Use main commands
```
❯ make test - start tests
❯ make up - build and start development containers
❯ make admin - create superuser
❯ make shell - launch django shell
```

### API documentation
```
http://127.0.0.1:8000/api/v1/swagger/
```

### Frontend
```
http://lockalhost:3333/
```

## Main Usecase descriptions

Admin frontend Usecase:
- create/update/delete all organizations
- get all organization transactions and balances
- create/update/delete users with Client role
- create/update/delete any organization API keys

Client frontend Usecase:
- get own organization statistic, transactions and balance
- create/update/delete own organization API keys

With API-key backend authorization and message singe Usecase:
- get message from request payload and organization from API-key
- return message singed with organization RSA-key

