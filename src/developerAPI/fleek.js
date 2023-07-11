// Your Key goes here
const fleekAPIKey = "htCvmwK8hk1H1XDY/rd5eLWqOih1Zq1URZ8ykXJzwRg=";

// Your site name goes here
const your_site_name = process.argv[2]

const endpoint = 'https://api.fleek.co/graphql'
const query = `query {
    getSiteBySlug(slug: "${your_site_name}") {
        id
        name
        platform
        publishedDeploy {
            id
            status
            ipfsHash
            log
            completedAt
        }
        team {
            id
            name
        }
    }
}`

fetch(
  endpoint,
  {
    method: 'POST',
    headers: { 
        'Content-Type' : 'application/json',
        'authorization' : fleekAPIKey
     },
    body: JSON.stringify({ query })
  }
)
  .then(res => res.json())
  .then(json => console.log(JSON.stringify(json.data, null, 2)))