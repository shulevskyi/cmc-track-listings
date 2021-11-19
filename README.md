## Instruction

That code provides access to Public-API from CoinMarketCap and grabs info about recently listed tokens.

### Dive into the structure

Let us find out about API. Public-API provides faster data for the user than Pro API (idk why); thus, we can quickly grab data and apply it wherever needed.
It is not as structured and ready for the developer as Pro API, but it does not matter now. We use /map endpoint; due to it being a Public API, it does not require any calls from us; thus, we can maintain the server forever without any additional cost, and it is fantastic. Compared to pro-API, which has only 10000 calls per month.
  
#### Endpoint /map
This endpoint provides us with all cryptocurrencies on CMC, even if it’s not listed yet. In parameters, we may specify what we want to see, inactive, untracked or fully active tokens.
Currently, there is code based on the untracked listing;

What does it mean? Simply, it means that when a token goes from inactive to untracked, it’s already on CMC; however, it has no access to everyone, so
it’s the perfect time to buy it. When it disappears from untracked, it goes to active, and it is a time when everyone may see it and most likely buy.
