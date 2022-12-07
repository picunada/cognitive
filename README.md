AI-House license service.

The service has 4 permissions levels(roles) Administrator(superuser), Manager,
Client and API Client. <br>Main Usecase for all roles are described below.

### Configure .env file
```
❯ cp .env.template backend/.env
❯ nano backend/.env
```

### Build
```
❯ docker compose build
❯ docker compose run frontend npm i
```

### Run local 
```
❯ docker compose up
```

### Use main commands
```
❯ make build - build and start development containers
❯ make test - start tests
❯ make admin - create superuser
❯ make shell - launch django shell
```

### API documentation
```
http://127.0.0.1:8000/api/v1/swagger/
```

### Frontend
```
http://localhost:3333/
```
Admin Usecase:
- create/update/delete all organizations
- get all organization transactions and balances
- get/create/update/delete any users with Manager and Client roles
- create any organization API keys

Manager Usecase:
- get own organization's statistic, transactions and balances
- get/create/update/delete users with Client role for own organization's
- create own organization's API keys

Client Usecase:
- get own organization statistic, transactions and balance
- create own organization API keys

### API Client methods
```
GET /api/v1/organization/get_balance/
```
```
POST /api/v1/organization/sign_message/
```

API Client Usecase:
- get organization balance
- sine message

