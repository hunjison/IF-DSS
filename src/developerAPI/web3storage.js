// npm install web3.storage
import { Web3Storage } from 'web3.storage'

function getAccessToken () {
  // Put your token here
  var token = "YOUR TOKEN";
  return token;
}

function makeStorageClient () {
  return new Web3Storage({ token: getAccessToken() });
}

async function checkStatus (cid) {
  const client = makeStorageClient();
  const status = await client.status(cid);
  if (status) {
    console.log(JSON.stringify(status, null, 2));
  };
}

// replace with your own CID to see info about your uploads!
checkStatus(process.argv[2]);