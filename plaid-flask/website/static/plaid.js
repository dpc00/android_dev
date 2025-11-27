const { Configuration, PlaidApi, PlaidEnvironments } = require('plaid');

const CLIENT_ID = "63f128ec7ba715001385cd7c";
const SECRET = "e688a320e5481254abb96aca9db812";
const ACCOUNT = "qn8mYA9LOJH1L5pzwDJYUEXY4rn9zPCJ3RxOp"
const ACCESS_TOKEN = "access-development-cced815d-8936-42fc-94c3-b28a8655c8b8"

const configuration = new Configuration({
  basePath: PlaidEnvironments.development,
  baseOptions: {
    headers: {
      'PLAID-CLIENT-ID': CLIENT_ID,
      'PLAID-SECRET': SECRET,
    },
  },
});

const client = new PlaidApi(configuration);

function getNetspend
client.accountsGet({'access_token':ACCESS_TOKEN})
.then(
    (accounts_response) => {
        console.log(accounts_response.data.accounts[0].balances.current);
    })
.catch(
    (error) => {
        const err = error.response.data;
        console.log(err)
    });

